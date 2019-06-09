from socket import *
import os,sys
from time import sleep
import getpass 
from view import View

class user():
    def __init__(self,addr):
        self.scokfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
    
    def connect(self,addr):
        self.sockfd.connect(addr)
    
    def do_registered(self):
        while True:
            data = s.recv(1024).decode()
            if data == '注册成功':
                print(data)
                break
            elif data == '请输入密码：' or data == '请确认密码：':
                msg = getpass.getpass(data)
            else:
                msg = input(data)
            s.send(msg.encode())

    def do_login(self):
        while True:
            name = input("请输入您的用户名:")
            passwd = getpass.getpass("请输入您的密码：")
            msg = "L {} {}".format(name,passwd)

            s.send(msg.encode())
            data = s.recv(1024).decode()
            if data == "登录成功":
                print(data)
                return name
            else:
                print(data)
                return

    def do_Recharge(self,name):
        while True:
            money = input("请输入您要充值的费用:")
            if len(money) < 0:
                print("您的充值金额低于0")
                continue
            data = 'C {} {}'.format(name,money)
            s.send(data.encode())
            msg = s.recv(1024).decode()
            if msg =="充值失败":
                return 1
            else:
                print(msg)
                return 0

    def do_tickets(self,name):
        while True:
        sleep(1)
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)
        num = input("请选择电影序号or退出：")
        sleep(1)
        t_num = input("您要购买几张票:")
        if num.isdigit() and 0<int(t_num)<4:
            data = '{} {} {}'.format(name,int(num),int(t_num))
            sleep(3)
            s.send(data.encode())
            sleep(0.5)
            msg = s.recv(1024).decode()
            if msg =="购票失败":
                return 1
            elif msg =="查找电影失败，请重试":
                print(msg)
                return 
            else:
                print(msg)
                return 0
        elif num == "q":
            return 
        else:
            print("输出有误")

    def quiry_money(self,name):
        while True:
            data = "M {}".format(name)
            s.send(data.encode())
            msg = s.recv(1024).decode()
            if msg =="没有充值记录":
                return 1
            else:
                print(msg)
                return 0

    def quiry_ticket(s,name):
        while True:
            data = "Q {}".format(name)
            s.send(data.encode())
            sleep(1)
            msg = s.recv(1024).decode()
            if msg == "没有购票记录":
                return 1
            else:
                print(msg)
                return 0

    def change_pwd(s,name):
        while True:
            passwd = getpass.getpass("请输入您要修改的密码:")
            passwd1 = getpass.getpass("请确认您要修改的密码:")
            if passwd != passwd1 or len(passwd)<6:
                continue
            data = 'P {} {}'.format(name,passwd)
            s.send(data.encode())
            msg = s.recv(1024).decode()
            if msg =="修改失败":
                return 1 
            else:
                return 0 