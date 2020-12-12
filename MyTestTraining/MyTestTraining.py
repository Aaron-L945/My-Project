import json
import random
import pdb
from time import sleep


class TestTraining():

    def __init__(self):
        pass

    # 获取所有试题
    def get_all_test_question(self):
        with open("./test_data.py", encoding="utf-8") as f:
            try:
                test_data = json.load(f)
            except Exception as e:
                print(e)
                return
            return test_data

    # 获取所有试题关键字
    def get_all_test_key(self):
        with open("./test_check.py", encoding="utf-8") as f:
            try:
                test_data = json.load(f)
            except Exception as e:
                print(e)
                return
            return test_data

    # 获取所有测试权重
    def get_all_weight(self, head=None):
        with open("./test_weight.py", encoding="utf-8") as f:
            test_weight_list = []
            try:
                test_data_dict = json.load(f)
            except Exception as e:
                print(e)
                return
            test_heads = test_data_dict.keys()
            for test in test_heads:
                if head:
                    if head == test:
                        for k, v in test_data_dict[test].items():
                            test_weight_list.append(v)
                        return test_weight_list
                for k, v in test_data_dict[test].items():
                    test_weight_list.append(v)
            return test_weight_list

    # 指定试题测试
    def appoint_test_question(self):
        # 获取所有试题大类
        test_all_dict = self.get_all_test_question()
        test_head = test_all_dict.keys()
        print(test_head)
        return test_head

    # 根据权重选择试题
    def weight_choice(self, weight):
        t = random.randint(0, sum(weight) - 1)
        for i, val in enumerate(weight):
            t -= val
            if t < 0:
                return i

    # 随机打开试题
    def random_open_test_question(self):

        test_all_dict = {}
        test_all_data = self.get_all_test_question()
        test_count = 0
        correct_count = 0
        head = None
        while True:
            self.test_show("Input all or specified or quit?")
            result = input("The input==>")
            # 所有试题随机
            if result == 'all':
                for k in list(self.appoint_test_question()):
                    test_all_dict.update(test_all_data[k])
                # test = random.choice(list(test_all_dict.keys()))
                all_head_test = list(test_all_dict.keys())
                all_weight_num = self.get_all_weight()
                test = all_head_test[self.weight_choice(all_weight_num)]
                for k in test_all_data:
                    if test in test_all_data[k]:
                        head = k

                print(test)
                test_count += 1
                self.test_show("Input you answer")
                result = input("The input==>")
                self.test_show("Are you sure? yes|no")
                choose = input("The input==>")
                if choose == "no":
                    result = input("The input==>")
                # pdb.set_trace()
                result = self.check_test_question(head, test, result)
                if result:
                    print("You are Right！")
                    self.reduce_the_weight(test)
                    correct_count += 1
                else:
                    print("Wrong answer！")
                    self.add_the_weight(test)
                    req_num = 0
                    while req_num < 2:
                        self.test_show("Whether to check the answer yes/no?")
                        choose = input("The input==>")
                        if choose == "yes":
                            req_num += 1
                            if req_num >= 2:
                                print(self.look_test_answer(test))
                            else:
                                print("Please Think again 10s!")
                                sleep(5)
                                continue
                        elif choose == "no":
                            break


            # 指定类别随机
            elif result == 'specified' or result == 's':
                choose_test = []
                for k in enumerate(list(self.appoint_test_question())):
                    choose_test.append(k)

                while True:
                    print("=" * 60)
                    for k in enumerate(list(self.appoint_test_question())):
                        print(k)
                    print("=" * 60)
                    self.test_show("Input you want learning test! or quit(q) or return(r)")
                    test_number = input("The input==>")

                    if test_number == "quit" or test_number == "q":
                        self.test_score(test_count, correct_count)
                        return

                    if test_number == "r" or test_number == "return":
                        break

                    if choose_test[int(test_number)]:
                        test_head = choose_test[int(test_number)]
                        head = test_head[1]
                        test_all_dict.update(test_all_data[head])
                        # test = random.choice(list(test_all_dict.keys()))
                        all_head_test = list(test_all_dict.keys())
                        all_weight_num = self.get_all_weight(head)
                        test = all_head_test[self.weight_choice(all_weight_num)]
                        print(test)
                        test_count += 1
                        self.test_show("Input you answer")
                        result = input("The input==>")
                        self.test_show("Are you sure? yes|no")
                        choose = input("The input==>")
                        if choose == "no":
                            result = input("The input==>")
                        result = self.check_test_question(head, test, result)

                        if result:
                            print("You are Right！")
                            self.reduce_the_weight(test)
                            correct_count += 1
                        else:
                            print("Wrong answer！")
                            self.add_the_weight(test)
                            req_num = 0
                            while req_num < 2:
                                self.test_show("Whether to check the answer yes/no?")
                                choose = input("The input==>")
                                if choose == "yes":
                                    req_num += 1
                                    if req_num >= 2:
                                        print(self.look_test_answer(test))
                                    else:
                                        print("Please Think again 10s !")
                                        sleep(5)
                                        continue
                                elif choose == "no":
                                    break
                    else:
                        print("Error! Please Input again")

            elif result == "quit":
                self.test_score(test_count, correct_count)
                return

            else:
                print("Error! Please Input again")

    # 错的试题增加权重，下次加强学习
    def add_the_weight(self, question):
        with open("./test_weight.py", encoding="utf-8") as f:
            try:
                test_data_dict = json.load(f)
            except Exception as e:
                print(e)
            test_heads = test_data_dict.keys()
            for test in test_heads:
                # pdb.set_trace()
                if test_data_dict[test].get(question) is not None:
                    weight = test_data_dict[test].get(question) + 1
                    test_data_dict[test][question] = weight
            test_data = test_data_dict
        with open("./test_weight.py", "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)

    # 对的试题减少权重，最小为1
    def reduce_the_weight(sel, question):
        with open("./test_weight.py", encoding="utf-8") as f:
            try:
                test_data_dict = json.load(f)
            except Exception as e:
                print(e)
            test_heads = test_data_dict.keys()
            for test in test_heads:
                # pdb.set_trace()
                if test_data_dict[test].get(question) is not None:
                    if test_data_dict[test].get(question) > 1:
                        weight = 1
                        test_data_dict[test][question] = weight
            test_data = test_data_dict

        with open("./test_weight.py", "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)

        pass

    # 测试打分
    def test_score(self, test, correct):
        print('answer %s correct %s percent: {:.1f}%'.format(test, correct, correct / test * 100))

    # 检查试题，关键字匹配
    def check_test_question(self, test_data, question, answer):
        all_test_keys = self.get_all_test_key()
        appoint_test = all_test_keys[test_data]
        flag = True
        for k in appoint_test:
            if question == k:
                # pdb.set_trace()
                for i in appoint_test[k].split("，"):
                    if i in answer:
                        pass
                    else:
                        flag = False
        return flag

    # 三次回答不上，查看答案
    def look_test_answer(self, question):
        all_test_data = self.get_all_test_question()
        all_test_head = all_test_data.keys()
        for head in all_test_head:
            answer = all_test_data[head].get(question)
            if answer:
                return answer

    # 展示请求
    def test_show(self, data):
        print("=" * 60)
        print(data.center(60))
        print("=" * 60)


test1 = TestTraining().random_open_test_question()
# test1 = TestTraining().add_the_weight("软件生命周期？")
# test1 = TestTraining().look_test_answer("软件生命周期？")
# print(test1)
