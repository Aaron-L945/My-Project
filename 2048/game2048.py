# !/usr/bin/env python
# -*- coding:utf-8 -*-
import random


class Game:
    def __init__(self):
        self.scores = 0  # 分数
        # 用一个嵌套列表来表示数字方块
        self.board_list = [
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.restart()  # 回调函数，初始化
        self.empty_board = set([])  # 空白位置

    # 重新
    def restart(self):
        self.board_list = [
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]
        self.scores = 0
        while True:  # 添加2个随机的数
            t1 = (random.randint(0, 3), random.randint(0, 3))
            t2 = (random.randint(0, 3), random.randint(0, 3))
            if t1 != t2:
                break
        self.board_list[t1[0]][t1[1]] = random.randrange(2, 5, 2)
        self.board_list[t2[0]][t2[1]] = random.randrange(2, 5, 2)

    def move_left(self):
        for i in range(4):
            self.board_list[i] = self.row_left_oper(self.board_list[i])

    def move_right(self):
        for i in range(4):
            self.board_list[i].reverse()  # 反向每一行
            self.board_list[i] = self.row_left_oper(self.board_list[i])
            self.board_list[i].reverse()  # 反向

    def move_down(self):
        self.board_list = self.turn_right(self.board_list)
        self.move_left()
        self.board_list = self.turn_left(self.board_list)

    def move_up(self):
        self.board_list = self.turn_left(self.board_list)
        self.move_left()
        self.board_list = self.turn_right(self.board_list)

    def row_left_oper(self, row):
        temp = []
        # 先挤到一起
        for item in row:
            if item != ' ':
                temp.append(item)
        new_row = []
        flag = True
        for i in range(len(temp)):

            if flag:
                if i+1 < len(temp) and temp[i] == temp[i+1]:
                    new_row.append(temp[i]*2)
                    flag = False
                    self.scores += temp[i]*2
                else:
                    new_row.append(temp[i])
            else:
                flag = True
        n = len(new_row)
        # 补齐
        for i in range(len(row) - n):
            new_row.append(' ')

        return new_row

    def is_win(self):
        # 添加了一个功能 更新 空白位置
        self.empty_board.clear()
        for i in range(4):
            for j in range(4):
                if self.board_list[i][j] == 2048:
                    return True
                elif self.board_list[i][j] == ' ':
                    self.empty_board.add((i, j))

    def is_game_over(self):
        # 所有的格子都占满
        # 每一行，每一列，没有相同
        flag = True
        if len(self.empty_board) == 0:
            for l in self.board_list:
                for i in range(len(l)-1):
                    if l[i] == l[i+1]:
                        flag = False
            for l in self.turn_right(self.board_list):
                for i in range(len(l)-1):
                    if l[i] == l[i+1]:
                        flag = False
        else:
            flag = False
        return flag

    def turn_right(self, matrix):
        return [list(x)[::-1] for x in zip(*matrix)]

    def turn_left(self, matrix):
        temp = self.turn_right(self.turn_right(matrix))
        return self.turn_right(temp)

    # 随机添加方块
    def add_board(self):

        for i in range(2):
            try:
                temp = temp = self.empty_board.pop()
                self.board_list[temp[0]][temp[1]] = random.randrange(2, 5, 2)
            except:
                break

    def start(self):
        while True:
            self.print_game_board()
            code = input('请输入指令>>>>:')
            if code == 'w':
                self.move_up()
            elif code == 's':
                self.move_down()
            elif code == 'a':
                self.move_left()
            elif code == 'd':
                self.move_right()
            elif code == 'r':
                self.restart()
                continue
            elif code == 'q':
                exit('退出')
            else:
                print('请输入正确的指令！')
                continue

            if self.is_win():
                print('游戏得分%s' % self.scores)
                print('恭喜你，赢得游戏！')
                break
            if self.is_game_over():
                exit('gameover')
            self.add_board()

    def print_game_board(self):
        game_str = """
        SCORE:{}
        +-----+-----+-----+-----+
        |{: ^5}|{: ^5}|{: ^5}|{: ^5}|
        +-----+-----+-----+-----+
        |{: ^5}|{: ^5}|{: ^5}|{: ^5}|
        +-----+-----+-----+-----+
        |{: ^5}|{: ^5}|{: ^5}|{: ^5}|
        +-----+-----+-----+-----+
        |{: ^5}|{: ^5}|{: ^5}|{: ^5}| 
        +-----+-----+-----+-----+
        w(up),s(down),a(left),d(right)
             r(restart),q(exit)
        """.format(self.scores,
                   *self.board_list[0],
                   *self.board_list[1],
                   *self.board_list[2],
                   *self.board_list[3],
                   )
        print(game_str)


if __name__ == '__main__':
    game = Game()

    game.start()
