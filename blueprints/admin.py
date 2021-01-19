# -*- coding: utf-8 -*-

from quart import Blueprint, render_template
from cmyui import log, Ansi

from objects import glob

__all__ = ()

admin = Blueprint('admin', __name__)

""" admin home """
@admin.route('/dashboard')
@admin.route('/home')
@admin.route('/')
async def home():
    return await render_template('admin/home.html')
