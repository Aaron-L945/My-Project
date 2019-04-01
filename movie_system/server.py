#encoding =utf-8
from socket import *
from time import *
import os
import pymysql
import sys
from random import *
import threading

def main():
    #链接数据库
    db = pymysql.connect('localhost','root','123456',\
        'Cinema',charset = 'utf8')
    host = '0.0.0.0'
    prot = 8888
    addr = (host,prot)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(5)
 
    while True:
        try:
            c,addr = s.accept()
            print("连接地址是:",addr)
            print("等待客户端请求!")
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        pid = os.fork()
        if pid < 0:
            sys.exit("登录系统失败")
        elif pid == 0:
            s.close()
            do_processes(c,db)
        else:
            c.close()



def tickets_num():
    num =""
    for _ in range(6):
        th =randrange(0,9)
        num += str(th)
    return num

def user_money(c,db,msg):
    sql = "select money from user where name ='%s';"%msg
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    price_info = cursor.fetchone()
    price = int(price_info[0])
    return price

def movie_ms(c,db,number):
    cursor=db.cursor()
    sql = "select m_name,s_time,price from movie where id ='%s';"%number
    cursor.execute(sql)
    movie_ms = cursor.fetchone()
    return movie_ms

def do_Deductions(c,db,msg,cash,data):
    cursor=db.cursor()
    sql = "update user set money=%s where name = %s;"
    c_time = ctime()
    sql1 = "insert into c_info(name,c_time,c_cash)\
    values(%s,%s,%s);"
    try:
        cursor.execute(sql1,[msg,c_time,data])
        db.commit()
    except Exception as e:
        print(e)
    try:
        cursor.execute(sql,[cash,msg])
        db.commit()
        print("消费成功,{}的余额是:{}".format(msg,cash))    
    except Exception as e:
        print(e)
        print("充值失败")
        db.rollback()
        return
    else:
        return cash


def do_seat(c,db,msg,num):
    sql = "update movie set seat=%s where m_name = %s;"
    cursor=db.cursor()
    try:
        cursor.execute(sql,[num,msg])
        db.commit()
        print("座位已修改，现在的座位是{}".format(num))    
    except Exception as e:
        print(e)
        print("座位修改失败")
        db.rollback()
        return
    else:
        return num
    

def seat_number(num):
    L =[]
    for _ in range(int(num)):
        line_n = ""
        th =randrange(1,11)
        line_n += str(th)
        list_n = ""
        ts = randrange(1,11)
        list_n += str(ts)
        seat_num = line_n+list_n
        L.append(seat_num)
    return L


def do_checkseat(c,db,msg):
    sql = "select seat from movie where m_name = %s;"
    cursor = db.cursor()
    cursor.execute(sql,[msg])
    movie_seat = cursor.fetchone()
    print(movie_seat)
    now_seat = movie_seat[0]
    return now_seat


def do_tickets(c,db):
    sql = "select * from movie;"
    cursor = db.cursor()
    cursor.execute(sql)
    movie_tb = cursor.fetchall()
    if movie_tb:
        for movie_info in movie_tb:
            m_id = movie_info[0]
            m_name = movie_info[1]
            m_time = movie_info[2]
            price = movie_info[3]
            seat = movie_info[4]
            data = ' {} {} {} {} {}\n'.format(m_id,m_name,m_time,price,seat)
            c.send(data.encode())
    else:
        c.send("查找电影失败，请重试！".encode())
    data = c.recv(1024).decode()
    name = data.split(' ')[0]
    t_id = data.split(' ')[1]
    t_num = data.split(' ')[2]
    print(name)
    print(t_id)
    print(t_num)
    movie_mssg = movie_ms(c,db,t_id)
    print(movie_mssg)
    n_name = movie_mssg[0]
    n_time = str(movie_mssg[1]).split(' ')
    print(n_time)
    n_price = movie_mssg[2]
    n_time_1 = n_time [0].split('-')
    n_time_2 = n_time[1].split(':')
    a_time = int(''.join(n_time_1+n_time_2))
    num = tickets_num()
    seat_num = seat_number(t_num)
    user_price = user_money(c,db,name)
    print(user_price)
    c_amount = str(int(n_price)*int(t_num))
    dissipate = ctime()
    now_price = int(user_price)-int(n_price)*int(t_num)
    cash = do_Deductions(c,db,name,now_price,c_amount)
    balance = str(now_price)
    now_seat = do_checkseat(c,db,n_name)
    change_seat = str(int(now_seat)-int(t_num))
    new_seat = do_seat(c,db,n_name,change_seat)
    i = 0
    while i<int(t_num):
        useat = seat_num[i]
        line_n = useat[0]
        list_n = useat[1]
        print(line_n)
        print(list_n)
        sql1 = "insert into info (name,m_name,s_time,num,line_n,list_n,t_num,dissipate,c_amount) \
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        try:
            cursor.execute(sql1,[name,n_name,a_time,num,line_n,list_n,t_num,dissipate,c_amount])
            db.commit()
            msg = "购票成功，您的取票码是{0},您的余额是{1},您的座位号是{2}排{3}号".format(num,balance,line_n,list_n)
            c.send(msg.encode())
        except Exception as e:
            print(e)
            c.send('购票失败'.encode())
            db.rollback()
            return 
        else:
            print("%s购票成功"%name)
        i+=1



def do_registered(c,db):
    print("准备注册:")
    while True:
        c.send('请输入用户名：'.encode())
        name = c.recv(1024).decode()
        sql = "select * from user\
        where name='%s'"%name
        cursor = db.cursor()
        cursor.execute(sql)
        msg_info = cursor.fetchone()
        if msg_info or name == 'Administrators':
            c.send("用户名已存在！".encode())
            continue
        break
    while True:
        c.send('请输入密码：'.encode())
        passwd = c.recv(1024).decode()
        if len(passwd) < 6:
            c.send("密码不能小于6位".encode())
            continue
        c.send('请确认密码：'.encode())
        passwd1 = c.recv(1024).decode()
        if passwd != passwd1:
            c.send("两次密码不相同！".encode())
            continue
        break
    while True:
        c.send("请输入身份证号：".encode())
        userid = c.recv(1024).decode()
        if len(str(userid)) != 18:
            c.send("身份证号不正确！".encode())
            continue
        break
    while True:
        c.send("请输入电话号码：".encode())
        try:
            pnumber = int(c.recv(1024).decode())
            if not(9999999999< pnumber <99999999999):
                c.send("电话号码不正确！".encode())
                continue
        except:
            c.send("请输入数字！".encode())
            continue
        break
    while True:
        c.send("请输入预存金额：".encode())
        try:
            money = int(c.recv(1024).decode())
            if money < 100:
                c.send("预存金额不能小于100！".encode())
                continue
        except:
            c.send("请输入数字！".encode())
            continue
        break
    
    sql = "insert into user (name,passwd,userid,pnumber,money)\
    values('%s','%s','%s','%s','%s')"\
    %(name,passwd,userid,pnumber,money)
    
    try:
        cursor.execute(sql)
        db.commit()
        c.send("注册成功".encode())
    except Exception as e:
        print(e)
        c.send(b'FALL')
        db.rollback()
        return 
    else:
        print("%s注册成功"%name)



def do_Login(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    passwd = data[2]
    cursor = db.cursor()
    sql = "select * from user\
    where name='%s' and passwd='%s'"%(name,passwd)
    cursor.execute(sql)
    msg_info = cursor.fetchone()
    if msg_info != None:
        c.send("登录成功".encode())
        return 0
    else:
        c.send("用户名或密码不对!".encode())
        return 1

def do_Recharge(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    c_money = data[2]
    cursor = db.cursor()
    sql1 = "select money from user where name = '%s'"%name
    cursor.execute(sql1)
    k_money = cursor.fetchone()[0]
    new_money = str(int(k_money)+int(c_money))
    sql = "update user set money=%s where name = %s;"
    try:
        cursor.execute(sql,[new_money,name])
        db.commit()
        c.send(("充值成功,您的余额是:{}".format(new_money)).encode())      
    except Exception as e:
        print(e)
        c.send("充值失败".encode())
        db.rollback()
        return
    else:
        print("%s充值成功"%name)
    r_time = ctime()
    sql = "insert into r_info(name,r_time,r_cash)\
    values(%s,%s,%s);"
    try:
        cursor.execute(sql,[name,r_time,c_money])
        db.commit()
    except Exception as e:
        print(e)
        return

def do_quiry_ticket(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    cursor = db.cursor()
    sql = "select * from info where name = '%s'"%name
    cursor.execute(sql)
    user_info = cursor.fetchall()
    if not user_info:
        c.send("没有购票记录".encode())
    else:
        for user_tb in user_info:
            user_id = user_tb[0]
            user_name = user_tb[1]
            m_name = user_tb[2]
            s_time = user_tb[3]
            c_num = user_tb[4]
            h_num = str(user_tb[5])
            l_num = str(user_tb[6])
            tickets_num = user_tb[7]
            data = '{} {} {} {} {} 排:{} 号:{}票数:{}\n'\
            .format(user_id,user_name,m_name,s_time,c_num,h_num,l_num,tickets_num)
            c.send(data.encode())
        
def do_quiry_money(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    cursor = db.cursor()
    sql = "select money from user where name = '%s';"%name
    cursor.execute(sql)
    money_info = cursor.fetchone()
    if not money_info:
        c.send("没有充值记录".encode())
    else:
        money_num = money_info[0]
        data = '您的余额是{}'.format(money_num)
        c.send(data.encode())

def do_change_pwd(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    n_passwd = data[2]
    cursor = db.cursor()
    sql = "update user set passwd=%s where name = %s;"
    try:
        cursor.execute(sql,[n_passwd,name])
        db.commit()
        c.send("密码修改成功".encode())      
    except Exception as e:
        print(e)
        c.send("修改失败".encode())
        db.rollback()
        return
    else:
        print("%s修改密码成功"%name)

def r_records(c,db,msg):
    cursor = db.cursor()
    sql = "select name,r_time,r_cash from r_info where name = '%s';"%msg
    cursor.execute(sql)
    records = cursor.fetchall()
    if not records:
        return None
    else:
        return records

def c_records(c,db,msg):
    cursor = db.cursor()
    sql = "select name,c_time,c_cash from c_info where name = '%s';"%msg
    cursor.execute(sql)
    records = cursor.fetchall()
    if not records:
        return None
    else:
        return records

def do_c_records(c,db,msg):
    data = msg.split(" ")
    name = data[2]
    if data[1] == '2':
        data = r_records(c,db,name)
        if not data:
            c.send("没有消费记录".encode())
        else:
            for records in data:
                user_name = records[0]
                r_time = records[1]
                r_cash = records[2]
                msg = "{}充值{}元,充值时间:{}\n".format(user_name,r_cash,r_time)
                c.send(msg.encode())
                print("%s查询成功"%user_name)
    else:
        data = c_records(c,db,name)
        if not data:
            c.send("没有消费记录".encode())
        else:
            for records in data:
                user_name = records[0]
                c_time = records[1]
                c_cash = records[2]
                msg = "{}消费{}元，消费时间:{}\n".format(user_name,c_cash,c_time)
                c.send(msg.encode())
                print("%s查询成功"%user_name)


def do_processes(c,db):
    while True:
        msg = c.recv(1024).decode()
        print("客户端的请求是:",msg)
        if msg =='R':
            do_registered(c,db)
        elif msg[0] =='L':
            a = do_Login(c,db,msg)
            if a == 0: 
                d_remind = threading.Thread(target=do_remind,args=(c,db,msg))
                d_remind.setDaemon(True)
                d_remind.start()
            else:
                continue
        elif msg == "Q":
            sys.exit("退出系统")
            d_remind.join()
        elif msg[0] =='C':
            do_Recharge(c,db,msg)
        elif msg == 'T':
            do_tickets(c,db)
        elif msg[0] =='Q':
            do_quiry_ticket(c,db,msg)
        elif msg[0] =='M':
            do_quiry_money(c,db,msg)
        elif msg[0] =='P':
            do_change_pwd(c,db,msg)
        elif msg[0] == 'D':
            do_c_records(c,db,msg)


def do_remind(c,db,msg):
    data = msg.split(" ")
    name = data[1]
    sql = "select m_name,s_time from info where name ='%s'"%name
    cursor = db.cursor()
    cursor.execute(sql)
    s_times = cursor.fetchall()
    for n in range(len(s_times)):
        m_name = s_times[n][0]
        s_time = str(s_times[n][1])
        movie_start = s_time.split(' ')
        movie_year = movie_start[0].split("-")
        movie_time = movie_start[1].split(":")
        if int(movie_time[1]) > 20:
            remind_time = str(int(movie_time[1])-20)
            movie_time[1] = remind_time
            start = "".join(movie_year+movie_time)
            sleep(1)
            print(strftime('%Y-%m-%d %H:%M:%S',localtime())) 
            data = strftime('%Y-%m-%d %H:%M:%S',localtime())
            data_time = data.split(' ')
            year_moth = data_time[0].split('-')
            time_year = data_time[1].split(":")
            now_time = "".join(year_moth+time_year)
            if start == now_time:
                data = '你购买的电影{}还有20分钟开始,请提前取票入场!'.format(m_name)
                c.send(data.encode())
        else:
            remind_time = str(int(movie_time[1])+40)
            movie_time[1] = remind_time
            remind_hour = str(int(movie_time[0])-1)
            movie_time[0] = remind_hour 
            start = "".join(movie_year+movie_time)
            sleep(1)
            print(strftime('%Y-%m-%d %H:%M:%S',localtime())) 
            data = strftime('%Y-%m-%d %H:%M:%S',localtime())
            data_time = data.split(' ')
            year_moth = data_time[0].split('-')
            time_year = data_time[1].split(":")
            now_time = "".join(year_moth+time_year)
            if start == now_time:
                data = '你购买的电影{}还有20分钟开始,请提前取票入场!'.format(m_name)
                c.send(data.encode())


if __name__=="__main__":
    main()

