import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/course/list")
async def get_student_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS cur_sn, no AS cur_no, name AS cur_name, starttime AS cur_sta, place AS cur_pla
        FROM course
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")