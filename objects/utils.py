# -*- coding: utf-8 -*-

from quart import render_template

async def flash(status, msg, template):
    """ Flashes a success/error snackbar message on a specified template. """
    return await render_template(f'{template}.html', flash=msg, status=status)

def get_safe_name(name: str) -> str:
    """ Returns the safe version of a username. """
    return name.lower().replace(' ', '_')