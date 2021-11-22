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


def join():
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


def exit():
    w_file.write("1.2. 종료\n")


def customer_login():
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()

    CID = column_values[0]
    w_file.write("2.1. 로그인\n")
    w_file.write("> " + CID + "\n")
    return CID


def customer_insert_model(cur_cid):
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
        b_sql = "update model set rentaldate = '" + rentaldate + \
                "', " + "cid = '" + cur_cid + "' " + \
                " where bid = '" + BID + "' and mno = '" + mno + "' "

        cursor.execute(b_sql)
        conn.commit()
    print("2 2")
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


def customer_select(cur_cid):
    w_file.write("2.3. 제품 렌탈 예약 조회\n")
    sql = "select * from model where cid = '" + cur_cid + "' and rentaldate is not null "
    cursor.execute(sql)
    conn.commit()
    print("2 3")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        mno = record[1]
        type = record[3]
        rental = record[4]
        print(bid, mno, cur_cid, type, rental)
        w_file.write("> " + bid + " " + mno + " " + type + " " + str(rental) + "\n")


# 예약 취소를 하면 고객 id도 삭제할 것인가?
def customer_cancel(cur_cid):
    w_file.write("2.4. 제품 렌탈 예약 취소\n")
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()

    BID = column_values[0]
    mno = column_values[1]

    date_sql = "select rentaldate from model " + \
          " where bid = '" + BID + "' and mno = '" + mno + "' and cid = '" + cur_cid + "' "
    cursor.execute(date_sql)
    conn.commit()
    rtdate = ' '
    li = cursor.fetchall()
    for record in li:
        rtdate = record[0]

    sql = "update model set rentaldate = null " + \
          " where bid = '" + BID + "' and mno = '" + mno + "' and cid = '" + cur_cid + "' "

    cursor.execute(sql)
    conn.commit()
    print("2 4")
    cursor.execute("select * from model "
                   "where bid = '" + BID + "' and mno = '" + mno + "' and cid = '" + cur_cid + "' ")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        mno = record[1]
        cid = record[2]
        type = record[3]
        rental = record[4]
        print(bid, mno, cur_cid, type, rental)
        w_file.write("> " + bid + " " + mno + " " + type + " " + str(rtdate) + "\n")


def customer_logout(cid):
    w_file.write("2.5. 로그아웃\n")
    w_file.write("> " + cid + "\n")


def admin_login():
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    CID = column_values[0]
    w_file.write("3.1. 로그인\n")
    w_file.write("> " + CID + "\n")


def insert_branch():
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
        print(bid, bname, baddr)

    w_file.write("3.2. 대리점 정보 등록\n")
    w_file.write("> " + BID + ' ' + bname + ' ' + baddr + "\n")


def insert_model():
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    BID = column_values[0]
    mno = column_values[1]
    type = column_values[2]
    m_sql = "insert into model values('" \
            + BID + "', '" + mno + "', " + 'null' + ", '" + type + "', " + 'null' + ")"
    cursor.execute(m_sql)
    conn.commit()

    cursor.execute("select * from model")
    li = cursor.fetchall()
    for record in li:
        bid = record[0]
        mmno = record[1]
        cid = record[2]
        mtype = record[3]
        print(bid, mmno, cid, mtype)

    w_file.write("3.3. 제품 정보 등록\n")
    w_file.write("> " + BID + ' ' + mno + ' ' + type + "\n")


def select_model_all():
    m_sql = """select customer.cname, customer.cid, model.bid, model.mno, model.type, model.rentaldate 
            from customer, model
            where customer.cid = model.cid and rentaldate is not null"""

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
                     type + ' ' + str(rentaldate) + "\n")


def select_model_mno():
    w_file.write("3.5. 렌탈 예약 내역 조회 (모델번호)\n")
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    input_mno = column_values[0]
    if len(input_mno) == 1 or len(input_mno) == 4:  # mno는 고정길이 4
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where model.mno like '%" + input_mno + "%' and rentaldate is not null" + \
                "and customer.cid = model.cid"
    elif len(input_mno) == 2:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where model.mno like '%" + input_mno[0] + "%" + \
                "" + input_mno[1] + "%' and rentaldate is not null " + \
                "and customer.cid = model.cid"
    elif len(input_mno) == 3:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where model.mno like '%" + input_mno[0] + "%" + \
                input_mno[1] + "%" + \
                input_mno[2] + "%' and rentaldate is not null " + \
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
                     type + ' ' + str(rentaldate) + "\n")


def select_model_cname():
    w_file.write("3.6. 예약 내역 조회 (고객 이름)\n")
    line = r_file.readline()
    line = line.strip()
    column_values = line.split()
    input_cname = column_values[0]
    if len(input_cname) == 1:  # cname은 가변길이. 근데 이름이 '손고장난벽시'라면?
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where customer.cname like '%" + input_cname + "%' and rentaldate is not null " + \
                "and customer.cid = model.cid"
    elif len(input_cname) == 2:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where customer.cname like '%" + input_cname[0] + "%" + \
                input_cname[1] + "%' and rentaldate is not null " + \
                "and customer.cid = model.cid"
    elif len(input_cname) == 3:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where customer.cname like '%" + input_cname[0] + "%" + \
                input_cname[1] + "%" + \
                input_cname[2] + "%' and rentaldate is not null " + \
                "and customer.cid = model.cid"
    elif len(input_cname) == 4:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where customer.cname like '%" + input_cname[0] + "%" + \
                input_cname[1] + "%" + \
                input_cname[2] + "%" + \
                input_cname[3] + "%' and rentaldate is not null " + \
                "and customer.cid = model.cid"
    elif len(input_cname) == 5:
        m_sql = "select customer.cname, customer.cid, bid, model.mno, model.type, model.rentaldate " + \
                "from customer, model " + \
                "where customer.cname like '%" + input_cname[0] + "%" + \
                input_cname[1] + "%" + \
                input_cname[2] + "%" + \
                input_cname[3] + "%" + \
                input_cname[4] + "%' and rentaldate is not null " + \
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
                     type + ' ' + str(rentaldate) + "\n")


def admin_logout():
    w_file.write("3.7. 로그아웃\n")
    w_file.write("> admin\n")


def doTask():
    # 종료 메뉴(1 2)가 입력되기 전까지 반복함
    while True:
        # 입력파일에서 메뉴 숫자 2개 읽기
        line = r_file.readline()
        line = line.strip()
        menu_levels = line.split()

        # 메뉴 파싱을 위한 level 구분
        menu_level_1 = int(menu_levels[0])
        menu_level_2 = int(menu_levels[1])

        # 메뉴 구분 및 해당 연산 수행
        if menu_level_1 == 1:
            if menu_level_2 == 1:
                join()
            elif menu_level_2 == 2:
                exit()
                break
        elif menu_level_1 == 2:
            if menu_level_2 == 1:
                cur_cid = customer_login()
            elif menu_level_2 == 2:
                customer_insert_model(cur_cid)
            elif menu_level_2 == 3:
                customer_select(cur_cid)
            elif menu_level_2 == 4:
                customer_cancel(cur_cid)
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
            else:
                admin_logout()


cur_cid = ' '

r_file = open("input.txt", "r")
w_file = open("output.txt", "w")

doTask()

r_file.close()
w_file.close()

conn.close()
