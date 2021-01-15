import os
from cmyui import (AsyncSQLPool, Version, Ansi, log)
from quart import Quart

from objects import glob

""" Application """
app = Quart(__name__)

""" Globals """
# Database
@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)
    log("Connected to MySQL!", Ansi.LGREEN)

# Version
@app.before_serving
@app.template_global("appVersion")
def app_version() -> str:
    return Version(0, 1, 0)

# app name
@app.before_serving
@app.template_global("appName")
def app_name() -> str:
    return glob.config.app_name

# import external blueprints & add to app
from blueprints.frontend import frontend
app.register_blueprint(frontend)

# backend
from blueprints.admin import admin
app.register_blueprint(admin, url_prefix="/admin")

# api
from blueprints.api import api
app.register_blueprint(api, url_prefix="/api")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug=glob.config.debug) # blocking call
