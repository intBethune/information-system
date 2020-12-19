from urllib.parse import urlencode
from aiohttp.web_request import Request
import psycopg2.errors
from aiohttp import web

from .config import db_block, render_html, web_routes


@web_routes.post('/action/cg/')
async def  course_grade_action(request):
    cou_sn = await request.post()
    #print(cou_sn)
    with db_block() as db:  
        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE cou_sn = %(cou_sn)s;
        """,dict(cou_sn=cou_sn))

        items = list(db)
        print(items)   
    return render_html(request, 'course_grade_list2.html',
                       items=items)



@web_routes.post('/action/sg/')
async def  student_grade_action(request):
    stu_sn = await request.post()
    #print(stu_sn)
    with db_block() as db:  
        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
           INNER JOIN student as s ON g.stu_sn = s.sn
           INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s;
        """,dict(stu_sn=stu_sn))

        items = list(db)
        print(items)   
    return render_html(request, 'student_grade_list2.html',
                    items=items)

   
                      
