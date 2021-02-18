# -*- coding: utf-8 -*-

from cmyui import log, Ansi
from quart import render_template

from objects import glob

async def flash(status, msg, template):
    """ Flashes a success/error message on a specified template. """
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

async def fetch_geoloc(ip: str) -> str:
    """ Fetches the country code corresponding to an IP. """
    url = f'http://ip-api.com/line/{ip}'
    
    async with glob.http.get(url) as resp:
        if not resp or resp.status != 200:
            if glob.config.debug:
                log('Failed to get geoloc data: request failed.', Ansi.LRED)
            return 'xx'
        status, *lines = (await resp.text()).split('\n')
        if status != 'success':
            if glob.config.debug:
                log(f'Failed to get geoloc data: {lines[0]}.', Ansi.LRED)
            return 'xx'
        return lines[1].lower()