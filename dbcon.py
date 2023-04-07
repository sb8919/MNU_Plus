import pymysql

#circle================================================================
#  섹터 : Page 방문기록
#  수정일              작성자              내용
# 23.01.18            박상범              최초등록
#=======================================================================
page_conn = None
page_cur = None

page_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='PAGE_INFO',
                       charset='utf8')
page_cur = page_conn.cursor()

#circle================================================================
#  섹터 : 동아리 (동아리 리스트, 동아리 등록) 
#  수정일              작성자              내용
# 23.01.08            박상범              최초등록
#=======================================================================
circle_conn = None
circle_cur = None

circle_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='CIRCLE',
                       charset='utf8')
circle_cur = circle_conn.cursor()

#circle================================================================
#  섹터 : 스터디 (스터디 리스트, 스터디 등록) 
#  수정일              작성자              내용
# 23.01.14            박상범              최초등록
#=======================================================================
study_conn = None
study_cur = None

study_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='STUDY',
                       charset='utf8')
study_cur = study_conn.cursor()


#car================================================================
#  섹터 : 
#  수정일              작성자              내용
# 23.01.11            강민지              최초등록
#=======================================================================
car_conn = None
car_cur = None

car_conn=pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     passwd='ScE1234**',
                     db='CAR',
                     charset='utf8')
car_cur=car_conn.cursor()

#rest================================================================
#  섹터 : 
#  수정일              작성자              내용
# 23.01.12            박서린              최초등록
#=======================================================================
rest_conn = None
rest_cur = None

rest_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='REST', 
                       charset='utf8')
rest_cur = rest_conn.cursor()

#program================================================================
#  섹터 :
#  수정일              작성자              내용
# 23.01.12            양선아              최초등록
#=======================================================================
program_conn = None
program_cur = None

program_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='PROGRAM', 
                       charset='utf8')
program_cur = program_conn.cursor()

#festival================================================================
#  섹터 :
#  수정일              작성자              내용
# 23.03.30            양선아              최초등록
#=======================================================================
festival_conn = None
festival_cur = None

festival_conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='ScE1234**',
                       db='FESTIVAL', 
                       charset='utf8')
festival_cur = festival_conn.cursor()
