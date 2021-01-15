# -*- coding: utf-8 -*-

from quart import Blueprint

__all__ = ()

admin = Blueprint('admin', __name__)

""" admin home """
@admin.route('/home')
@admin.route('/')
async def home():
    return b'admin not finished.'
