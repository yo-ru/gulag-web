from quart import Blueprint, render_template

from objects import glob

frontend = Blueprint('frontend', __name__)

@frontend.route('/home')
@frontend.route('/')
async def home():
    return await render_template('home.html')