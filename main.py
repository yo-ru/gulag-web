#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import os
from quart import Quart
from cmyui import AsyncSQLPool, Version, Ansi, log

from objects import glob

__all__ = ()

app = Quart(__name__)
version = Version(0, 1, 0)

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

# import external blueprints & add to app
from blueprints.frontend import frontend
from blueprints.admin import admin
from blueprints.api import api
app.register_blueprint(frontend)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=glob.config.debug) # blocking call
