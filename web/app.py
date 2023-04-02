# -*- coding: utf-8 -*-
import socket
import dbcon
import os
import dbcl
from flask import Flask, session, redirect, url_for, jsonify, render_template, request, flash
from flask_login import LoginManager
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename

# 메인 코드
app = Flask(__name__)

app.secret_key = 'merjklwj34'

#DB pymysql=============================================================
circledb = dbcl.DBconnector('CIRCLE')
finddb = dbcl.DBconnector('FIND')
pagedb = dbcl.DBconnector('PAGE_INFO')
cardb = dbcl.DBconnector('CAR')
restdb = dbcl.DBconnector('REST')
programdb = dbcl.DBconnector('PROGRAM')
festivaldb = dbcl.DBconnector('FESTIVAL')


#Main==================================================================
#  섹터 : 메인화면 (인트로, 조회수 표시) 
#  작성일              작성자              내용
# 23.01.12            박상범              최초등록
#=======================================================================
@app.route("/")
def main_intro():
    #동아리 등록수 확인 쿼리
    circle_count_sql = "SELECT COUNT(*) FROM Circle_List;"
    circle_count = circledb.fetch_one(circle_count_sql)
    
    # 스터디 등록수 확인 쿼리
    find_count_sql = "SELECT COUNT(*) FROM Find_List;"
    find_count = finddb.fetch_one(find_count_sql)
    
    # 방문자수 업데이트 및 확인 쿼리
    page_update_count_sql = "UPDATE page_info SET PAGE_COUNT = (SELECT PAGE_COUNT FROM page_info) + 1 WHERE PAGE_COUNT > 0;"
    pagedb.save(page_update_count_sql)
    page_count_sql = "SELECT PAGE_COUNT FROM page_info;"
    page_count = pagedb.fetch_one(page_count_sql)
    return render_template('main/intro.html',circle_count = circle_count, find_count = find_count, page_count = page_count)

#circle================================================================
#  섹터 : 동아리 (동아리 리스트, 동아리 등록) 
#  작성일              작성자              내용
# 23.01.08            박상범              최초등록
#=======================================================================
@app.route("/circle") #orion.mokpo.ac.kr:8486/circle
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
#test
@app.route("/circle/detail")
def circle_detail():
    circle_name=request.args.get("circle_name")
    circle_ref_sql = "SELECT * FROM Circle_details WHERE circle_name ='"+str(circle_name)+"';"
    circle_ref_data = circledb.fetch_all(circle_ref_sql)
    return render_template('circle/circle_detail.html',circle_ref_data = circle_ref_data[0])
    
@app.route("/circle_sign")
def circle_sign():
    return render_template('circle/circle_sign.html')

@app.route("/circle_sign_intro")
def circle_sign_intro():
    return render_template('circle/circle_sign_intro.html')

@app.route("/circle_detail_test")
def circle_detail2():
    return render_template('circle/circle_detail.html')

# 동아리 등록 =====================================================================================
@app.route("/circle_sign_post", methods=['POST'])
def circle_sign_post():
    circle_name=request.form['circle_name']
    circle_category=request.form['circle_category']
    circle_short_intro=request.form['circle_short_intro']
    circle_logo_url=request.files['circle_logo_url']
    recruit_stday=request.form['recruit_stday']
    recruit_endday=request.form['recruit_endday']
    circle_detail_intro=request.form['circle_detail_intro']
    apply_process=request.form['apply_process']
    qualifications=request.form['qualifications']
    circle_recruit_url=request.form['circle_recruit_url']
    preferential=request.form['preferential']
    master_name=request.form['master_name']
    master_number=request.form['master_number']
    id = request.form['id']
    password=request.form['confirm_password']
    team_agree= bool(request.form.get('team_agree'))
    print(circle_logo_url)
    circle_logo_url.save('./static/circle_logo/'+circle_name+'.png')
    circle_insert_sql = "INSERT INTO Circle_details VALUES('"+circle_name+"','"+circle_category+"','"+circle_short_intro+"','"+('/circle_logo/'+circle_name+'.png')+"','"+recruit_stday+"','"+recruit_endday+"','"+circle_detail_intro+"','"+apply_process+"','"+qualifications+"','"+circle_recruit_url+"','"+preferential+"','"+master_name+"','"+master_number+"','"+id+"','"+password+"','"+str(team_agree)+"','"+str(datetime.today().strftime("%Y-%m-%d"))+"','"+'N'+"'"+');'
    user_data = circledb.insert(circle_insert_sql)
    return render_template('circle/circle_sign.html')
    
@app.route("/circle/manage/id_check", methods=['POST'])
def cm_id_check():
    id = request.form['id']
    sql = "SELECT EXISTS(SELECT * FROM user WHERE id='"+id+"');"
    id_result = circledb.fetch_one(sql)
    return jsonify({"id":id_result})

# 페이지 관리자 ============================================================
@app.route("/circle/manage/admin")
def cm_admin():
    sql = "SELECT * FROM user;"
    user_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/admin/admin.html',user_data = user_data)

@app.route("/circle/manage/admin/update", methods=['POST'])
def cm_admin_update():
    id=request.form['id']
    passwd=request.form['passwd']
    name=request.form['name']
    authority=request.form['authority']
    sql = "UPDATE user SET ID='"+id+"', pW='"+passwd+"', NAME='"+name+"', AUTHORITY='"+authority+"' WHERE id='"+id+"';"
    circledb.update(sql)
    return redirect('/circle/manage/admin')


# 동아리 마스터 ============================================================
@app.route("/circle/manage/circle_admin")
def cm_circle_admin():
    sql = "SELECT circle_name,circle_category,master_name,master_number,circle_short_intro,circle_logo_url,sign_date FROM Circle_details WHERE circle_approval = 'N';"
    circle_sign_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/cc_admin/cc_admin.html',circle_sign_data= circle_sign_data)

@app.route("/circle/manage/approve", methods=['POST'])
def cm_approve():
    circle_name=request.form['circle_name']
    circle_category=request.form['circle_category']
    master_name=request.form['master_name']
    sql = "UPDATE Circle_details SET circle_approval='Y' WHERE circle_name=('"+circle_name+"') and circle_category = ('" + circle_category +"');"
    circledb.update(sql)
    sql = "SELECT circle_name,circle_category,circle_short_intro,circle_logo_url,id,password FROM Circle_details WHERE circle_name=('"+circle_name + "') and master_name=('" + master_name +"');"
    circle_data = circledb.fetch_all(sql)[0]
    sql = "INSERT INTO Circle_List VALUES('"+str(circle_data[0])+"','"+str(circle_data[1])+"','"+str(circle_data[2])+"','"+str(circle_data[3])+"');"
    circledb.insert(sql)
    sql = "INSERT INTO user VALUES('"+str(circle_data[4])+"','"+str(circle_data[5])+"','"+master_name+"','"+'circle_user'+"');"
    circledb.insert(sql)
    return redirect('/circle/manage/circle_admin')

@app.route("/circle/manage/declined", methods=['POST'])
def cm_declined():
    circle_name=request.form['circle_name']
    circle_logo_url=request.form['circle_logo_url']
    master_name=request.form['master_name']
    sql = "DELETE FROM Circle_details WHERE  circle_name=('"+circle_name + "') and master_name=('" + master_name +"');"
    circledb.delete(sql)
    os.remove('./static'+circle_logo_url)
    return redirect('/circle/manage/circle_admin')

# 동아리 관리자(수정하기) ============================================================
@app.route("/circle/manage/circle_user")
def cm_circle_user():
    id=request.args.get('user_id')
    sql = "SELECT * FROM Circle_details WHERE id ='"+str(id)+"';"
    circle_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/cc_user/cc_user.html',circle_data= circle_data)


@app.route("/circle_update_post", methods=['POST'])
def circle_update_post():
    circle_name=request.form['circle_name']
    circle_category=request.form['circle_category']
    circle_short_intro=request.form['circle_short_intro']
    circle_logo_url=request.files['circle_logo_url']
    recruit_stday=request.form['recruit_stday']
    recruit_endday=request.form['recruit_endday']
    circle_detail_intro=request.form['circle_detail_intro']
    apply_process=request.form['apply_process']
    qualifications=request.form['qualifications']
    circle_recruit_url=request.form['circle_recruit_url']
    preferential=request.form['preferential']
    master_name=request.form['master_name']
    master_number=request.form['master_number']
    id=request.form['id']
    sql = "UPDATE Circle_details SET circle_name = '"+circle_name+"',circle_category='"+circle_category+"',circle_short_intro='"+circle_short_intro+"',recruit_stday='"+recruit_stday+"',recruit_endday='"+recruit_endday+"',circle_detail_intro='"+circle_detail_intro+"',apply_process='"+apply_process+"',qualifications='"+qualifications+"',preferential='"+preferential+"',circle_recruit_url='"+circle_recruit_url+"',master_name='"+master_name+"',master_number='"+master_number+"',sign_date='"+str(datetime.today().strftime("%Y-%m-%d"))+"' WHERE "+"circle_name ='"+circle_name+"' and master_name ='"+master_name+"';"
    circledb.update(sql)
    if len(secure_filename(circle_logo_url.filename)) != 0:
        circle_logo_url.save('./static/circle_logo/'+circle_name+'.png')
        sql = "UPDATE Circle_details SET circle_logo_url='"+('/circle_logo/'+circle_name+'.png')+"' WHERE circle_name='"+circle_name+"' and master_name='"+master_name+"';"
        circledb.update(sql)
    else:
        pass
    return redirect(url_for('cm_circle_user',user_id=id))

# 로그인/로그아웃 ============================================================
@app.route("/circle/manage/login")
def cm_login():
    if 'id' in session:  # 로그인한 사용자의 권한이 이미 저장되어 있으면
        if session['id'] == 'Admin':
            return redirect('/circle/manage/admin')
        elif session['id'] == 'circle_user':
            return redirect(url_for('cm_circle_user', user_id=id))
        elif session['id'] == 'circle_admin':
            return redirect('/circle/manage/circle_admin')
    return render_template('/circle/manage/cm_login.html')

@app.route("/circle/manage/logout")
def cm_logout():
    session.clear()
    return redirect('/circle/manage/login')

@app.route("/circle/cm_login_rq", methods=['POST'])
def cm_login_check():
    id=request.form['id']
    passwd=request.form['passwd']
    pwd_check_sql = "SELECT PW FROM user WHERE ID = '"+ str(id)+"'"
    check_pwd = circledb.fetch_all(pwd_check_sql)
    if len(check_pwd) == 0:
        check_pwd=''
    else:
        check_pwd = check_pwd[0][0]
    if check_pwd == passwd and len(check_pwd) != 0:
        sql="SELECT Authority FROM user WHERE ID ='"+ id + "'"
        authority = circledb.fetch_all(sql)
        authority = authority[0][0]
        session['id'] = authority
        if authority == 'Admin':
            return redirect('/circle/manage/admin')
        elif authority == 'circle_user':
            return redirect(url_for('cm_circle_user',user_id = id))
        elif authority == 'circle_admin':
            return redirect('/circle/manage/circle_admin')
        else:
            return redirect('/circle/manage/login')
    else:
        return '''<script>   alert('아이디 또는 패스워드를 확인하세요!'); 
                             window.location.href = '/circle/manage/login';
                  </script>'''
#find================================================================
#  섹터 : Find (Find 리스트, Find 등록) 
#  작성일              작성자              내용
# 23.01.08            박상범              최초등록
#=======================================================================

@app.route("/testtable")
def table():
    return render_template('info/bus.html')
@app.route("/find")
def find():
    sql = "SELECT * FROM Find_List;"
    find_list = finddb.fetch_all(sql)
    return render_template('find/find.html', find_data=find_list)

@app.route("/find_sign")
def find_sign():
    return render_template('find/find_sign.html')

@app.route("/find_sign_post", methods=['POST'])
def find_sign_post():
    category=request.form['category']
    title=request.form['title']
    contents=request.form['contents']
    place=request.form['place']
    date=request.form['Date']
    sign_url=request.form['sign_url']
    passwd=request.form['passwd']
    sign_date = datetime.now()+timedelta(hours=9)
    sql="INSERT INTO Find_List(Category, Title, Contents, Place, Date, signdate, password, sign_url) VALUES('"+category+"','"+title+"','"+contents+"','"+place+"','"+date+"','"+str(sign_date)+"','"+passwd+"','"+sign_url+"');"
    finddb.insert(sql)
    return render_template('find/find_sign.html') 

@app.route("/find/passwd")
def find_input_passwd_get():
    No = request.args.get('No')
    return render_template('find/find_del.html',No=No) 

@app.route("/find/check/passwd", methods=['POST'])
def find_check_passwd():
    No=request.form['No']
    passwd=request.form['password']
    sql = "SELECT password FROM Find_List WHERE No ="+No+"; "
    password = finddb.fetch_one(sql)
    if password == passwd:
        sql = "DELETE FROM Find_List WHERE No ="+No+"; "
        finddb.delete(sql)
        return '''<script>   alert('정상적으로 삭제되었습니다.'); 
                             window.location.href = '/find';
                  </script>'''
    else:
        return '''<script>   alert('아이디 또는 패스워드를 확인하세요!'); 
                            history.back();
                  </script>'''
    return password

@app.route('/find/detail/<int:question_id>/')
def find_detail(question_id):
    sql = "SELECT * FROM ;"
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question)
#carpool================================================================

@app.route('/car')
def car():
    return render_template('carpool/car.html')


@app.route('/car_driver', methods=['GET','POST'])
def car_driver():
    if(request.method=='GET'):
        return render_template('carpool/driver.html')
    elif(request.method=='POST'):     
        link=request.form ['link']
        car_name=request.form['car_name']
        departure=request.form['departure']
        destination=request.form['destination']
        car_time=request.form['time1']+request.form['time2']+request.form['time3']
        message=request.form['message']
        password=request.form['password']
        sql="INSERT INTO Car_List(car_name, link, departure, destination, car_time, message, password) VALUES('"+car_name+"','"+link+"','"+departure+"','"+destination+"','"+car_time+"','"+message+"','"+password+"');"
        cardb.insert(sql)
        return render_template('carpool/driver.html') 

@app.route('/car_choice')
def car_choice():
    sql='SELECT * FROM Car_List;'
    car_list=cardb.fetch_all(sql)
    return render_template('carpool/choice.html', car_data=car_list)

@app.route('/car_del')
def car_del():
    return render_template('carpool/car_del.html')

@app.route("/car_passwd")
def car_passwd():
    car_num = request.args.get('car_num')
    return render_template('carpool/car_del.html',car_num=car_num) 

@app.route("/car_passwd_check", methods=['POST'])
def car_passwd_check():
    car_num=request.form['car_num']
    passwd=request.form['check']
    sql = "SELECT password FROM Car_List WHERE car_num ="+car_num+"; "
    password = cardb.fetch_one(sql)
    if password == passwd:
        sql = "DELETE FROM Car_List WHERE car_num ="+car_num+"; "
        cardb.delete(sql)
        return '''<script>   alert('삭제되었습니다.'); 
                             window.location.href = '/car_choice';
                  </script>'''
    else:
        return '''<script>   alert('비밀번호를 확인하세요!'); 
                            history.back();
                  </script>'''
    return password
    


#rest=======================================================================

@app.route("/rest")
def rest():
    sql = "SELECT * FROM Rest_List;"
    rest_list = restdb.fetch_all(sql)
    return render_template('rest/restaurant.html', rest_data=rest_list)


#program================================================================

@app.route("/program")
def program():
    sql = "SELECT * FROM Prog_List;"
    prog_list = programdb.fetch_all(sql)
    
    event_sql = "SELECT * FROM Event_List;"
    event_list = programdb.fetch_all(event_sql)
    return render_template('program/program.html', prog_data=prog_list, event_data=event_list)


@app.route("/facility")
def facility():
    sql = "SELECT * FROM Facility_List;"
    facility_list = programdb.fetch_all(sql)
    return render_template('program/facility.html', facility_data=facility_list)

#info================================================================

@app.route('/graduation')
def graduation():
    return render_template('info/graduation.html')

@app.route('/bus')
def bus():
    return render_template('info/bus.html')


#=======================================================================

#청명제================================================================
@app.route('/festival2')
def fes_test():
    user_agent = 'naver'
    return render_template("/special/festival/agent_info.html",agent=user_agent)
import datetime
@app.route('/festival')
def festival():
    user_agent = request.user_agent.string.lower()
    if 'naver' in user_agent or 'samsung' in user_agent:
        if 'naver' in user_agent:
            user_agent = 'naver'
        if 'samsung' in user_agent:
            user_agent = 'samsung'
        return render_template("/special/festival/agent_info.html",agent=user_agent)
    stage_list = []
    if datetime.datetime.now().date() == datetime.date(2023, 4, 5):
        sql = '''SELECT CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">',stage_name, '</a>') AS stage_name,
                CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">', TIME_FORMAT(start_time, '%H:%i'), '</a>') AS start_time,
                CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">', TIME_FORMAT(end_time, '%H:%i'), '</a>') AS end_time
                FROM (
                    SELECT *,
                        @row_num := @row_num + 1 AS row_num
                    FROM DAY1_Stage_List, (SELECT @row_num := 0) r
                    WHERE DATE_FORMAT(STR_TO_DATE(end_time, '%H:%i:%s'), '%H:%i') >= TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i')
                ) AS t
                LIMIT 2;

            '''

        stage_list = festivaldb.fetch_all(sql)
    elif datetime.datetime.now().date() == datetime.date(2023, 4, 6):
        sql = '''SELECT CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">',stage_name, '</a>') AS stage_name,
                CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">', TIME_FORMAT(start_time, '%H:%i'), '</a>') AS start_time,
                CONCAT('<a style="color:', IF(row_num = 1, 'rgb(255, 59, 59)', 'black'), ';">', TIME_FORMAT(end_time, '%H:%i'), '</a>') AS end_time
                FROM (
                    SELECT *,
                        @row_num := @row_num + 1 AS row_num
                    FROM DAY2_Stage_List, (SELECT @row_num := 0) r
                    WHERE DATE_FORMAT(STR_TO_DATE(end_time, '%H:%i:%s'), '%H:%i') >= TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i')
                ) AS t
                LIMIT 2;

            '''

        stage_list = festivaldb.fetch_all(sql)
        
    else:
        stage_list.append('축제 당일에 공개 됩니다.')
        
    current_time = datetime.datetime.now().time()
    if datetime.time(11, 0) <= current_time <= datetime.time(23, 59):
        booth_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
    else:
        booth_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
    if datetime.time(17, 0) <= current_time <= datetime.time(23, 59):
        pub_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
    else:
        pub_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
    
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    
    sql = "SELECT COUNT(DISTINCT foodtu_name) FROM FoodTruck_List;"
    foodtruck_count = festivaldb.fetch_one(sql)
    sql = "SELECT COUNT(DISTINCT market_name) FROM Market_List;"
    market_count = festivaldb.fetch_one(sql)
    sql = "SELECT COUNT(DISTINCT booth_name) FROM Booth_List;"
    booth_count = festivaldb.fetch_one(sql)
    count_list = [booth_count,market_count,foodtruck_count]
    
    sql='''SELECT COUNT(*) 
           FROM Booth_List
           WHERE TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') >= 13 AND DATE_FORMAT(STR_TO_DATE(end_time, '%H:%i:%s'), '%H:%i') > TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i')

    '''
    food_count = festivaldb.fetch_one(sql)
    
    return render_template('special/festival/festival.html',booth_hour=booth_hour,pub_hour=pub_hour,stage_list=stage_list, count_list = count_list, food_count=food_count, month=month, day=day)



@app.route('/dev_info')
def dev_info():
    return render_template('special/festival/info/dev_info.html')


#청명제 지도============================================================
@app.route('/festival/map')
def map():
    sql = "SELECT * FROM FoodTruck_List;"
    foodtruck_list = festivaldb.fetch_all(sql)

    sql = "SELECT * FROM Boothbar_List ORDER BY booth_no ASC;"
    boothbar_list = festivaldb.fetch_all(sql)
    
    sql = "SELECT * FROM Boothbooth_List ORDER BY booth_no ASC;"
    boothbooth_list = festivaldb.fetch_all(sql)
    return render_template('special/festival/map/map.html', foodtruck_data=foodtruck_list, boothbar_data=boothbar_list, boothbooth_data=boothbooth_list)

@app.route('/festival/map_f')
def map2():
    sql = "SELECT * FROM FoodTruck_List;"
    foodtruck_list = festivaldb.fetch_all(sql)

    sql = "SELECT * FROM Boothbar_List ORDER BY booth_no ASC;"
    boothbar_list = festivaldb.fetch_all(sql)
    
    sql = "SELECT * FROM Boothbooth_List ORDER BY booth_no ASC;"
    boothbooth_list = festivaldb.fetch_all(sql)
    return render_template('special/festival/map/map_fix.html', foodtruck_data=foodtruck_list, boothbar_data=boothbar_list, boothbooth_data=boothbooth_list)

#청명제 타임테이블=========================================================

@app.route('/festival/timetable')
def timetable():
    sql_Schedule = "SELECT * FROM Schedule_List limit 13;"
    schedule_list = festivaldb.fetch_all(sql_Schedule)
    
    sql_DAY1_Booth = "SELECT * FROM DAY1_BoothTime_List;"
    d1boothtime_list = festivaldb.fetch_all(sql_DAY1_Booth)
    
    sql_DAY2_BoothTime = "SELECT * FROM DAY2_BoothTime_List;"
    d2boothtime_list = festivaldb.fetch_all(sql_DAY2_BoothTime)
    
    sql_Boothbar = "SELECT * FROM Boothbar_List;"
    boothbar_list = festivaldb.fetch_all(sql_Boothbar)
    
    return render_template('special/festival/timetable/timetable.html', schedule_data=schedule_list, d1boothtime_data=d1boothtime_list, d2boothtime_data=d2boothtime_list, boothbar_data=boothbar_list)

#청명제 search===========================================================
@app.route('/festival/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
        
    sql = "SELECT * FROM Booth_List WHERE booth_name LIKE '%{}%' OR booth_main LIKE '%{}%'".format(keyword, keyword)
    boothsearch_list = festivaldb.fetch_all(sql)

    search_name = "'{}'에 대한 검색 결과입니다!".format(keyword)
    return render_template('special/festival/search/search.html', boothsearch_data=boothsearch_list, search_name=search_name)

#======================================================================
#=======================================================================


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=3000)
