from flask import Blueprint, render_template, request
import dbcl
import datetime

main_bp = Blueprint("festival_main", __name__)
festivaldb = dbcl.DBconnector('FESTIVAL')
@main_bp.route('/festival3')
def festival2():
    return '더 좋은 서비스를 제공 해드리기 위해 점검중입니다.'
    
@main_bp.route('/festival')
def festival():
    user_agent = request.user_agent.string.lower()
    # if 'naver' in user_agent:
    #     if 'naver' in user_agent:
    #         user_agent = 'naver'
    #     if 'samsung' in user_agent:
    #         user_agent = 'samsung'
    #     return render_template("/special/festival/agent_info.html",agent=user_agent)
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
        stage_list.append ('축제 당일에 공개 됩니다.')
    booth_hour = ""
    pub_hour=""    
    ect=""
    if datetime.datetime.now().date() == datetime.date(2023, 4, 5):   
        current_time = datetime.datetime.now().time()
        if datetime.time(11, 0) <= current_time <= datetime.time(23, 59):
            booth_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
        else:
            booth_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
        if datetime.time(17, 0) <= current_time <= datetime.time(23, 59):
            pub_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
        else:
            pub_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
    elif datetime.datetime.now().date() == datetime.date(2023, 4, 6):
        current_time = datetime.datetime.now().time()
        if datetime.time(11, 0) <= current_time <= datetime.time(23, 59):
            booth_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
        else:
            booth_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
        if datetime.time(17, 0) <= current_time <= datetime.time(23, 59):
            pub_hour = '''<a style="color:rgb(255, 59, 59)">운영중</a>'''
        else:
            pub_hour = '''<a style="color:rgb(49, 127, 245)">오픈전</a>'''
    else:
        ect = '''<a style="color:rgb(255, 156, 173)">오픈 예정</a>'''
        
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    
    sql = "SELECT COUNT(DISTINCT foodtu_name) FROM FoodTruck_List;"
    foodtruck_count = festivaldb.fetch_one(sql)
    sql = "SELECT COUNT(DISTINCT market_name) FROM Market_List;"
    market_count = festivaldb.fetch_one(sql)
    sql = "SELECT COUNT(DISTINCT booth_name) FROM ALL_Booth_DAY1;"
    booth_count = festivaldb.fetch_one(sql)
    count_list = [booth_count,market_count,foodtruck_count]
    
    open_count = []
    if datetime.datetime.now().date() == datetime.date(2023, 4, 5):
        if datetime.datetime.now().time() >= datetime.time(17, 0):
            sql = '''SELECT count(*)
                     FROM ALL_Booth_DAY1
                     WHERE TIME_FORMAT(DATE_ADD('2023-04-05 09:02:00', INTERVAL 9 HOUR), '%H:%i') >=
                     DATE_FORMAT(STR_TO_DATE(open_time, '%H:%i:%s'), '%H:%i')
                     AND TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') <=
                     DATE_FORMAT(STR_TO_DATE(close_time, '%H:%i:%s'), '%H:%i');'''
            open_count = festivaldb.fetch_one(sql)
        else:
            sql = '''SELECT count(*)
                     FROM ALL_Booth_DAY1
                     WHERE TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') >= TIME_FORMAT(DATE_ADD('2023-04-05 04:00:00', INTERVAL 9 HOUR), '%H:%i') 
                     AND TIME_FORMAT(DATE_ADD('2023-04-05 07:58:00', INTERVAL 9 HOUR), '%H:%i') >=
                     DATE_FORMAT(STR_TO_DATE(open_time, '%H:%i:%s'), '%H:%i')
                     AND TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') <=
                     DATE_FORMAT(STR_TO_DATE(close_time, '%H:%i:%s'), '%H:%i');
            '''
            open_count = festivaldb.fetch_one(sql)
            
    elif datetime.datetime.now().date() == datetime.date(2023, 4, 6):
        if datetime.datetime.now().time() >= datetime.time(17, 0):
            sql = '''SELECT count(*)
                     FROM ALL_Booth_DAY2
                     WHERE TIME_FORMAT(DATE_ADD('2023-04-06 09:02:00', INTERVAL 9 HOUR), '%H:%i') >=
                     DATE_FORMAT(STR_TO_DATE(open_time, '%H:%i:%s'), '%H:%i')
                     AND TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') <=
                     DATE_FORMAT(STR_TO_DATE(close_time, '%H:%i:%s'), '%H:%i');'''
            open_count = festivaldb.fetch_one(sql)
        else:
            sql = '''SELECT count(*)
                     FROM ALL_Booth_DAY2
                     WHERE TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') >= TIME_FORMAT(DATE_ADD('2023-04-05 01:00:00', INTERVAL 9 HOUR), '%H:%i') 
                     AND TIME_FORMAT(DATE_ADD('2023-04-06 07:58:00', INTERVAL 9 HOUR), '%H:%i') >=
                     DATE_FORMAT(STR_TO_DATE(open_time, '%H:%i:%s'), '%H:%i')
                     AND TIME_FORMAT(DATE_ADD(NOW(), INTERVAL 9 HOUR), '%H:%i') <=
                     DATE_FORMAT(STR_TO_DATE(close_time, '%H:%i:%s'), '%H:%i');

            '''
            open_count = festivaldb.fetch_one(sql)
    else:
        open_count.append('축제 당일 운영중인 부스의 수가 표시됩니다.')  
    return render_template('special/festival/festival.html',booth_hour=booth_hour,pub_hour=pub_hour,stage_list=stage_list, count_list = count_list, open_count=open_count, month=month, day=day, ect=ect)
