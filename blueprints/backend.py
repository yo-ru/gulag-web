from quart import Blueprint, render_template

from objects import glob

backend = Blueprint('backend', __name__)

@backend.route('/home')
@backend.route('/')
async def home():
    return "a"