from cmyui import (AsyncSQLPoolWrapper, Version, Ansi, log)
from quart import Quart

from objects import glob

""" Application """
app = Quart(__name__)

""" Globals """
# Database
@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPoolWrapper()
    await glob.db.connect(glob.config.mysql)
    log("Connected to MySQL!", Ansi.LGREEN)

# Version
@app.before_serving
@app.template_global("appVersion")
def app_version() -> str:
    return Version(0, 1, 0)

# App Name
@app.before_serving
@app.template_global("appName")
def app_name() -> str:
    return glob.config.app_name

""" Blueprints """
# Frontend
from blueprints.frontend import frontend
app.register_blueprint(frontend)

# Backend
from blueprints.backend import backend
app.register_blueprint(backend, url_prefix='/admin')

# API
from blueprints.api import api
app.register_blueprint(api, url_prefix='/api')


""" Start Application """
if __name__ == "__main__":
    app.run(debug=True)
