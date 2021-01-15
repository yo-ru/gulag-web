# -*- coding: utf-8 -*-

import orjson
from quart import Blueprint, request
from objects import glob

__all__ = ()

api = Blueprint('api', __name__)


""" /get_leaderboard """
valid_modes = frozenset({'std', 'taiko', 'catch', 'mania'})
valid_mods = frozenset({'vn', 'rx', 'ap'})
valid_sorts = frozenset({'tscore', 'rscore', 'pp', 'plays',
                        'playtime', 'acc', 'maxcombo'})
@api.route('/get_leaderboard') # GET
async def get_leaderboard():
    mode = request.args.get('mode', default='std', type=str)
    mods = request.args.get('mods', default='vn', type=str)
    sort_by = request.args.get('sort', default='pp', type=str)
    country = request.args.get('country', default=None, type=str)
    page = request.args.get('page', default=0, type=int)

    if mode not in valid_modes:
        return b'invalid mode! (std, taiko, catch, mania)'

    if mods not in valid_mods:
        return b'invalid mods! (vn, rx, ap)'

    if country is not None and len(country) != 2:
        return b'invalid country!'

    if sort_by not in valid_sorts:
        return b'invalid sort param!'

    q = ['SELECT u.id user_id, u.name username, '
         'u.country, tscore_{0}_{1} tscore, '
         'rscore_{0}_{1} rscore, pp_{0}_{1} pp, '
         'plays_{0}_{1} plays, playtime_{0}_{1} playtime, '
         'acc_{0}_{1} acc, maxcombo_{0}_{1} maxcombo FROM stats '
         'JOIN users u ON stats.id = u.id '
         'WHERE pp_{0}_{1} > 0'.format(mods, mode)]

    args = []

    if country is not None:
        q.append('AND u.country = %s')
        args.append(country)

    # TODO: maybe cache total num of scores in the db to get a
    # rough estimate on what is a ridiculous page for a request?
    q.append(f'ORDER BY {sort_by}_{mods}_{mode} DESC '
             'LIMIT 50 OFFSET %s')
    args.append(page * 50)

    res = await glob.db.fetchall(' '.join(q), args)
    return orjson.dumps(res) if res else b'{}'
