# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, session, redirect
from cmyui import log, Ansi

from objects import glob
from objects.privileges import Privileges

__all__ = ()

admin = Blueprint('admin', __name__)

""" admin home """
@admin.route('/dashboard')
@admin.route('/home')
@admin.route('/')
async def home():

    # if user is not authenticated or they're not a staff member; redirect home
    if not 'authenticated' in session or not session['user_data']['priv'] & Privileges.Staff:
        return redirect('/home')

    return await render_template('admin/home.html')
