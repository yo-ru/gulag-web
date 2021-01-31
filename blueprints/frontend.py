# -*- coding: utf-8 -*-

import asyncio
import re
import time
import bcrypt
import hashlib
import aiohttp
import orjson
from quart import Blueprint, render_template, redirect, request, session
from cmyui import log, Ansi
from cmyui.discord import Webhook, Embed

from objects import glob
from objects.privileges import Privileges
from objects.utils import flash, get_safe_name

__all__ = ()

frontend = Blueprint('frontend', __name__)

""" valid modes, mods, sorts """
valid_modes = frozenset({'std', 'taiko', 'catch', 'mania'})
valid_mods = frozenset({'vn', 'rx', 'ap'})
valid_sorts = frozenset({'tscore', 'rscore', 'pp', 'plays',
                        'playtime', 'acc', 'maxcombo'})

""" home """
@frontend.route('/home') # GET
@frontend.route('/')
async def home():
    return await render_template('home.html')

""" settings """
@frontend.route('/settings') # GET
async def settings():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access user settings!', 'login')

    # TODO: user settings page
    NotImplemented

    return await render_template('settings.html')

@frontend.route('/u/<user>') # GET
async def profile(user):
    mode = request.args.get('mode', type=str)
    mods = request.args.get('mods', type=str)

    if mods:
        if mods not in valid_mods:
            return b'invalid mods! (vn, rx, ap)'
    else:
        mods = 'vn'
    if mode:
        if mode not in valid_modes:
            return b'invalid mode! (std, taiko, catch, mania)'
    else:
        mode = 'std'

    userdata = await glob.db.fetch(f'SELECT name, id, priv, country FROM users WHERE id = {user}')

    return await render_template('profile.html', user=userdata, mode=mode, mods=mods)

""" leaderboard """
@frontend.route('/leaderboard') # GET
async def leaderboard_nodata():
    return await render_template('leaderboard.html', mode='std', sort='pp', mods='vn')
@frontend.route('/leaderboard/<mode>/<sort>/<mods>') # GET
async def leaderboard(mode, sort, mods):
    return await render_template('leaderboard.html', mode=mode, sort=sort, mods=mods)

""" login """
@frontend.route('/login') # GET
async def login():
    # if authenticated; render home
    if 'authenticated' in session:
        return await flash('error', f'Hey! You\'re already logged in {session["user_data"]["name"]}!', 'home')

    return await render_template('login.html')
@frontend.route('/login', methods=['POST']) # POST
async def login_post():
    # if authenticated; deny post; return
    if 'authenticated' in session:
        return await flash('error', f'Hey! You\'re already logged in {session["user_data"]["name"]}!', 'home')

    login_time = time.time_ns() if glob.config.debug else 0

    form = await request.form
    username = form.get('username')

    # check if account exists
    user_info = await glob.db.fetch(
        'SELECT id, name, priv, pw_bcrypt, silence_end '
        'FROM users WHERE safe_name = %s',
        [get_safe_name(username)]
    )

    # the second part of this if statement exists because if we try to login with Aika
    # and compare our password input against the database it will fail because the
    # hash saved in the database is invalid.
    if not user_info or user_info['id'] == 1:
        if glob.config.debug:
            log(f'{username}\'s login failed - account doesn\'t exist.', Ansi.LYELLOW)
        return await flash('error', 'Account does not exist.', 'login')

    bcrypt_cache = glob.cache['bcrypt']

    pw_bcrypt = user_info['pw_bcrypt'].encode()
    pw_md5 = hashlib.md5(form.get('password').encode()).hexdigest().encode()

    # check credentials (password) against db
    # intentionally slow, will cache to speed up
    if pw_bcrypt in bcrypt_cache:
        if pw_md5 != bcrypt_cache[pw_bcrypt]: # ~0.1ms
            if glob.config.debug:
                log(f'{username}\'s login failed - pw incorrect.', Ansi.LYELLOW)
            return await flash('error', 'Password is incorrect.', 'login')
    else: # ~200ms
        if not bcrypt.checkpw(pw_md5, pw_bcrypt):
            if glob.config.debug:
                log(f'{username}\'s login failed - pw incorrect.', Ansi.LYELLOW)
            return await flash('error', 'Password is incorrect.', 'login')

        # login successful; cache password for next login
        bcrypt_cache[pw_bcrypt] = pw_md5

    # user not verified render verify page
    if user_info['priv'] == 1:
        if glob.config.debug:
            log(f'{username}\'s login failed - not verified.', Ansi.LYELLOW)
        return await render_template('verify.html')

    # login successful; store session data
    if glob.config.debug:
        log(f'{username}\'s login succeeded.', Ansi.LGREEN)

    session['authenticated'] = True
    session['user_data'] = {
        'id': user_info['id'],
        'name': user_info['name'],
        'priv': user_info['priv'],
        'silence_end': user_info['silence_end'],
        'is_staff': user_info['priv'] & Privileges.Staff
    }

    if glob.config.debug:
        login_time = (time.time_ns() - login_time) / 1e6
        log(f'Login took {login_time:.2f}ms!', Ansi.LYELLOW)

    # authentication successful; redirect home
    return await flash('success', f'Hey! Welcome back {username}!', 'home')

""" registration """
_username_rgx = re.compile(r'^[\w \[\]-]{2,15}$')
_email_rgx = re.compile(r'^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$')
@frontend.route('/register') # GET
async def register():
    # if authenticated; redirect home
    if 'authenticated' in session:
        return await flash('error', f'Hey You\'re already registered and logged in {session["user_data"]["name"]}!', 'home')

    return await render_template('register.html')
@frontend.route('/register', methods=['POST']) # POST
async def register_post():
    # if authenticated; deny post; return
    if 'authenticated' in session:
        return await flash('error', f'Hey You\'re already registered and logged in {session["user_data"]["name"]}!', 'home')

    # get form data (username, email, password)
    form = await request.form
    username = form.get('username')
    email = form.get('email')
    pw_txt = form.get('password')
    key = form.get('key')

    # Usernames must:
    # - be within 2-15 characters in length
    # - not contain both ' ' and '_', one is fine
    # - not be in the config's `disallowed_names` list
    # - not already be taken by another player
    # check if username exists
    if not _username_rgx.match(username):
        return await flash('error', 'Invalid username syntax.', 'register')

    if '_' in username and ' ' in username:
        return await flash('error', 'Username may contain "_" or " ", but not both.', 'register')

    # TODO: disallowed usernames
    NotImplemented

    if await glob.db.fetch('SELECT 1 FROM users WHERE name = %s', username):
        return await flash('error', 'Username already taken by another user.', 'register')

    # Emails must:
    # - match the regex `^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$`
    # - not already be taken by another player
    if not _email_rgx.match(email):
        return await flash('error', 'Invalid email syntax.', 'register')

    if await glob.db.fetch('SELECT 1 FROM users WHERE email = %s', email):
        return await flash('error', 'Email already taken by another user.', 'register')

    if key == "H4LOAL5VTHD9I6P20HCE":
        return await flash('error', 'Nice try...', 'register')

    if await glob.db.fetch('SELECT 1 FROM beta_keys WHERE beta_key = %s', key):
        key_valid = True
    else:
        return await flash('error', 'Invalid beta key.', 'register')

    if key_valid:
        used_key = await glob.db.fetch('SELECT used AS c FROM beta_keys WHERE beta_key = %s', key)
        if int(used_key['c']):
            return await flash('error', 'This beta key has already been used.', 'register')

    # Passwords must:
    # - be within 8-32 characters in length
    # - have more than 3 unique characters
    # - not be in the config's `disallowed_passwords` list
    if not 8 < len(pw_txt) <= 32:
        return await flash('error', 'Password must be 8-32 characters in length', 'register')

    if len(set(pw_txt)) <= 3:
        return await flash('error', 'Password must have more than 3 unique characters.', 'register')

    # TODO: disallowed passwords
    NotImplemented

    async with asyncio.Lock():
        pw_md5 = hashlib.md5(pw_txt.encode()).hexdigest().encode()
        pw_bcrypt = bcrypt.hashpw(pw_md5, bcrypt.gensalt())
        glob.cache['bcrypt'][pw_bcrypt] = pw_md5 # cache result for login

        safe_name = get_safe_name(username)

        # add to `users` table.
        user_id = await glob.db.execute(
            'INSERT INTO users '
            '(name, safe_name, email, pw_bcrypt, creation_time, latest_activity) '
            'VALUES (%s, %s, %s, %s, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())',
            [username, safe_name, email, pw_bcrypt]
        )

        # add to `stats` table.
        await glob.db.execute(
            'INSERT INTO stats '
            '(id) VALUES (%s)',
            [user_id]
        )

    if glob.config.debug:
        log(f'{username} has registered - awaiting verification.', Ansi.LGREEN)

    # user has successfully registered
    await glob.db.execute('UPDATE beta_keys SET used = 1 WHERE beta_key = %s', key)
    await glob.db.execute('UPDATE beta_keys SET user = %s WHERE beta_key = %s', [username, key])
    webhook_url = glob.config.webhooks['audit-log']
    webhook = Webhook(url=webhook_url)
    embed = Embed(title = f'')
    embed.set_author(url = f"https://{glob.config.domain}/u/{user_id}", name = username, icon_url = f"https://a.{glob.config.domain}/{user_id}")
    thumb_url = f'https://a.{glob.config.domain}/1'
    embed.set_thumbnail(url=thumb_url)
    embed.add_field(name = 'New user', value = f'{username} has registered.', inline = True)
    webhook.add_embed(embed)
    http = aiohttp.ClientSession(json_serialize=orjson.dumps)
    await webhook.post(http)
    return await render_template('verify.html')

""" logout """
@frontend.route('/logout') # GET
async def logout():
    if not 'authenticated' in session:
        return await flash('error', 'You can\'t logout if you aren\'t logged in!', 'login')

    if glob.config.debug:
        log(f'{session["user_data"]["name"]} logged out.', Ansi.LGREEN)

    # clear session data
    session.pop('authenticated', None)
    session.pop('user_data', None)

    # render login
    return await flash('success', 'Successfully logged out!', 'login')

""" rules """
@frontend.route('/rules') # GET
async def rules():
    return await render_template('rules.html')

""" discord redirect """
@frontend.route('/discord') # GET
async def discord():
    return redirect(glob.config.discord_server)
