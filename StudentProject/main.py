from menu import show_menu
import student_infos as si


def main():
    while True:
        show_menu()
        s = input('请选择')
        if s == '1':
            si.add_student_info()
        elif s == '2':
            si.show_student_info()
        elif s == '3':
            si.modify_student_score()
        elif s == '4':
            si.del_student_info()
        elif s == '5':
            si.order_by_score_desc()
        elif s == '6':
            si.order_by_score()
        elif s == '7':
            si.order_by_age_desc()
        elif s == '8':
            si.order_by_age()
        elif s == '9':
            si.save_to_txt()
        elif s == '10':
            si.read_from_txt()
        elif s == '11':
            si.save_to_csv()
        elif s == '12':
            si.read_from_csv()
        elif s == '13':
            si.save_to_mysql()
        elif s == 'q':
            break


if __name__ == '__main__':
    main()
