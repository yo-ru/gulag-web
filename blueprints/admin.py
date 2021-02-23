# -*- coding: utf-8 -*-

import timeago
import datetime
from cmyui import log, Ansi
from quart import Blueprint, render_template, session, redirect

from objects import glob
from objects.privileges import Privileges
from objects.utils import flash

__all__ = ()

admin = Blueprint('admin', __name__)

"""
home - the home page of the admin panel.
"""
@admin.route('/dashboard')
@admin.route('/home')
@admin.route('/')
async def home():

    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access the admin panel!', 'login')
    
    # if authenticated but not staff; render home
    elif not session['user_data']['is_staff']:
        return await flash('error', f'Hey! You don\'t have enough clearance to access the admin panel {session["user_data"]["name"]}!', 'home')
    
    # fetch data from database
    dash_data = await glob.db.fetch('SELECT COUNT(id) count, '
    '(SELECT name FROM users ORDER BY id DESC LIMIT 1) lastest_user, '
    '(SELECT COUNT(id) FROM users WHERE NOT priv & 1) banned FROM users')
    recent_users = await glob.db.fetchall('SELECT * FROM users ORDER BY id DESC LIMIT 5')
    recent_scores = await glob.db.fetchall('SELECT scores_vn.*, maps.artist, maps.title, maps.set_id, '
    'maps.creator, maps.version FROM scores_vn JOIN maps ON scores_vn.map_md5 = maps.md5 '
    'ORDER BY scores_vn.id DESC LIMIT 5')

    return await render_template('admin/home.html', dashdata=dash_data, recentusers=recent_users, recentscores=recent_scores, 
                                datetime=datetime, timeago=timeago)
