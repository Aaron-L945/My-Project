import sys


def input_student():
    L = []
    while True:
        i_name = input('输入学生姓名')
        if not i_name:
            break
        i_age = input('输入学生年龄')
        i_score = input('输入学生成绩')
        d = {'name': i_name, 'age': i_age, 'score': i_score}
        L.append(d)
    return L


# print(int_student())
def output_student(lst):
    print('+'+15*'-'+'+'+15*'-'+'+'+15*'-'+'+')
    print('|'+'name'.center(15)+'|'+'age'.center(15)
          + '|'+'score'.center(15)+'|')
    print('+'+15*'-'+'+'+15*'-'+'+'+15*'-'+'+')

    for i in lst:
        s = '|%s|%s|%s|' % (i['name'].center(15),
                            str(i['age']).center(15),
                            str(i['score']).center(15))
        print(s)


def alter(lst):
    l = []
    while True:
        in_name = input('输入要修改的学生姓名')
        if not in_name:
            break
        in_score = input('输入要修改的学生成绩')
        for i in lst:
            if i['name'] == in_name:
                i['score'] = in_score
                l.append(i)
            else:
                l.append(i)
    return l


def del_student(lst):
    l = []
    while True:
        in_name = input('输入要删除的学生名字')
        if not in_name:
            break
        for i in lst:
            if i['name'] == in_name:
                lst.remove(i)
            else:
                l.append(i)
    return l


def save_student(lst):
    f = open('si.txt', 'w')
    for i in lst:
        s = i['name']+','+i['age']+','+i['score']
        f.write(s)

        f.write('\n')
    f.close()


def read_student():
    L = []
    try:
        f = open('si.txt', 'r')
        while True:
            r = f.readline()
            if not r:
                break
            # s = r.rstrip()
            l = r.split(',')
            student = {'name': l[0], 'age': int(l[1]), 'score': int(l[2])}
            L.append(student)
        f.close()
    except:
        print('打开文件失败')
    return L


def save_csv_student(lst):
    f = open('infos.csv', 'wb')
    for i in lst:
        s = i['name'] + ',' + str(i['age']) + ',' + str(i['score'])
        b = s.encode('gbk') + b'\r\n'
        f.write(b)
    f.close()


def read_csv_student():
    L = []
    f = open('infos.csv', 'rb')
    while True:
        r = f.readline()
        if not r:
            break
        s = r.decode('gbk')
        # str1 = s.rstrip()
        str2 = s.split(',')
        student = {'name': str2[0], 'age': int(str2[1]),
                   'score': int(str2[2])}
        L.append(student)
    f.close()
    return L


def show_menu():
    print("+-----------------------------------+")
    print("| 1) 添加学生信息                   |")
    print("| 2) 显示学生信息                   |")
    print("| 3) 修改学生成绩                   |")
    print("| 4) 删除学生信息                   |")
    print("| 5) 按成绩从高至低打印学生信息     |")
    print("| 6) 按成绩从低至高打印学生信息     |")
    print("| 7) 按年龄从高至低打印学生信息     |")
    print("| 8) 按年龄从低至高打印学生信息     |")
    print("| 9)　保存数据到文件(si.txt)        |")
    print("|10)从文件中读取数据（si.txt）      |")
    print("|11)保存csv到文件（infos.csv）      |")
    print("|12)从csv文件中读取数据(infos.csv)  |")
    print("| q) 退出程序                       |")
    print("+-----------------------------------+")


def main():
    docs = []
    while True:
        show_menu()
        s = input('请选择')
        if s == '1':
            lst = input_student()
            docs.extend(lst)
        elif s == '2':
            output_student(docs)
        elif s == '3':
            alter(docs)
        elif s == '4':
            del_student(docs)
        elif s == '5':
            output_student(
                sorted(docs, key=lambda d: d['score'], reverse=True))
        elif s == '6':
            output_student(sorted(docs, key=lambda d: d['score']))
        elif s == '7':
            output_student(sorted(docs, key=lambda d: d['age'], reverse=True))
        elif s == '8':
            output_student(sorted(docs, key=lambda d: d['age']))
        elif s == '9':
            save_student(docs)
        elif s == '10':
            output_student(read_student())
        elif s == '11':
            save_csv_student(docs)
        elif s == '12':
            output_student(read_csv_student())
        elif s == 'q':
            sys.exit()


if __name__ == '__main__':

    main()



