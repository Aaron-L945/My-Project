import pymysql
import traceback


class Student:
    '''创建一个学生类'''

    def __init__(self, n, a, s):
        self.name, self.age, self.score = n, a, s

    def get_infos(self):
        s = '|%s|%s|%s|' % (self.name.center(15),
                            str(self.age).center(15),
                            str(self.score).center(15))
        return s

    def get_file_infos(self):
        s = self.name+',' +\
            str(self.age)+','+str(self.score)
        return s

    def get_score(self):
        return self.score

    def get_age(self):
        return self.age

    @classmethod
    def input_student(cls):
        L = []
        while True:
            n = input('输入学生姓名')
            if not n:
                break
            a = input('输入学生年龄')
            s = input('输入学生成绩')
            stu = Student(n, a, s)
            L.append(stu)
        return L

    @classmethod
    def output_student(cls, lst):
        print('+'+15*'-'+'+'+15*'-'+'+'+15*'-'+'+')
        print('|'+'name'.center(15)+'|'+'age'.center(15)
              + '|'+'score'.center(15)+'|')
        print('+'+15*'-'+'+'+15*'-'+'+'+15*'-'+'+')
        for stu in lst:
            s = stu.get_infos()
            print(s)
        print('+'+15*'-'+'+'+15*'-'+'+'+15*'-'+'+')

    @classmethod
    def alter_stdent(cls, lst):
        l = []
        while True:
            in_name = input('输入要修改的学生姓名')
            if not in_name:
                break
            in_score = input('输入要修改的学生成绩')
            for i in lst:
                if i.name == in_name:
                    i.score = in_score
                    l.append(i)
                else:
                    l.append(i)
        return l

    @classmethod
    def del_student(cls, lst):
        l = []
        while True:
            in_name = input('输入要删除的学生名字')
            if not in_name:
                break
            for i in lst:
                if i.name == in_name:
                    lst.remove(i)
                else:
                    l.append(i)
        return l

    @classmethod
    def save_to_txt(cls, lst):
        try:
            with open('si.txt', 'w')as f:
                for d in lst:
                    s = d.get_file_infos()
                    f.write(s+'\n')
                print('保存成功')
        except:
            print('写入文件失败')
            traceback.print_exc()

    @classmethod
    def read_from_txt(cls):
        L = []
        try:
            with open('si.txt', 'r')as f:
                while True:
                    s = f.readline()
                    if not s:
                        break
                    s = s.rstrip()
                    name_age_score = s.split(',')
                    n, a, s = name_age_score
                    a = int(a)
                    s = int(s)
                    L.append(Student(n, a, s))
        except:
            print('读文件失败！')
            traceback.print_exc()
        return L

    @classmethod
    def save_to_csv(cls, lst):
        try:
            with open('infos.csv', 'wb')as f:
                for i in lst:
                    s = i.get_file_infos()
                    b = s.encode('gbk') + b'\r\n'
                    f.write(b)
                print('保存成功')
        except:
            print('发生异常')
            traceback.print_exc()

    @classmethod
    def read_from_csv(cls):
        L = []
        try:
            with open('infos.csv', 'rb')as f:
                while True:
                    r = f.readline()
                    if not r:
                        break
                    s = r.decode()
                    s = s.rstrip()
                    name_age_score = s.split(',')
                    n, a, s = name_age_score
                    a = int(a)
                    s = int(s)
                    L.append(Student(n, a, s))
        except:
            print('发生异常')
            traceback.print_exc()
        return L

    @classmethod
    def save_stu_mysql(cls, lst):
        db = pymysql.connect('localhost', 'root', '123456', 'class')
        cursor = db.cursor()
        try:
            for i in lst:
                sql = 'insert into student (name,age,score) values("%s","%s","%s")'\
                    % (i.name, i.age, i.score)
                cursor.execute(sql)
            db.commit()
            print('保存成功')
        except:
            print('保存失败')
            traceback.print_exc()
            db.rollback()
        finally:
            cursor.close()
            db.close()
