from flask import Blueprint, render_template, request
import dbcl
import datetime

map_bp = Blueprint("map", __name__)
festivaldb = dbcl.DBconnector('FESTIVAL')

@map_bp.route('/festival/map')
def map():
    sql = "SELECT * FROM FoodTruck_List;"
    foodtruck_list = festivaldb.fetch_all(sql)

    sql = "SELECT * FROM Boothbar_List ORDER BY booth_no ASC;"
    boothbar_list = festivaldb.fetch_all(sql)
    
    sql = "SELECT * FROM Boothbooth_List ORDER BY booth_no ASC;"
    boothbooth_list = festivaldb.fetch_all(sql)
    return render_template('special/festival/map/map.html', foodtruck_data=foodtruck_list, boothbar_data=boothbar_list, boothbooth_data=boothbooth_list)
