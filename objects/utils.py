# -*- coding: utf-8 -*-

from quart import render_template

async def flash(status, msg, template):
    """ Flashes a success/error snackbar message on a specified template. """
    return await render_template(f'{template}.html', flash=msg, status=status)

def get_safe_name(name: str) -> str:
    """ Returns the safe version of a username. """
    return name.lower().replace(' ', '_')

def convert_mode_int(mode: str) -> int:
    """ Converts mode (str) to mode (int). """
    if mode == 'std':
        return 0
    elif mode == 'taiko':
        return 1
    elif mode == 'catch':
        return 2
    elif mode == 'mania':
        return 3
    else:
        return b'wrong mode type! (std, taiko, catch, mania)'
    
def convert_mode_str(mode: int) -> str:
    """ Converts mode (int) to mode (str). """
    if mode == 0:
        return 'std'
    elif mode == 0:
        return 'taiko'
    elif mode == 0:
        return 'catch'
    elif mode == 0:
        return 'mania'
    else:
        return b'wrong mode type! (0, 1, 2, 3)'
