# -*- coding: utf-8 -*-

import bcrypt
import hashlib
import re
from quart import Blueprint, render_template, redirect, request, flash
from cmyui import log, Ansi

from objects import glob

__all__ = ()

frontend = Blueprint('frontend', __name__)

""" home """
@frontend.route('/home') # GET
@frontend.route('/')
async def home():
    return await render_template('home.html')

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
    return await render_template('login.html')
@frontend.route('/login', methods=['POST']) # POST
async def login_post():
    # get form data (username, password)
    form = await request.form
    username = form.get('username')
    pw_md5 = hashlib.md5(form.get('password').encode()).hexdigest().encode()

    # check if account exists
    user_info = await glob.db.fetch(
        'SELECT id, name, priv, pw_bcrypt, silence_end '
        'FROM users WHERE safe_name = %s',
        [username.replace(' ', '_').lower()]
    )

    # the second part of this if statement exists because if we try to login with Aika
    # and compare our password input against the database it will fail because the 
    # hash saved in the database is invalid.
    if not user_info or user_info['id'] == 1:
        if glob.config.debug: log(f'Login failed. {username} does not exist.', Ansi.LRED) # debug
        return await flash('Account does not exist.', 'login')

    bcrypt_cache = glob.cache['bcrypt']
    pw_bcrypt = user_info['pw_bcrypt'].encode()
    user_info['pw_bcrypt'] = pw_bcrypt

    # check credentials (password) against db
    # intentionally slow, will cache to speed up
    # TODO: sessions and redirect
    if pw_bcrypt in bcrypt_cache:
        if pw_md5 != bcrypt_cache[pw_bcrypt]: # ~0.1ms
            if glob.config.debug: log(f'Login failed. Password for {username} is incorrect.', Ansi.LRED) # debug
            return await flash('Password is incorrect.', 'login')
    else: # ~200ms
        if not bcrypt.checkpw(pw_md5, pw_bcrypt):
            if glob.config.debug: log(f'Login failed. Password for {username} is incorrect.', Ansi.LRED) # debug
            return await flash('Password is incorrect.', 'login')
            
        # login success. cache password for next login
        bcrypt_cache[pw_bcrypt] = pw_md5
    
    # user not verified render verify page
    if user_info["priv"] == 1:
        if glob.config.debug: log(f'Login failed. {username} is not verified!', Ansi.LRED) # debug
        return await render_template('verify.html')

    # login successful
    if glob.config.debug: log(f'Login successful! {username} is now logged in.', Ansi.LGREEN) # debug
    return b'login successful.'

""" register """
@frontend.route('/register') # GET
async def register():
    return await render_template('register.html')
@frontend.route('/register', methods=['POST']) # POST
async def register_post():
    # get form data (username, email, password)
    form = await request.form
    username = form.get('username')
    safe_name = username.replace(' ', '_').lower()
    email = form.get('email')
    pw_md5 = hashlib.md5(form.get('password').encode()).hexdigest().encode()

    pw_bcrypt = bcrypt.hashpw(pw_md5, bcrypt.gensalt())
    glob.cache['bcrypt'][pw_bcrypt] = pw_md5 # cache result for login

    # check if username exists
    user_info = await glob.db.fetch(
        'SELECT * FROM users WHERE safe_name = %s',
        [safe_name]
    )

    if user_info['safe_name'] == safe_name:
        return await flash('Username is already in use!', 'register')
    elif not re.match(r'[A-Za-z0-9]+', username): 
        return await flash('Username must contain only characters and numbers!', 'register')
    elif user_info['email'] == email:
        return await flash('Email is already in use!', 'register')
    elif not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
        return await flash('Please input a valid email address!', 'register')
    elif not username or not pw_md5 or not email:
        return await flash('Please fill out the form!', 'register')

    # add to users table
    user_id = await glob.db.execute(
        'INSERT INTO users '
        '(name, safe_name, email, pw_bcrypt, creation_time, latest_activity) '
        'VALUES (%s, %s, %s, %s, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())',
        [username, [username.replace(' ', '_').lower()], email, pw_bcrypt]
    )

    # add to stats table
    await glob.db.execute(
        'INSERT INTO stats '
        '(id) VALUES (%s)',
        [user_id]
    )

    if glob.config.debug: log(f'Registration successful! {username} is now registered. Awaiting verification...', Ansi.LGREEN) # debug

    # user has successfully registered.
    return await render_template('verify.html')

""" asserts (for if got error) """
def flash(msg, template):
    return render_template(f"{template}.html", flash=msg)

""" rules """
@frontend.route('/rules') # GET
async def rules():
    return await render_template('rules.html')

""" discord redirect """
@frontend.route('/discord') # GET
async def discord():
    return redirect(glob.config.discord_server)
