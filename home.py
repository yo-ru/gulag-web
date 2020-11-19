from quart import Blueprint, render_template

from objects import glob

blueprint = Blueprint('home', __name__)

@blueprint.route('/home')
@blueprint.route('/')
async def home():
    return await render_template('home.html')