# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, session, redirect
from cmyui import log, Ansi

from objects import glob
from objects.privileges import Privileges
from objects.utils import flash

__all__ = ()

admin = Blueprint('admin', __name__)

""" admin home """
@admin.route('/dashboard')
@admin.route('/home')
@admin.route('/')
async def home():

    # if not authenticated; render login
    if not 'authenticated' in session:
        return await flash('error', 'You must be logged in to access the admin panel!', 'login')
    
    # if authenticated but not staff; render home
    elif not session['user_data']['priv'] & Privileges.Staff:
        return await flash('error', f'Hey! You don\'t have enough clearance to access the admin panel {session["user_data"]["name"]}!', 'home')

    # TODO: admin panel
    NotImplemented

    return await render_template('admin/home.html')
