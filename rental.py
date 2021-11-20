import pymysql
conn = pymysql.connect(host='localhost', user='root',
                       password='2020121t', db='appliance_rental', charset='utf8mb4')
cursor = conn.cursor()

# 기존 테이블 삭제
cursor.execute("set foreign_key_checks = 0")
cursor.execute("drop table IF EXISTS customer cascade")
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
cursor.execute("drop table IF EXISTS branch cascade")
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
cursor.execute("drop table IF EXISTS model cascade")
cursor.execute("set foreign_key_checks = 1")



# 테이블 생성
sql = """create table customer(
    cid varchar(7),
    cname varchar(7),
    ctel varchar(15),
    PRIMARY KEY (cid)
    )
    """
cursor.execute(sql)
sql = """create table branch(
    bid varchar(7) NOT NULL,
    bname varchar(7),
    baddr varchar(15),
    PRIMARY KEY (bid)
    )
    """
cursor.execute(sql)
sql = """create table model(
    bid varchar(7) NOT NULL,
    mno varchar(7) NOT NULL,
    cid varchar(7),
    type varchar(10),
    rentaldate date,
    FOREIGN KEY (bid) REFERENCES branch (bid),
    FOREIGN KEY (cid) REFERENCES customer (cid),
    PRIMARY KEY (bid, mno)
    )
    """
cursor.execute(sql)

def join() :
    # 입력 형식: 주고객 ID, 이름, 연락처 정보를 입력 파일로부터 읽기
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    CID = column_values[0]
    cname = column_values[1]
    contact = column_values[2]

    customer_sql = "insert into customer values('" \
                   + CID + "', '" + cname + "', '" + contact + "')"
    try:
        cursor.execute(customer_sql)
        conn.commit()
    except:
        conn.rollback()

    w_file.write("1.1. 회원가입\n")
    w_file.write("> " + CID + ' ' + cname + ' ' + contact + "\n")


def exit() :
    w_file.write("1.2. 종료\n")


def customer_login() :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()

    CID = column_values[0]
    w_file.write("2.1. 로그인\n")
    w_file.write("> " + CID + "\n")
    return CID


def customer_insert_model(cid) :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()

    BID = column_values[0]
    mno = column_values[1]
    rentaldate = column_values[2]

    sql = "select type from model where mno =" + "'" + mno + "'"
    cursor.execute(sql)
    conn.commit()
    rows = cursor.fetchall()
    type = ' '
    for cur_row in rows:
        type = cur_row[0]
        b_sql = "update model set rentaldate = '" + rentaldate + "' " + "where bid = '" + BID + "' and mno = '" + mno + "' "

        cursor.execute(b_sql)
        conn.commit()

    cursor.execute("select * from model")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        mmno = record[1]
        cid = record[2]
        mtype = record[3]
        rental = record[4]
        print(bid, mmno, cid, mtype, rental)

    w_file.write("2.2. 제품 렌탈 예약\n")
    w_file.write("> " + BID + " " + mno + " " + type + " " + rentaldate + "\n")


def customer_logout(cid):
    w_file.write("2.5. 로그아웃\n")
    w_file.write("> " + cid + "\n")

def admin_login() :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    CID = column_values[0]
    w_file.write("3.1. 로그인\n")
    w_file.write("> " + CID + "\n")

def insert_branch() :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    BID = column_values[0]
    bname = column_values[1]
    baddr = column_values[2]
    b_sql = "insert into branch values('" \
                   + BID + "', '" + bname + "', '" + baddr + "')"
    cursor.execute(b_sql)
    conn.commit()
    cursor.execute("select * from branch")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        bname = record[1]
        baddr = record[2]
        print(bid,bname, baddr)

    w_file.write("3.2. 대리점 정보 등록\n")
    w_file.write("> " + BID + ' ' + bname + ' ' + baddr + "\n")



def insert_model() :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    BID = column_values[0]
    mno = column_values[1]
    type = column_values[2]
    m_sql = "insert into model values('" \
            + BID + "', '" + mno + "', " + 'null' + ", '" + type +  "', " +'null' + ")"
    cursor.execute(m_sql)
    conn.commit()

    cursor.execute("select * from model")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        mmno = record[1]
        cid = record[2]
        mtype = record[3]
        print(bid,mmno,cid,mtype)

    w_file.write("3.3. 제품 정보 등록\n")
    w_file.write("> " + BID + ' ' + mno + ' ' + type + "\n")

def select_model_all() :

    '''m_sql = """select *
                from model"""'''

    m_sql = """select customer.cname, customer.cid, model.bid, model.mno, model.type, model.rentaldate 
            from customer, model
            where customer.cid = model.cid"""

    cursor.execute(m_sql)
    conn.commit()

    w_file.write("3.4. 렌탈 예약 내역 전체 조회\n")
    rows = cursor.fetchall()
    for cur_row in rows:
        cname = cur_row[0]
        cid = cur_row[1]
        bid = cur_row[2]
        mno = cur_row[3]
        type = cur_row[4]
        rentaldate = cur_row[5]
        w_file.write("> " + cname + ' ' + cid + ' ' + bid + ' ' + mno + ' ' +
                     type + ' ' + rentaldate + "\n")

def select_model_mno() :
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    input_mno = column_values[0]
    w_file.write("3.5. 렌탈 예약 내역 조회 (모델번호)\n")
    m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
            "from customer, model" + \
            "where model.mno like '%'" + input_mno + "'%' " + \
            "and customer.cid = model.cid"
    cursor.execute(m_sql)
    conn.commit()
    rows = cursor.fetchall()
    for cur_row in rows:
        cname = cur_row[0]
        cid = cur_row[1]
        bid = cur_row[2]
        mno = cur_row[3]
        type = cur_row[4]
        rentaldate = cur_row[5]
        w_file.write("> " + cname + ' ' + cid + ' ' + bid + ' ' + mno + ' ' +
                     type + ' ' + rentaldate + "\n")



def select_model_cname() :
    w_file.write("3.6. 예약 내역 조회 (고객 이름)\n")
    m_sql = """select customer.cname, customer.cid, branch.bid, model.mno, model.type, model.rentaldate 
            from customer, model, branch 
            and customer.cid = model.cid and model.bid = branch.bid"""
    try:
        cursor.execute(m_sql)
        conn.commit()
    except:
        conn.rollback()

cur_cid = ' '

def do_menu2(cid) :
    while True :
        line = r_file.readline()
        line = line.strip()
        menu_levels = line.split()

        # 메뉴 파싱을 위한 level 구분
        menu_level_1 = int(menu_levels[0])
        menu_level_2 = int(menu_levels[1])

        if menu_level_2 == 5:
            return
        elif menu_level_2 == 2:
            customer_insert_model(cid)

def doTask() :
    # 종료 메뉴(1 2)가 입력되기 전까지 반복함
    while True :
        # 입력파일에서 메뉴 숫자 2개 읽기
        line = r_file.readline()
        line = line.strip()
        menu_levels = line.split()

        # 메뉴 파싱을 위한 level 구분
        menu_level_1 = int(menu_levels[0])
        menu_level_2 = int(menu_levels[1])

        # 메뉴 구분 및 해당 연산 수행
        if menu_level_1 == 1 :
            if menu_level_2 == 1 :
                join()
            elif menu_level_2 == 2 :
                exit()
                break
        elif menu_level_1 == 2 :
            if menu_level_2 == 1:
                cur_cid = customer_login()
            elif menu_level_2 == 2:
                customer_insert_model(cur_cid)
            elif menu_level_2 == 5:
                customer_logout(cur_cid)

        elif menu_level_1 == 3:
            if menu_level_2 == 1:
                admin_login()
            elif menu_level_2 == 2:
                insert_branch()
            elif menu_level_2 == 3:
                insert_model()
            elif menu_level_2 == 4:
                select_model_all()
            elif menu_level_2 == 5:
                select_model_mno()
            elif menu_level_2 == 6:
                select_model_cname()



##############
#  메인 코드  #
##############

r_file = open("input.txt", "r")
w_file = open("output.txt", "w")

doTask()

r_file.close()
w_file.close()

conn.close()


'''

import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='2020121t', db='university', charset='utf8mb4')

def input_student(sno, sname, grade, dept):
    stud_sql = "insert into student values('" \
               + sno + "', '" + sname + "', " + grade + ", '" + dept + "')"
    try:
        cursor.execute(stud_sql)
        conn.commit()
    except:
        conn.rollback()

def input_course(cno, cname, credit, profname, dept):
    course_sql = "insert into course values('" \
                 + cno + "', '" + cname + "', '" + credit + "', '" + profname + "', '" + dept + "')"
    try:
        cursor.execute(course_sql)
        conn.commit()
    except:
        conn.rollback()

def input_enroll(sno, cno, final, lettergrade):
    enroll_sql = "insert into enroll values('" \
                 + sno + "', '" + cno + "', '" + final + "', '" + lettergrade + "')"
    student_sql = "insert into student values('" + sno + "',NULL,NULL,NULL)"
    course_sql = "insert into course values('" + cno + "',NULL,NULL,NULL,NULL)"
    cursor.execute(student_sql)
    cursor.execute(course_sql)
    cursor.execute(enroll_sql)
    conn.commit()


def select_student(cursor):
    sql = "select * from student"
    cursor.execute(sql)
    print("{0:<7}{1:>22}{2:>10}{3:>19}".format("sno", "sname", "grade", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sno = cur_row[0]
        sname = cur_row[1]
        grade = cur_row[2]
        dept = cur_row[3]
        print("%7s %20s %5s %20s" % (sno, sname, grade, dept))

def select_course(cursor):
    sql = "select * from course"
    cursor.execute(sql)
    print("{0:<4}{1:>33}{2:>9}{3:>20}{4:>20}".format("cno", "cname", "credit", "profname", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        cno = cur_row[0]
        cname = cur_row[1]
        credit = cur_row[2]
        profname = cur_row[3]
        dept = cur_row[4]
        print("%4s %30s %5s %20s %20s" % (cno, cname, credit, profname, dept))

def select_enroll(cursor):
    sql = "select * from enroll"
    cursor.execute(sql)
    print("{0:<7}{1:>4}{2:>8}{3:>20}".format("sno", "cno", "final", "lettergrade"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sno = cur_row[0]
        cno = cur_row[1]
        final = cur_row[2]
        lettergrade = cur_row[3]
        print("%7s %4s %5d %20s" % (sno, cno, final, lettergrade))

cursor = conn.cursor()

# 기존 테이블 삭제
cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS student cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS course cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

sql = "drop table IF EXISTS enroll cascade"
cursor.execute(sql)

# 테이블 생성
sql = "create table student(sno varchar(7), sname varchar(20), grade int, dept varchar(20), primary key (sno))"
cursor.execute(sql)
sql = "create table course(cno varchar(4), cname varchar(30), credit int, profname varchar(20), dept varchar(20), primary key (cno))"
cursor.execute(sql)
sql = """create table enroll(
    sno varchar(7),
    cno varchar(4),
    final int default 0,
    lettergrade varchar(2),
    FOREIGN KEY (sno) REFERENCES student (sno),
    FOREIGN KEY (cno) REFERENCES course (cno),
    PRIMARY KEY (sno, cno)
    )
    """
cursor.execute(sql)

print("0. 종료\n1. student 레코드 검색\n2. course 레코드 검색\n3. enroll 레코드 검색\n4. enroll 레코드 삽입")

input_student('B823019', '홍길동', '4', '컴퓨터')
input_student('B890515', '김철수', '3', '전기')
input_course('C101', '전기회로', '3', '김홍익', '전기')
input_course('C102', '데이터베이스', '4', '이대학', '컴퓨터')

while True:
    cmd = input("기능을 선택하시오 : ")
    if cmd == '0':
        break
    elif cmd == '1':
        select_student(cursor)
    elif cmd == '2':
        select_course(cursor)
    elif cmd == '3':
        select_enroll(cursor)
    else:
        print(">> 4. enroll 레코드 삽입")
        sno = input("학번을 입력하시오: ")
        cno = input("과목번호를 입력하시오: ")
        final = input("기말고사 점수를 입력하시오: ")
        grade = input("학점을 입력하시오: ")
        input_enroll(sno, cno, final, grade)

conn.close()

'''
