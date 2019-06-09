from time import *

start_time = '20180919190000'
print(start_time)
while True:
    sleep(1)
    print(strftime('%Y-%m-%d %H:%M:%S',localtime()))
    data = strftime('%Y-%m-%d %H:%M:%S',localtime())
    data_time = data.split(' ')
    year_moth = data_time[0].split('-')
    time_year = data_time[1].split(":")
    now_time = "".join(year_moth+time_year)
    if start_time == now_time:
        print("电影开始了")
        break