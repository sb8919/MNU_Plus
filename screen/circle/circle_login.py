from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os
import dbcl
import datetime

circle_login_bp = Blueprint("circle_login", __name__)
circledb = dbcl.DBconnector('CIRCLE')

# 동아리 등록 =====================================================================================
@circle_login_bp.route("/circle_sign_post", methods=['POST'])
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
    
@circle_login_bp.route("/circle/manage/id_check", methods=['POST'])
def cm_id_check():
    id = request.form['id']
    sql = "SELECT EXISTS(SELECT * FROM user WHERE id='"+id+"');"
    id_result = circledb.fetch_one(sql)
    return jsonify({"id":id_result})

# 페이지 관리자 ============================================================
@circle_login_bp.route("/circle/manage/admin")
def cm_admin():
    sql = "SELECT * FROM user;"
    user_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/admin/admin.html',user_data = user_data)

@circle_login_bp.route("/circle/manage/admin/update", methods=['POST'])
def cm_admin_update():
    id=request.form['id']
    passwd=request.form['passwd']
    name=request.form['name']
    authority=request.form['authority']
    sql = "UPDATE user SET ID='"+id+"', pW='"+passwd+"', NAME='"+name+"', AUTHORITY='"+authority+"' WHERE id='"+id+"';"
    circledb.update(sql)
    return redirect('/circle/manage/admin')


# 동아리 마스터 ============================================================
@circle_login_bp.route("/circle/manage/circle_admin")
def cm_circle_admin():
    sql = "SELECT circle_name,circle_category,master_name,master_number,circle_short_intro,circle_logo_url,sign_date FROM Circle_details WHERE circle_approval = 'N';"
    circle_sign_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/cc_admin/cc_admin.html',circle_sign_data= circle_sign_data)

@circle_login_bp.route("/circle/manage/approve", methods=['POST'])
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

@circle_login_bp.route("/circle/manage/declined", methods=['POST'])
def cm_declined():
    circle_name=request.form['circle_name']
    circle_logo_url=request.form['circle_logo_url']
    master_name=request.form['master_name']
    sql = "DELETE FROM Circle_details WHERE  circle_name=('"+circle_name + "') and master_name=('" + master_name +"');"
    circledb.delete(sql)
    os.remove('./static'+circle_logo_url)
    return redirect('/circle/manage/circle_admin')

# 동아리 관리자(수정하기) ============================================================
@circle_login_bp.route("/circle/manage/circle_user")
def cm_circle_user():
    id=request.args.get('user_id')
    sql = "SELECT * FROM Circle_details WHERE id ='"+str(id)+"';"
    circle_data = circledb.fetch_all(sql)
    return render_template('/circle/manage/cc_user/cc_user.html',circle_data= circle_data)


@circle_login_bp.route("/circle_update_post", methods=['POST'])
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
@circle_login_bp.route("/circle/manage/login")
def cm_login():
    if 'id' in session:  # 로그인한 사용자의 권한이 이미 저장되어 있으면
        if session['id'] == 'Admin':
            return redirect('/circle/manage/admin')
        elif session['id'] == 'circle_user':
            return redirect(url_for('cm_circle_user', user_id=id))
        elif session['id'] == 'circle_admin':
            return redirect('/circle/manage/circle_admin')
    return render_template('/circle/manage/cm_login.html')

@circle_login_bp.route("/circle/manage/logout")
def cm_logout():
    session.clear()
    return redirect('/circle/manage/login')

@circle_login_bp.route("/circle/cm_login_rq", methods=['POST'])
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
