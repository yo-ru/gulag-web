from quart import Blueprint, render_template

blueprint = Blueprint('home', __name__)

@blueprint.route('/home')
@blueprint.route('/')
async def home():
    return await render_template('home.html')