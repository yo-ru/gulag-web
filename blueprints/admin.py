from quart import Blueprint, render_template

from objects import glob

admin = Blueprint("admin", __name__)

# admin home
@admin.route("/home")
@admin.route("/")
async def home():
    return "admin"