import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/student/list")
async def get_student_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, no AS stu_no, name AS stu_name, gender, enrolled FROM student
        """)
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")