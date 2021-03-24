# -*- coding: utf-8 -*-

import asyncio
import re
import time
import timeago
import bcrypt
import hashlib
import aiohttp
import orjson
import string
import random
import os
import aiofiles.os
from PIL import Image
from resizeimage import resizeimage
from quart import Blueprint, render_template, redirect, request, session
from cmyui import log, Ansi
from cmyui.discord import Webhook, Embed
from datetime import datetime
from email.mime.text import MIMEText

from objects import glob
from objects.privileges import Privileges
from objects.utils import flash, get_safe_name
from async_sender import Message

__all__ = ()

frontend = Blueprint('frontend', __name__)

""" valid modes, mods, sorts """
valid_modes = frozenset({'std', 'taiko', 'catch', 'mania'})
valid_mods = frozenset({'vn', 'rx', 'ap'})
valid_sorts = frozenset({'tscore', 'rscore', 'pp', 'plays',
                        'playtime', 'acc', 'maxcombo'})

_username_rgx = re.compile(r'^[\w \[\]-]{2,15}$')
_email_rgx = re.compile(r'^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$')

""" home """
@frontend.route('/home') # GET
@frontend.route('/')
async def home():
    vn = await glob.db.fetch('SELECT pp, users.name FROM scores_vn LEFT JOIN users ON scores_vn.userid = users.id LEFT JOIN maps ON scores_vn.map_md5 = maps.md5 WHERE users.priv & 1 AND users.frozen = 0 AND maps.status = 2 ORDER BY pp DESC LIMIT 1')
    rx = await glob.db.fetch('SELECT pp, users.name FROM scores_rx LEFT JOIN users ON scores_rx.userid = users.id LEFT JOIN maps ON scores_rx.map_md5 = maps.md5 WHERE users.priv & 1 AND users.frozen = 0 AND maps.status = 2 ORDER BY pp DESC LIMIT 1')
    ap = await glob.db.fetch('SELECT pp, users.name FROM scores_ap LEFT JOIN users ON scores_ap.userid = users.id LEFT JOIN maps ON scores_ap.map_md5 = maps.md5 WHERE users.priv & 1 AND users.frozen = 0 AND maps.status = 2 ORDER BY pp DESC LIMIT 1')
    try:
        return await render_template('home.html', vnpp=round(vn['pp']), vnuser=vn['name'], rxpp=round(rx['pp']), rxuser=rx['name'], appp=round(ap['pp']), apuser=ap['name'])
    except:
        return await render_template('home.html', vnpp=0, vnuser="None", rxpp=0, rxuser="None", appp=0, apuser="None")

""" settings """
@frontend.route('/settings') # GET
@frontend.route('/settings/profile') # GET
async def settings_profile():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access profile settings!', 'login')

    return await render_template('settings/profile.html')

""" avatars """
@frontend.route('/settings/avatar') # GET
async def settings_avatar():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access profile settings!', 'login')

    return await render_template('settings/avatar.html')

@frontend.route('/settings/password') # GET
async def settings_pw():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access password settings!', 'login')

    return await render_template('settings/password.html')

@frontend.route('/settings/password', methods=['POST']) # POST
async def settings_pw_post():
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to change your password!', 'login')

    # get required info from form
    form = await request.form
    old_text = form.get('old_password')
    oldpw = hashlib.md5(old_text.encode()).hexdigest().encode()
    newpw = form.get('new_password')
    check = form.get('repeat_password')

    # check new password & repeated password match
    if check != newpw:
        return await flash('error', "Repeat password doesn't match new password!", 'settings/password')


    # get current pw
    ui = await glob.db.fetch('SELECT pw_bcrypt FROM users WHERE id = %s', [session["user_data"]["id"]])
    dbpw = ui['pw_bcrypt'].encode()

    # check current pw against old pw
    bcache = glob.cache['bcrypt']
    if dbpw in bcache:
        if oldpw != bcache[dbpw]:
            return await flash('error', 'Old password is incorrect!', 'settings/password')
    else:
        if not bcrypt.checkpw(oldpw, dbpw):
            return await flash('error', 'Old password is incorrect!', 'settings/password')

    # make sure new password isn't the same as old password
    if old_text == newpw:
        return await flash('error', "Old and new password cannot be the same!", 'settings/password')

    # Passwords must:
    # - be within 8-32 characters in length
    # - have more than 3 unique characters
    # - not be in the config's `disallowed_passwords` list
    if not 8 <= len(oldpw) <= 32:
        return await flash('error', 'Password must be 8-32 characters in length', 'settings/password')

    if len(set(oldpw)) <= 3:
        return await flash('error', 'Password must have more than 3 unique characters.', 'settings/password')

    async with asyncio.Lock():
        # hash & cache new password
        newmd5 = hashlib.md5(newpw.encode()).hexdigest().encode()
        newbc = bcrypt.hashpw(newmd5, bcrypt.gensalt())
        bcache[newbc] = newmd5

        # set new password & make user relog
        await glob.db.execute('UPDATE users SET pw_bcrypt = %s WHERE id = %s', [newbc, session["user_data"]["id"]])
        session.pop('authenticated', None)
        session.pop('user_data', None)
        return await flash('success', 'Your password has been changed! Please login again.', 'login')

@frontend.route('/settings/avatar', methods=['POST']) # POST
async def settings_avatar_post():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access avatar settings!', 'login')

    APATH = f'{glob.config.gulag_path}/.data/avatars'
    EXT = glob.config.avatar_extensions
    
    files = await request.files

    #this could possibly not look ANY uglier
    avatar_file = (files.get('avatar'))
    ava = (os.path.splitext(avatar_file.filename.lower()))[1]
    new_dir = f"{APATH}/{session['user_data']['id']}{ava}"
    
    if ava not in EXT:
        return await flash('error', 'Please submit an image which is either a png, jpg, jpeg or gif file!', 'settings/avatar')

    # remove any old avatars
    for old_ava in EXT:
        old_dir = f"{APATH}/{session['user_data']['id']}{old_ava}"
        if os.path.exists(old_dir):
            await aiofiles.os.remove(old_dir)

    avatar_file.save(new_dir)

    # force image resizing
    img = Image.open(new_dir)
    width, height = img.size
    if width > 256 or height > 256:
        new = resizeimage.resize_cover(img, [256, 256])
        new.save(new_dir, img.format)

    return await flash('success', 'Your avatar has been successfully changed!', 'settings/avatar')

@frontend.route('/settings/profile', methods=['POST']) # POST
async def settings_profile_post():
    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access profile settings!', 'login')
    
    # form data
    form = await request.form
    username = form.get('username')
    email = form.get('email')

    # no data has changed; deny post
    if username == session['user_data']['name'] and email == session['user_data']['email']:
        return await flash('error', 'No changes have been made.', 'settings/profile')

    # Usernames must:
    # - be within 2-15 characters in length
    # - not contain both ' ' and '_', one is fine
    # - not be in the config's `disallowed_names` list
    # - not already be taken by another player
    if not _username_rgx.match(username):
        return await flash('error', 'Your new username syntax is invalid.', 'settings/profile')

    if '_' in username and ' ' in username:
        return await flash('error', 'Your new username may contain "_" or " ", but not both.', 'settings/profile')

    if await glob.db.fetch('SELECT 1 FROM users WHERE name = %s AND NOT name = %s', [username, session['user_data']['name']]):
        return await flash('error', 'Your new username already taken by another user.', 'settings/profile')

    # Emails must:
    # - match the regex `^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$`
    # - not already be taken by another player
    if not _email_rgx.match(email):
        return await flash('error', 'Email syntax is invalid.', 'settings/profile')

    if await glob.db.fetch('SELECT 1 FROM users WHERE email = %s AND NOT email = %s', [email, session['user_data']['email']]):
        return await flash('error', 'This email is already taken by another user.', 'settings/profile')

    # username change successful
    if session['user_data']['is_donator']:
        if username != session['user_data']['name']:
            await glob.db.execute('UPDATE users SET name = %s, safe_name = %s WHERE safe_name = %s', [username, get_safe_name(username), get_safe_name(session['user_data']['name'])])
    elif not session['user_data']['key'] and username != session['user_data']['name']:
        return await flash('error', 'You must be a supporter or staff member to change your username!')
    
    # email change successful
    if email != session['user_data']['email']:
        safe_name = get_safe_name(username) if username != session['user_data']['name'] else get_safe_name(session['user_data']['name'])
        await glob.db.execute('UPDATE users SET email = %s WHERE safe_name = %s', [email, safe_name])

    # logout
    session.pop('authenticated', None)
    session.pop('user_data', None)
    return await flash('success', 'Your username/email have been changed! Please login again.', 'login')

@frontend.route('/key') # GET
async def keygen():
    if not glob.config.keys:
        return await flash('error', 'The use of keys is currently disabled/unneeded!', 'home')

    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access the key gen!', 'login')

    if not session["user_data"]["is_donator"] and not session["user_data"]["is_staff"]:
        return await flash('error', 'You must be a donator to do this!', 'home')

    return await render_template('key.html')

@frontend.route('/key', methods=['POST'])
async def gen_key():
    if glob.config.keys:
        form = await request.form
        if form['submit'] == 'Generate':
            if session["user_data"]["is_donator"] or session["user_data"]["is_staff"]:
                    e = await glob.db.fetch(f'SELECT keygen FROM users WHERE id = {session["user_data"]["id"]}')
                    if not e['keygen'] > 0 and session["user_data"]["is_donator"]:
                        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
                        await glob.db.execute('INSERT INTO beta_keys(beta_key, generated_by) VALUES (%s, %s)', [key, session["user_data"]["name"]])
                        await glob.db.execute('UPDATE users SET keygen = keygen + 1 WHERE id = %s', [session["user_data"]["id"]])
                        return await render_template('key.html', keygen=key)
                    elif e['keygen'] > 0 and session["user_data"]["is_donator"]:
                        return await flash('error', 'You have already generated a key!', 'key')
                    elif session["user_data"]["is_staff"]:
                        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
                        await glob.db.execute('INSERT INTO beta_keys(beta_key, generated_by) VALUES (%s, %s)', [key, session["user_data"]["name"]])
                        return await render_template('key.html', keygen=key)
            else:
                return await flash('error', 'You do not have permissions to do this!', 'key')
        else:
            return await render_template('key.html')
    else:
        return await flash('error', 'The use of keys is currently disabled/unneeded!', 'home')

@frontend.route('/pwreset') # GET
async def pw():
    return await render_template('pwreset.html')

@frontend.route('/pwreset', methods=['POST'])
async def reset_pw():
    form = await request.form
    if form['submit'] == 'Submit':
        username = form['username']
        e = await glob.db.fetch('SELECT email, id FROM users WHERE safe_name = %s', [username.lower()])
        try:
            email = e['email']
            uid = e['id']
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            mail = f"""
            Hey {username}!

            Someone, hopefully you, has requested to reset your {glob.config.app_name} password! If this was you, please click <a href="https://{glob.config.domain}/changepw?code={code}">here</a> to reset your password. If it was not you who requested this password reset, you can simply ignore this email.
            """
            msg = MIMEText(mail, 'html')
            await Message(f"{glob.config.app_name} Password Reset", from_address=f"contact@{glob.config.domain}", to=email, body=msg)
            await glob.db.execute('INSERT INTO pwreset(uid, code, used, gentime) VALUES (%s, %s, 0, UNIX_TIMESTAMP())', [uid, code])
            return await flash('success', "Password reset email sent! Please check your emails for further instructions.", 'home')
        except:
            return await flash('error', "Couldn't find a user with that username!", 'pwreset')
    else:
        return await render_template('pwreset.html')


@frontend.route('/u/<user>') # GET
async def profile(user):
    mode = request.args.get('mode', type=str)
    mods = request.args.get('mods', type=str)

    try:
        if 'authenticated' in session and int(user) == int(session['user_data']['id']):
            dist = True
        else:
            dist = False
    except:
        if 'authenticated' in session and user.lower() == session['user_data']['name'].lower():
            dist = True
        else:
            dist = False

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

    try:
        userdata = await glob.db.fetch("SELECT name, id, priv, country, frozen, freezetime FROM users WHERE id = %s OR safe_name = %s", [user, get_safe_name(user)])
        freezeinfo = [userdata['frozen'], timeago.format(datetime.fromtimestamp(userdata['freezetime']), datetime.now())]
        if await glob.db.fetch('SELECT 1 FROM user_badges WHERE userid = %s', [userdata['id']]):
            badges = True
            defbadges = await glob.db.fetchall("SELECT badgeid, badges.name, badges.colour, badges.icon FROM user_badges LEFT JOIN badges ON user_badges.badgeid = badges.id WHERE userid = %s", [userdata['id']])
        else:
            badges = None
            defbadges = None

        in_clan = await glob.db.fetch("SELECT clan_id FROM users WHERE id = %s", [userdata['id']])
        if in_clan['clan_id'] is not None:
            isclan = in_clan['clan_id']
            clandata = await glob.db.fetch("SELECT tag FROM clans WHERE id = %s", [isclan])
            if clandata is not None:
                clantag = f"[{clandata['tag']}]"
            else:
                clantag = ""
        else:
            clantag = ""

        if not int(userdata['priv']) & 1:
            res = True
            if 'authenticated' in session:
                if session["user_data"]["id"] != userdata['id'] and not session["user_data"]["is_staff"]:
                    return await render_template('resuser.html')
                else:
                    return await render_template('profile.html', user=userdata, mode=mode, mods=mods, tag=clantag, freeze=freezeinfo, ub=False, dist=dist, res=res)
            else:
                return await render_template('resuser.html')
        else:
            res = False
    except:
        return await render_template('nouser.html')

    return await render_template('profile.html', user=userdata, mode=mode, mods=mods, tag=clantag, freeze=freezeinfo, ub=badges, bi=defbadges, dist=dist, res=res)

""" leaderboard """
@frontend.route('/leaderboard') # GET
async def leaderboard_nodata():
    return await render_template('leaderboard.html', mode='std', sort='pp', mods='vn')
@frontend.route('/leaderboard/<mode>/<sort>/<mods>') # GET
async def leaderboard(mode, sort, mods):
    return await render_template('leaderboard.html', mode=mode, sort=sort, mods=mods)

@frontend.route('/leaderboard/clans') # GET
async def c_leaderboard_nodata():
    return await render_template('clans/c-leaderboard.html', mode='std', sort='pp', mods='vn')
@frontend.route('/leaderboard/clans/<mode>/<sort>/<mods>') # GET
async def c_leaderboard(mode, sort, mods):
    return await render_template('clans/c-leaderboard.html', mode=mode, sort=sort, mods=mods)

@frontend.route("/clans/create")
async def create_clan():
    return await render_template('clans/create.html')

@frontend.route("/clans/info")
async def clan_info():
    return await render_template('clans/claninfo.html')

@frontend.route("/clans/create", methods=['POST'])
async def cc_post():
    if not 'authenticated' in session:
        return await flash('error', f'Hey! You need to login to create a clan.', 'login')

    # check if they in clan already
    e = await glob.db.fetch("SELECT clan_id FROM users WHERE id = %s", session["user_data"]["id"])
    if int(e['clan_id']) != 0:
        return await flash('error', 'Hey! You are already in a clan. Please leave your current clan to create your own!', 'home')

    form = await request.form
    name = form.get('c_name')
    tag = form.get('c_tag')
    desc = form.get('description')

    clan_rgx = re.compile(r'^[\w \[\]-]{2,15}$')
    tag_rgx = re.compile(r'^[\w \[\]-]{1,6}$')
    if not clan_rgx.match(name):
        return await flash('error', 'Invalid clan name syntax.', 'clans/create')

    if '_' in name and ' ' in name:
        return await flash('error', 'Clan names may contain "_" or " ", but not both.', 'clans/create')

    if await glob.db.fetch('SELECT 1 FROM clans WHERE name = %s', name):
        return await flash('error', 'Clan name already taken by another clan.', 'clans/create')

    if not tag_rgx.match(tag):
        return await flash('error', 'Invalid clantag syntax.', 'clans/create')

    if '_' in tag and ' ' in tag:
        return await flash('error', 'Clan tags may contain "_" or " ", but not both.', 'clans/create')

    if await glob.db.fetch('SELECT 1 FROM clans WHERE tag = %s', tag):
        return await flash('error', 'Clan tags already taken by another clan.', 'clans/create')

    await glob.db.execute("INSERT INTO clans (name, tag, owner, created_at, description) VALUES (%s, %s, %s, UNIX_TIMESTAMP(), %s)", [name, tag, session["user_data"]["id"], desc])
    a = await glob.db.fetch("SELECT id FROM clans WHERE name = %s", name)
    clanid = a['id']
    await glob.db.execute("UPDATE users SET clan_id = %s WHERE id = %s", [clanid, session["user_data"]["id"]])
    await glob.db.execute("UPDATE users SET clan_rank = 3 WHERE id = %s", session["user_data"]["id"])
    return await flash('success', 'Clan created!', 'home')

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
        'SELECT id, name, priv, pw_bcrypt, email, silence_end '
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
        'email': user_info['email'],
        'silence_end': user_info['silence_end'],
        'is_staff': user_info['priv'] & Privileges.Staff,
        'is_donator': user_info['priv'] & Privileges.Donator,
        'key': user_info['priv'] & Privileges.Donator or user_info['priv'] & Privileges.Staff or user_info['priv'] & Privileges.Nominator

    }

    if glob.config.debug:
        login_time = (time.time_ns() - login_time) / 1e6
        log(f'Login took {login_time:.2f}ms!', Ansi.LYELLOW)

    # authentication successful; redirect home
    return await flash('success', f'Hey! Welcome back {username}!', 'home')

""" registration """
@frontend.route('/register') # GET
async def register():
    # if authenticated; redirect home
    if 'authenticated' in session:
        return await flash('error', f'Hey You\'re already registered and logged in {session["user_data"]["name"]}!', 'home')

    return await render_template('register.html', ckey=glob.config.hcaptcha_sitekey, captcha=glob.config.captcha, keys=glob.config.keys)
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

    if glob.config.captcha:
        token = form.get('h-captcha-response')
        data = { 'secret': glob.config.hcaptcha_key, 'response': token }
        async with aiohttp.ClientSession() as sessionn:
            async with sessionn.post('https://hcaptcha.com/siteverify', data=data) as ses:
                res = await ses.json()
                success = res['success']
    else:
        success = True

    if success:
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

        if glob.config.keys:
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
        if not 8 <= len(pw_txt) <= 32:
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
                '(name, safe_name, email, pw_bcrypt, creation_time, latest_activity, verif) '
                'VALUES (%s, %s, %s, %s, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), 1)',
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
        if glob.config.keys:
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
        await webhook.post()
        return await render_template('verify.html')
    else:
        return await flash('error', 'Please complete the captcha and ensure you did so correctly!', 'register')

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

""" docs """
@frontend.route('/docs')
async def docs():
    return await render_template('docs/home.html')
