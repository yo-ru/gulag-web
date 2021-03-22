#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import quart.flask_patch # https://pgjones.gitlab.io/quart/how_to_guides/flask_extensions.html
import os
from quart import Quart, render_template, request
from cmyui import AsyncSQLPool, Version, Ansi, log

from objects import glob

__all__ = ()

app = Quart(__name__)
version = Version(0, 1, 9)

app.secret_key = glob.config.secret_key
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = True

@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)
    log('Connected to MySQL!', Ansi.LGREEN)

_version = repr(version)
@app.before_serving
@app.template_global()
def appVersion() -> str:
    return _version

_app_name = glob.config.app_name
@app.before_serving
@app.template_global()
def appName() -> str:
    return _app_name

_key = glob.config.keys
@app.before_serving
@app.template_global()
def key() -> str:
    return _key

_domain = glob.config.domain
@app.before_serving
@app.template_global()
def domain() -> str:
    return _domain

# Import external blueprints & add to app
from blueprints.frontend import frontend
from blueprints.admin import admin
from blueprints.api import api
app.register_blueprint(frontend)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

""" error 404 """
@app.errorhandler(404)
async def page_not_found(e):
    # note that we set the 404 status explicitly
    return await render_template('404.html'), 404

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=glob.config.debug) # blocking call
