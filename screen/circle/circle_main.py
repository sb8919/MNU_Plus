from flask import Blueprint, render_template, request
import dbcl
import datetime

circle_main_bp = Blueprint("circle_main", __name__)
circledb = dbcl.DBconnector('CIRCLE')

@circle_main_bp.route("/circle") #orion.mokpo.ac.kr:8486/circle
def circle():
    sql = '''SELECT 
            cl.circle_name, 
            cl.circle_category, 
            cl.circle_text, 
            cl.circle_logo_url,
            CASE 
                WHEN cd.recruit_endday > CURDATE() THEN '모집중'
                ELSE '모집마감'
            END AS recruit_status
        FROM 
            Circle_List cl
        LEFT OUTER JOIN 
            Circle_details cd ON cl.circle_name = cd.circle_name;
'''
    circle_list = circledb.fetch_all(sql)
    circle_ct_id={"문화/예술/공연":'th1',"봉사/사회활동":'th2',"학술/교양":'th3',"창업/취업":'th4',"어학":'th5',"체육":'th6',"친목":'th7',"기타":'th8'}
    return render_template('circle/circle.html', circle_data=circle_list, circle_ct_id=circle_ct_id)

@circle_main_bp.route("/circle/detail")
def circle_detail():
    circle_name=request.args.get("circle_name")
    circle_ref_sql = "SELECT * FROM Circle_details WHERE circle_name ='"+str(circle_name)+"';"
    circle_ref_data = circledb.fetch_all(circle_ref_sql)
    return render_template('circle/circle_detail.html',circle_ref_data = circle_ref_data[0])
    
@circle_main_bp.route("/circle_sign")
def circle_sign():
    return render_template('circle/circle_sign.html')

@circle_main_bp.route("/circle_sign_intro")
def circle_sign_intro():
    return render_template('circle/circle_sign_intro.html')

@circle_main_bp.route("/circle_detail_test")
def circle_detail2():
    return render_template('circle/circle_detail.html')
