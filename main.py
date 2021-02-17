#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

""" imports """
import os
import aiohttp
import orjson
from quart import Quart, render_template, request, flask_patch
from cmyui import AsyncSQLPool, Version, Ansi, log

from objects import glob

__all__ = ()

""" app """
app = Quart(__name__)

""" app version """
version = Version(0, 1, 0)

"""
secret key - used to secure session data.
the only semi-sensitive data we store in
the session is a user's email address.
i recommend using a 2048 character randomly
generated string that excludes escape characters.
"""
app.secret_key = glob.config.secret_key

""" connect to mysql """
@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)
    log('Connected to MySQL!', Ansi.LGREEN)

""" retrieve a client session for http connections """
@app.before_serving
async def http_conn() -> None:
    glob.http = aiohttp.ClientSession(json_serialize=orjson.dumps)
    log('Got our Client Session!', Ansi.LGREEN)

""" global templates """
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
_domain = glob.config.domain
@app.before_serving
@app.template_global()
def domain() -> str:
    return _domain

""" external blueprints """
from blueprints.frontend import frontend
from blueprints.admin import admin
from blueprints.api import api
app.register_blueprint(frontend)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

""" 404 error handler """
@app.errorhandler(404)
async def page_not_found(e):
    # NOTE: we set the 404 status explicitly
    return await render_template('404.html'), 404

""" run app """
if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=glob.config.debug) # blocking call
