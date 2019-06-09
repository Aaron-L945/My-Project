import pymysql 
import re


db = pymysql.connect(host='localhost',user='root',password='123456',\
     database='Cinema',charset ='utf8')
#建立游标对象
cursor = db.cursor()

f = open('movie.txt','r')
while True:
    line = f.readline()
    if not line:
        break
    print(line)
    data = line.split(" ")
    m_name = data[0]
    print(m_name)
    s_time = data[1]
    print(s_time)
    price = data[2]
    print(price)
    seat = data[3]
    print(seat)
    sql = "insert into movie (m_name,s_time,price,seat) \
    values ('%s','%s','%s','%s')"%(m_name,s_time,price,seat)
    try:
        cursor.execute(sql)
        print("数据输入成功")
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

f.close()
cursor.close()
db.close()
