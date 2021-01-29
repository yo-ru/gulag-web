# -*- coding: utf-8 -*-

import orjson
from quart import Blueprint, request
from cmyui import log, Ansi
from enum import IntEnum

from objects import glob
from objects.utils import convert_mode_int, get_safe_name

__all__ = ()

api = Blueprint('api', __name__)

""" valid modes, mods, sorts """
valid_modes = frozenset({'std', 'taiko', 'catch', 'mania'})
valid_mods = frozenset({'vn', 'rx', 'ap'})
valid_sorts = frozenset({'tscore', 'rscore', 'pp', 'plays',
                        'playtime', 'acc', 'maxcombo'})

""" /get_leaderboard """
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

    if glob.config.debug:
        log(' '.join(q), Ansi.LGREEN)
    res = await glob.db.fetchall(' '.join(q), args)
    return orjson.dumps(res) if res else b'{}'

""" /get_user """
@api.route('/get_user') # GET
async def get_user():
    # get request args
    id = request.args.get('id', type=int)
    name = request.args.get('name', type=str)

    # check if required parameters are met
    if not name and not id:
        return b'missing parameters! (id or name)'

    # fetch user info and stats
    # user info
    q = ['SELECT u.id user_id, u.name username, u.safe_name username_safe, u.country, u.priv privileges, '
        'u.silence_end, u.donor_end, u.creation_time, u.latest_activity, u.clan_id, u.clan_rank, '

        # total score
        'tscore_vn_std, tscore_vn_taiko, tscore_vn_catch, tscore_vn_mania, '
        'tscore_rx_std, tscore_rx_taiko, tscore_rx_catch, '
        'tscore_ap_std, '

        # ranked score
        'rscore_vn_std, rscore_vn_taiko, rscore_vn_catch, rscore_vn_mania, '
        'rscore_rx_std, rscore_rx_taiko, rscore_rx_catch, '
        'rscore_ap_std, '

        # pp
        'pp_vn_std, pp_vn_taiko, pp_vn_catch, pp_vn_mania, '
        'pp_rx_std, pp_rx_taiko, pp_rx_catch, '
        'pp_ap_std, '

        # plays
        'plays_vn_std, plays_vn_taiko, plays_vn_catch, plays_vn_mania, '
        'plays_rx_std, plays_rx_taiko, plays_rx_catch, '
        'plays_ap_std, '

        # playtime
        'playtime_vn_std, playtime_vn_taiko, playtime_vn_catch, playtime_vn_mania, '
        'playtime_rx_std, playtime_rx_taiko, playtime_rx_catch, '
        'playtime_ap_std, '

        # accuracy
        'acc_vn_std, acc_vn_taiko, acc_vn_catch, acc_vn_mania, '
        'acc_rx_std, acc_rx_taiko, acc_rx_catch, '
        'acc_ap_std, '

        # maximum combo
        'maxcombo_vn_std, maxcombo_vn_taiko, maxcombo_vn_catch, maxcombo_vn_mania, '
        'maxcombo_rx_std, maxcombo_rx_taiko, maxcombo_rx_catch, '
        'maxcombo_ap_std, '

        # ranks
        'rank_vn_std, rank_vn_taiko, rank_vn_catch, rank_vn_mania, '
        'rank_rx_std, rank_rx_taiko, rank_rx_catch, '
        'rank_ap_std, '

        # country ranks
        'crank_vn_std, crank_vn_taiko, crank_vn_catch, crank_vn_mania, '
        'crank_rx_std, crank_rx_taiko, crank_rx_catch, '
        'crank_ap_std '


        # join users
        'FROM stats JOIN users u ON stats.id = u.id']

    # argumnts
    args = []

    # append request arguments (id or name)
    if id:
        q.append('WHERE u.id = %s')
        args.append(id)
    elif name:
        q.append('WHERE u.safe_name = %s')
        args.append(get_safe_name(name))

    if glob.config.debug:
        log(' '.join(q), Ansi.LGREEN)
    res = await glob.db.fetchall(' '.join(q), args)
    return orjson.dumps(res) if res else b'{}'

""" /get_scores """
@api.route('/get_scores') # GET
async def get_scores():
    # get request args
    id = request.args.get('id', type=int)
    mode = request.args.get('mode', type=str)
    mods = request.args.get('mods', type=str)
    sort = request.args.get('sort', type=str)
    limit = request.args.get('limit', type=int)

    # check if required parameters are met
    if not id:
        return b'missing parameters! (id)'

    if sort == 'recent':
        sort = 'id'
    elif sort == 'best':
        sort = 'pp'
    else:
        return b'invalid sort! (recent or best)'

    if mods not in valid_mods:
        return b'invalid mods! (vn, rx, ap)'

    if mode == 'std':
        mode = 0
    elif mode == 'taiko':
        mode = 1
    elif mode == 'catch':
        mode = 2
    elif mode == 'mania':
        mode = 3
    else:
        return b'wrong mode type! (std, taiko, catch, mania)'

    if not limit:
        limit = 5

    # fetch scores
    q = [f'SELECT scores_{mods}.*, maps.* '
        f'FROM scores_{mods} JOIN maps ON scores_{mods}.map_md5 = maps.md5']

    # argumnts
    args = []

    q.append(f'WHERE scores_{mods}.userid = %s '
            f'AND scores_{mods}.mode = {mode} '
            f'AND maps.status = 2')
    if sort == 'pp':
        q.append(f'AND scores_{mods}.status = 2')
    q.append(f'ORDER BY scores_{mods}.{sort} DESC '
            f'LIMIT {limit}')
    args.append(id)

    if glob.config.debug:
        log(' '.join(q), Ansi.LGREEN)
    res = await glob.db.fetchall(' '.join(q), args)
    return orjson.dumps(res) if res else b'{}'

""" /get_most_beatmaps """
@api.route('/get_most_beatmaps') # GET
async def get_most_beatmaps():
    # get request args
    id = request.args.get('id', type=int)
    mode = request.args.get('mode', type=str)
    mods = request.args.get('mods', type=str)
    limit = request.args.get('limit', type=int)

    # check if required parameters are met
    if not id:
        return b'missing parameters! (id)'

    if mods not in valid_mods:
        return b'invalid mods! (vn, rx, ap)'

    if mode == 'std':
        mode = 0
    elif mode == 'taiko':
        mode = 1
    elif mode == 'catch':
        mode = 2
    elif mode == 'mania':
        mode = 3
    else:
        return b'wrong mode type! (std, taiko, catch, mania)'

    if not limit:
        limit = 5

    # fetch scores
    q = [f'SELECT scores_{mods}.mode, scores_{mods}.map_md5, maps.artist, maps.title, maps.set_id, maps.creator, COUNT(*) AS `count` '
        f'FROM scores_{mods} JOIN maps ON scores_{mods}.map_md5 = maps.md5']

    # argumnts
    args = []

    q.append(f'WHERE userid = %s AND scores_{mods}.mode = {mode} GROUP BY map_md5')
    q.append(f'ORDER BY COUNT DESC '
            f'LIMIT {limit}')
    args.append(id)

    if glob.config.debug:
        log(' '.join(q), Ansi.LGREEN)
    res = await glob.db.fetchall(' '.join(q), args)
    return orjson.dumps(res) if res else b'{}'

@api.route('/get_grade') # GET
async def get_grade():
    # get request args
    id = request.args.get('id', type=int)
    mode = request.args.get('mode', type=str)
    mods = request.args.get('mods', type=str)

    # check if required parameters are met
    if not id:
        return b'missing parameters! (id)'

    if mods not in valid_mods:
        return b'invalid mods! (vn, rx, ap)'

    if mode in valid_modes:
        mode = convert_mode_int(mode)
    else:
        return b'wrong mode type! (std, taiko, catch, mania)'

    grades = ['xh','ss','sh','s','a']

    # fetch grades
    q = [f'SELECT userid,']

    for grade in grades:
        if grade == 'a':
            q.append(f'(SELECT COUNT(id) FROM scores_{mods} WHERE grade="{grade}" and mode = {mode}) as {grade}')
            break
        q.append(f'(SELECT COUNT(id) FROM scores_{mods} WHERE grade="{grade}" and mode = {mode}) as {grade},')

    # argumnts
    args = []

    q.append(f'FROM scores_{mods}')
    q.append(f'WHERE userid = %s AND mode = {mode}')
    args.append(id)

    if glob.config.debug:
        log(' '.join(q), Ansi.LGREEN)
    res = await glob.db.fetch(' '.join(q), args)
    print(res)
    return orjson.dumps(res) if res else b'{}'

@api.route('/get_online')
async def api_get_online():
    res = await glob.db.fetch('SELECT online FROM server_stats')
    online = {"online": res['online']}
    return orjson.dumps(online)
