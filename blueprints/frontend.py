# -*- coding: utf-8 -*-

import bcrypt
import hashlib
import re
from quart import Blueprint, render_template, request, flash
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
@frontend.route('/leaderboard')
async def leaderboard():
    return await render_template('leaderboard.html')

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
        return b'login failed. account does not exist.'

    bcrypt_cache = glob.cache['bcrypt']
    pw_bcrypt = user_info['pw_bcrypt'].encode()
    user_info['pw_bcrypt'] = pw_bcrypt

    # check credentials against db
    # intentionally slow, will cache to speed up
    # TODO: sessions and redirect
    if pw_bcrypt in bcrypt_cache:
        if pw_md5 != bcrypt_cache[pw_bcrypt]: # ~0.1ms
            return b'login failed. password is incorrect.'
    else: # ~200ms
        if not bcrypt.checkpw(pw_md5, pw_bcrypt):
            return b'login failed. password is incorrect.'
            
        # login success. cache password for next login
        bcrypt_cache[pw_bcrypt] = pw_md5
    
    # is this user verify?
    if user_info["priv"] == 1:
        return await flash('go verify','verify')

    # login successful
    return b'login successful.'

""" register """
@frontend.route('/register') # GET
async def register():
    return await render_template('register.html')
@frontend.route('/register', methods=['POST']) # POST
async def register_post():
    # get form data (username, password)
    form = await request.form
    username = form.get('username')
    email = form.get('email')

    pw_md5 = hashlib.md5(form.get('password').encode()).hexdigest().encode()
    pw_bcrypt = bcrypt.hashpw(pw_md5, bcrypt.gensalt())
    glob.cache['bcrypt'][pw_bcrypt] = pw_md5 # cache result for login

    # check if username exists
    user_info = await glob.db.fetch(
        'SELECT * FROM users WHERE safe_name = %s',
        [username.replace(' ', '_').lower()]
    )

    if user_info:
        return await flash('username exist.','register')
    elif not re.match(r'[A-Za-z0-9]+', username): 
        return await flash('Username must contain only characters and numbers !','register')
    elif not username or not pw_md5 or not email:
        return await flash('Please fill out the form !','register')

    # add to `users` table.
    user_id = await glob.db.execute(
        'INSERT INTO users '
        '(name, safe_name, email, pw_bcrypt, creation_time, latest_activity) '
        'VALUES (%s, %s, %s, %s, UNIX_TIMESTAMP(), UNIX_TIMESTAMP())',
        [username, [username.replace(' ', '_').lower()], email, pw_bcrypt]
    )

    # add to `stats` table.
    await glob.db.execute(
        'INSERT INTO stats '
        '(id) VALUES (%s)',
        [user_id]
    )

    msg = "wow you're registred in gulag server !!!"
    log(f'<{username} ({user_id})> has registered in gulag-web!', Ansi.LGREEN)

    return await render_template(f"verify.html", msg=msg)
@frontend.route('/verify')
async def verify():
    return await render_template('verify.html')

""" asserts """
async def flash(msg,template):
    return await render_template(f"{template}.html", flash=msg)
