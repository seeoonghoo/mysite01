from django.db import models

from MySQLdb import connect, OperationalError
from MySQLdb.cursors import DictCursor

def findbyno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select no from user where no = %s'
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def view_findbyno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
    select title, contents, user_no 
    from board as a, user as b 
    where a.no = %s and user_no = b.no 
    '''
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def real_findbyno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
    select user_no 
    from board as a, user as b 
    where a.no = %s and a.user_no = b.no 
    '''
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def update_findbyno(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select title,contents from board where no = %s'
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def count():
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select count(*) from board'
    cursor.execute(sql)

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def findall(page, list_count):
    db = conn()

    cursor = db.cursor(DictCursor)
    tmp = 'date_format(reg_date, "%Y-%m-%d %p %h:%i:%s") as reg_date'
    page = (page-1)*10
    sql = '''
    select 
        a.no, 
        title, 
        contents, 
        hit, 
        date_format(reg_date, "%%Y-%%m-%%d %%p %%h:%%i:%%s") as reg_date, 
        g_no, 
        o_no, 
        depth, 
        user_no, 
        name 
    from board as a, user as b 
    where user_no = b.no 
    order by g_no desc, o_no asc 
    limit %s, %s
    '''
    cursor.execute(sql, (page, list_count))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result

def search_find(kwd,page, list_count):
    db = conn()

    cursor = db.cursor(DictCursor)
    tmp = '%' + kwd + "%"
    page = (page-1)*10
    sql = '''
    select 
        a.no, 
        title, 
        contents, 
        hit, 
        date_format(reg_date, "%%Y-%%m-%%d %%p %%h:%%i:%%s") as reg_date,
        g_no, 
        o_no, 
        depth, 
        user_no, 
        name 
    from board as a, user as b 
    where user_no = b.no and title like %s
    order by g_no desc, o_no asc 
    limit %s, %s
    '''
    cursor.execute(sql, (tmp,page, list_count))

    result = cursor.fetchall()

    cursor.close()
    db.close()

    return result



def hit_update(no):
    try:
        db = conn()

        cursor = db.cursor()

        sql = 'update board set hit = hit+1 where no = %s'
        count = cursor.execute(sql, (no,))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def write(no, title, contents):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        g_no = g_no_find()
        g_no["max(g_no)"] = g_no["max(g_no)"] + 1

        sql = 'insert into board values(null, %s, %s, 0, now(), %s,1,0,%s);'
        count = cursor.execute(sql, (title,contents,g_no["max(g_no)"],no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def write(no, title, contents):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        g_no = g_no_find()
        g_no["max(g_no)"] = g_no["max(g_no)"] + 1

        sql = 'insert into board values(null, %s, %s, 0, now(), %s,1,0,%s);'
        count = cursor.execute(sql, (title,contents,g_no["max(g_no)"],no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def g_no_find():
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = 'select max(g_no) from board'
    cursor.execute(sql)

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def deleteby_no(no):
    try:
        db = conn()

        cursor = db.cursor()

        sql = 'delete from board where no = %s'
        count = cursor.execute(sql, (no, ))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def updateby_no(title,contents,no):
    try:
        db = conn()

        cursor = db.cursor()

        sql = 'update board set title = %s, contents=%s where no = %s'
        count = cursor.execute(sql, (title,contents,no ))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def reply_findall(no):
    db = conn()

    cursor = db.cursor(DictCursor)

    sql = '''
    select 
        g_no, 
        o_no, 
        depth
    from board as a, user as b 
    where a.user_no = b.no and a.no = %s
    '''
    cursor.execute(sql, (no,))

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result

def reply(no, title, contents, g_no, o_no, depth):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        reply_update(g_no,o_no)

        sql = 'insert into board values(null, %s, %s, 0, now(), %s,%s,%s,%s)'
        count = cursor.execute(sql, (title,contents,g_no,o_no,depth,no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')

def reply_update(g_no, o_no):
    try:
        db = conn()

        cursor = db.cursor(DictCursor)

        sql = 'update board set o_no = o_no + 1 where g_no = %s and o_no >= %s '
        count = cursor.execute(sql, (g_no,o_no))

        db.commit()

        cursor.close()
        db.close()

        return count == 1

    except OperationalError as e:
        print(f'error: {e}')


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')