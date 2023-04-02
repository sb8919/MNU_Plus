from flask import Blueprint, render_template, request
import dbcl
import datetime

timetable_bp = Blueprint("timetable", __name__)
festivaldb = dbcl.DBconnector('FESTIVAL')

@timetable_bp.route('/festival/timetable')
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
