from student import Student
docs = []


def add_student_info():
    L = Student.input_student()
    docs.extend(L)


# "| 2) 显示学生信息
def show_student_info():
    Student.output_student(docs)


# "| 3) 修改学生成绩
def modify_student_score():
    Student.alter_stdent(docs)


# | 4) 删除学生信息
def del_student_info():
    Student.del_student(docs)


# "| 5) 按成绩从高至低打印学生信息
def order_by_score_desc():
    Student.output_student(sorted(docs, key=Student.get_score, reverse=True))


# "| 6) 按成绩从低至高打印学生信息
def order_by_score():
    Student.output_student(sorted(docs, key=Student.get_score))


# "| 7) 按年龄从高至低打印学生信息
def order_by_age_desc():
    Student.output_student(sorted(docs, key=Student.get_age, reverse=True))


# "| 8) 按年龄从低至高打印学生信息
def order_by_age():
    Student.output_student(sorted(docs, key=Student.get_age))


# "| 9)　保存数据到文件(si.txt)
def save_to_txt():
    Student.save_to_txt(docs)


# "|10)从文件中读取数据（si.txt）
def read_from_txt():
    Student.output_student(Student.read_from_txt())


# |11)保存csv到文件（infos.csv）
def save_to_csv():
    Student.save_to_csv(docs)


# "|12)从csv文件中读取数据(infos.csv)
def read_from_csv():
    Student.output_student(Student.read_from_csv())
#print("|13) 保存到数据库                   |")


def save_to_mysql():
    Student.save_stu_mysql(docs)
