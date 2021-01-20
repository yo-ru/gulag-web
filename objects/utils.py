# -*- coding: utf-8 -*-

from quart import render_template

async def flash(status, msg, template):
    """ Flashes a success/error snackbar message on a specified template. """
    return await render_template(f'{template}.html', flash=msg, status=status)