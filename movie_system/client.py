#encoding =utf-8
from socket import *
import os,sys
from time import sleep
import getpass 
from view import View

def do_child(s):
    data = s.recv(1024).decode()
    print(data)
    
def do_parent(s,name):
    view = View()
    while True:
        view.sysFunctionView()
        try:
            msg = int(input("请输入您要的选项(1or2or3or4or5or6):"))
        except Exception:
            print('您输入的选项有误:')
            continue
        if msg not in [1,2,3,4,5,6,7]:
            print('请输入正确选项:')
            sys.stdin.flush()
            continue
        elif msg == 1: 
            s.send('T'.encode())
            if do_tickets(s,name) !=0:
                print("购票失败")
            else:
                print("购票成功")
        elif msg == 2:
            if do_Recharge(s,name) == 0:
                print("充值成功")
            else:
                print("充值失败")
        elif msg == 3:
            if quiry_ticket(s,name) != 0:
                print("没有购票记录")
            else:
                print("购票记录如上")
        elif msg == 4:  
            if quiry_money(s,name) != 0:
                print("没有余额")
            else:
                print("余额如上")
        elif msg == 5:
            if change_pwd(s,name) !=0:
                print("修改失败")
            else:
                print("密码修改成功")
        elif msg == 6:
            if c_records(s,name) == 1:
                print("没有消费记录")
            else:
                print("消费记录如上")
        elif msg == 7:
            return



def c_records(s,name):
    while True:
        option = input("请输入您需要的服务，输入1查询消费记录，输入2查询充值记录"
)
        data = "D {} {}".format(option,name)
        s.send(data.encode())
        sleep(0.5)
        msg = s.recv(1024).decode()
        if msg =="没有消费记录":
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

def quiry_money(s,name):
    while True:
        data = "M {}".format(name)
        s.send(data.encode())
        msg = s.recv(1024).decode()
        if msg =="没有充值记录":
            return 1
        else:
            print(msg)
            return 0

def do_tickets(s,name):
    while True:
        sleep(1)
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)
        # choice = input("请选择影院or退出：")
        # msg = 
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


def do_Recharge(s,name):
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

def do_login(s):
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

def do_registered(s):
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

def main():  
    if len(sys.argv) <3:
        print(' argv is error!!!')
        return    
    host = sys.argv[1]
    port = int(sys.argv[2])
    addr = (host,port)
    s = socket()
    s.connect(addr)

    view = View()
    while True:
        view.printAdmView()
        choose = input("请输入要选择的选项(1.注册　2.登录 3.退出)：")
        if choose == '1':
            s.send('R'.encode())
            do_registered(s)
            continue
        elif choose == '2':
            name = do_login(s)
            if name:
                do_parent(s, name)             
            else:
                continue
        elif choose == '3':
            s.send('Q'.encode())
            sys.exit("客户端退出")
        else:
            print("选项不存在！")

    pid = os.fork()
    if pid <0:
        sys.exit("创建进程失败")
    elif pid ==0:
        do_child(s)
    else: 
        do_parent(s, name) 

if __name__=="__main__":
    main()