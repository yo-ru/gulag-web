#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

""" imports """
import os
import orjson
import aiohttp
from quart import Quart, render_template, request, flask_patch, jsonify
from cmyui import AsyncSQLPool, Version, Ansi, log

from objects import glob

__all__ = ()

"""
app - our quart app pertaining to gulag-web.
"""
app = Quart(__name__)



"""
app version - current version of gulag-web.
"""
version = Version(0, 1, 0)



"""
secret key - used to secure session data.
the only semi-sensitive data we store in
the session is a user's email address.
i recommend using a 2048 character randomly
generated string that excludes escape characters.
"""
app.secret_key = glob.config.secret_key



"""
mysql - connect to mysql.
"""
@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)
    log('Connected to MySQL!', Ansi.LGREEN)



"""
clientsession - get our client session for http connections.
"""
@app.before_serving
async def http_conn() -> None:
    glob.http = aiohttp.ClientSession(json_serialize=orjson.dumps)
    log('Got our Client Session!', Ansi.LGREEN)



""" 
global templates - python variables used in template throughout gulag-web.
"""
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

_captcha_key = glob.config.hCaptcha_sitekey
@app.before_serving
@app.template_global()
def captchaKey() -> str:
    return _captcha_key

_domain = glob.config.domain
@app.before_serving
@app.template_global()
def domain() -> str:
    return _domain



"""
blueprints - modular code relating to separate sections of gulag-web.
"""
from blueprints.frontend import frontend
app.register_blueprint(frontend)

from blueprints.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

from blueprints.api import api
app.register_blueprint(api, url_prefix='/api')



"""
error handlers - handle certain http status codes.
"""
@app.errorhandler(404)
async def page_not_found(e):
    # NOTE: we set the 404 status explicitly
    return await render_template('404.html'), 404



"""
run app - run gulag-web.
"""
if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=glob.config.debug) # blocking call
