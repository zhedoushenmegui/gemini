#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/10/27
description:
history:
"""
# import sys
# import os
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)
import random

DEFAULT = 0
BLACK = 1
WHITE = 2


class Sizi0:
    """
    一个四子棋引擎
    四子棋的规则:
    1. 连续四个同色棋子(横/竖/斜着) 结束;
    2. 除了第一行,每个落子的下方都要有棋子;
    """

    def __init__(self, rows=6, cols=6, ln=4, black_first=True, record_flag=False):
        assert cols >= 6
        assert rows >= 6
        assert ln > 2
        #
        self.board = [[0] * cols for i in range(rows)]
        self.width = cols
        self.height = rows
        #
        self.ln = ln
        #
        self.stepn = 0
        # 执黑先行 且黑为1 白为2
        self.black_flag = black_first
        # 记录
        self.record_flag = record_flag
        self.records = []
        self.acts = []
        self.cal_acts()
        #
        self.end = False
        self.result = DEFAULT

    def shuffle_board(self, board):
        self.board = [[p for p in row] for row in board]
        assert len(board) > 0
        self.height = len(board)
        self.width = len(board[0])
        self.global_check()
        self.cal_acts()

    def global_check(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] != DEFAULT:
                    self.check(r, c)
                if self.end:
                    return

    def cal_acts(self):
        self.acts = [(r, c) for r in range(self.height) for c in range(self.width) if
                     self.board[r][c] == DEFAULT and (r == 0 or self.board[r - 1][c] != DEFAULT)]

    def step(self, r, c):
        if self.end:
            return False
        if c >= self.width or c < 0:
            return False
        if r >= self.height or r < 0:
            return False
        if self.board[r][c] != DEFAULT:
            return False
        if r > 0 and self.board[r - 1][c] == DEFAULT:
            return False

        #
        pot = BLACK if self.black_flag else WHITE
        self.board[r][c] = pot
        self.black_flag = not self.black_flag
        #
        self.check(r, c)
        #
        if self.record_flag:
            self.records.append((self.stepn, r, c, pot,))
        #
        self.stepn += 1
        #
        return True

    def check(self, r, c, *args, **kwargs):
        pot = self.board[r][c]
        # 换个思路
        tobe_check = [
            [(r - i, c) for i in range(self.ln) if 0 <= r - i < self.height],
            [(r, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.width],
            [(r + i, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.width and 0 <= r + i < self.height],
            [(r - i, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.width and 0 <= r - i < self.height],
        ]
        for arr in tobe_check:
            if len(arr) < self.ln: continue
            l = 0
            for p in arr:
                if self.board[p[0]][p[1]] == pot:
                    l += 1
                    if l >= self.ln:
                        break
                else:
                    l = 0
            #
            if l >= self.ln:
                self.end = True
                self.result = pot
        #
        self.cal_acts()
        if len(self.acts) == 0:
            self.end = True
            self.black_flag = None

    def print_board(self):
        for row in self.board[::-1]:
            print(row)


class SiziRandomAgent:
    def __init__(self, *args, **kwargs):
        pass

    def perform(self, sizi: Sizi0, *args, **kwargs):
        pot = random.choice(sizi.acts)
        actioni = pot[0] * sizi.width + pot[1]
        return actioni


class Sizi1StepAgent:
    def __init__(self, me=WHITE):
        self.inner = Sizi0()
        self.me = me

    def _copy(self, sizi: Sizi0):
        inner = Sizi0(sizi.height, sizi.width)
        inner.board = [[p for p in row] for row in sizi.board]
        inner.cal_acts()
        inner.black_flag = sizi.black_flag
        return inner

    def perform(self, sizi: Sizi0, *args, **kwargs):
        self.inner = self._copy(sizi)
        # 一步就赢
        for act in self.inner.acts:
            inner = self._copy(self.inner)
            row, col = act
            flag = inner.step(row, col)
            if inner.end:
                action = row * sizi.width + col
                return action

        # 避免一步输
        good_acts = []
        for act in self.inner.acts:
            inner = self._copy(self.inner)
            row, col = act
            flag = inner.step(row, col)
            next_acts = inner.acts
            good = True
            for nact in next_acts:
                ninner = self._copy(inner)
                row, col = nact
                flag = ninner.step(row, col)
                if ninner.end:
                    good = False
                    break
            if good:
                good_acts.append(act)
        # 这里没辙了
        if len(good_acts) == 0:
            good_acts = self.inner.acts
        # 随机
        act = random.choice(good_acts)
        row, col = act
        action = row * sizi.width + col
        return action


if __name__ == '__main__':
    # 输入坐标, 比如  "0,0"
    import random

    use_black = False

    agent = Sizi1StepAgent(me=WHITE if use_black else BLACK)
    sz = Sizi0()

    # 下面这行代码, 启动后, 黑方一步获胜, 方便调试
    # sz.board[0] = [BLACK, BLACK, BLACK, DEFAULT, DEFAULT, DEFAULT]
    if not use_black:
        pot = agent.perform(sz)
        sz.step(pot // sz.width, pot % sz.width)
    #
    while not sz.end:
        sz.print_board()
        print("========")

        while sz.black_flag == use_black:
            txt = input().strip()
            try:
                r = int(txt.split(",")[0])
                c = int(txt.split(",")[1])
            except:
                print(txt)
                continue
            if (r, c) not in sz.acts:
                print("invalid input, re input:")
                continue
            sz.step(r, c)
        if sz.end:
            break
        #
        pot = agent.perform(sz)
        sz.step(pot // sz.width, pot % sz.width)
    print("winner: ", sz.result)
    sz.print_board()
