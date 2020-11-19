# Imports
from cmyui import Version
from quart import Quart

# App
app = Quart(__name__)

""" Globals """
# Version
@app.template_global('appVersion')
def app_version() -> str:
    return Version(0, 1, 0)

# Instance Name
@app.template_global('appName')
def app_name() -> str:
    return "gulag-web"

""" Blueprints """
# Home
from home import blueprint
app.register_blueprint(blueprint)

# Leaderboards
from leaderboards import blueprint
app.register_blueprint(blueprint)


""" Start Applicaiton """
if __name__ == '__main__':
    app.run()
