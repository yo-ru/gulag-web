import orjson
from quart import Blueprint, render_template, request
from objects import glob

api = Blueprint("api", __name__)

# api "/get_leaderboard"
@api.route("/get_leaderboard")
async def get_leaderboard():
    # grabbing some args from frontend
    mode = request.args.get("m", type=str)
    mods = request.args.get("v", type=str)
    country = request.args.get("c", type=str)
    sort = request.args.get("s", type=str)

    if not mode and not mods and not sort:
        return (b"Must provide either mode or mods and sort by!")

    """ ROW_NUMBER() OVER () ?
    that's counting for pagination : )
    like i++ or data = data + 1
    """

    if country:
        res = await glob.db.fetchall(
            f"SELECT ROW_NUMBER() OVER () AS id, users.id AS userid, users.name AS username, users.country, tscore_{mods}_{mode} AS tscore, "
            f"rscore_{mods}_{mode} AS rscore, pp_{mods}_{mode} AS pp, plays_{mods}_{mode} AS plays, playtime_{mods}_{mode} AS playtime, "
            f"acc_{mods}_{mode} AS acc, maxcombo_{mods}_{mode} AS maxcombo FROM stats "
            f"JOIN users ON stats.id = users.id "
            f"WHERE pp_{mods}_{mode} > 1 AND users.country = '{country}' "
            f"ORDER BY stats.{sort}_{mods}_{mode} DESC"
        )
    else:
        res = await glob.db.fetchall(
            f"SELECT ROW_NUMBER() OVER () AS id, users.id AS userid, users.name AS username, users.country, tscore_{mods}_{mode} AS tscore, "
            f"rscore_{mods}_{mode} AS rscore, pp_{mods}_{mode} AS pp, plays_{mods}_{mode} AS plays, playtime_{mods}_{mode} AS playtime, "
            f"acc_{mods}_{mode} AS acc, maxcombo_{mods}_{mode} AS maxcombo FROM stats "
            f"JOIN users ON stats.id = users.id "
            f"WHERE pp_{mods}_{mode} > 1"
            f"ORDER BY stats.{sort}_{mods}_{mode} DESC"
        )

    return orjson.dumps(res) if res else b"{}"