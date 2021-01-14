from quart import Blueprint, render_template

from objects import glob

frontend = Blueprint("frontend", __name__)

# frontend Home
@frontend.route('/home')
@frontend.route("/")
async def home():
    return await render_template("home.html")

@frontend.route("/login")
async def login():
    return await render_template("login.html")