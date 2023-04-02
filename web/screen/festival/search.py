from flask import Blueprint, render_template, request
import dbcl
import datetime

search_bp = Blueprint("search", __name__)
festivaldb = dbcl.DBconnector('FESTIVAL')

@search_bp.route('/festival/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
        
    sql = "SELECT * FROM Booth_List WHERE booth_name LIKE '%{}%' OR booth_main LIKE '%{}%'".format(keyword, keyword)
    boothsearch_list = festivaldb.fetch_all(sql)

    search_name = "'{}'에 대한 검색 결과입니다!".format(keyword)
    return render_template('special/festival/search/search.html', boothsearch_data=boothsearch_list, search_name=search_name)
