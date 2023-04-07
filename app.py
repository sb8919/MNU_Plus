# -*- coding: utf-8 -*-
import socket
import dbcon
import os
import dbcl
from flask import Flask, session, redirect, url_for, jsonify, render_template, request, flash
from flask_login import LoginManager
from datetime import datetime,timedelta


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

from screen.main import main
app.register_blueprint(main.main_bp)

#circle================================================================

from screen.circle import circle_main
app.register_blueprint(circle_main.circle_main_bp)

from screen.circle import circle_login
app.register_blueprint(circle_login.circle_login_bp)

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

from screen.festival import main
app.register_blueprint(main.main_bp)

#청명제 지도============================================================

from screen.festival import map
app.register_blueprint(map.map_bp)

#청명제 타임테이블=========================================================

from screen.festival import timetable
app.register_blueprint(timetable.timetable_bp)

#청명제 search===========================================================

from screen.festival import search
app.register_blueprint(search.search_bp)

#=======================================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
