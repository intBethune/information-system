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

@web_routes.post("/api/course")
async def new_student(request):
    course = await request.json()
   
    with db_block() as db:
        db.execute("""
        INSERT INTO course (no, name, starttime, place)
        VALUES(%(cur_no)s, %(cur_name)s, %(cur_sta)s, %(cur_pla)s) RETURNING sn;
        """, course)
        record = db.fetch_first()

        course["cur_sn"] = record.sn
    

    return web.Response(text=json_dumps(course), content_type="application/json")

@web_routes.put("/api/course/{cur_sn:\d+}")
async def update_student(request):
    cur_sn = request.match_info.get("cur_sn")

    course = await request.json()
  

    course["cur_sn"] = cur_sn

    with db_block() as db:
        db.execute("""
        UPDATE course SET
            no=%(cur_no)s, name=%(cur_name)s, starttime=%(cur_sta)s, place=%(cur_pla)s
        WHERE sn=%(cur_sn)s;
        """, course)

    return web.Response(text=json_dumps(course), content_type="application/json")



@web_routes.delete("/api/course/{cur_sn:\d+}")
async def delete_student(request):
    cur_sn = request.match_info.get("cur_sn")

    with db_block() as db:
        db.execute("""
        DELETE FROM course WHERE sn=%(cur_sn)s;
        """, dict(cur_sn=cur_sn))

    return web.Response(text="", content_type="text/plain")
