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
# Home
from home import blueprint
app.register_blueprint(blueprint)

# Leaderboards
from leaderboards import blueprint
app.register_blueprint(blueprint)


""" Start Application """
if __name__ == "__main__":
    app.run()
