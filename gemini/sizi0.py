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

    def __init__(self, rows, cols, ln=4, black_first=True, record_flag=False):
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

    def step(self, c):
        if self.end:
            return False
        if c >= self.width or c < 0:
            return False
        r = len([_[c] for _ in self.board if _[c] != DEFAULT])
        if r >= self.height:
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


class SiziAgent:
    def __init__(self, me=WHITE):
        self.inner = None
        self.me = me

    def _copy(self, sizi: Sizi0):
        inner = Sizi0(sizi.height, sizi.width)
        inner.shuffle_board(sizi.board)
        inner.black_flag = sizi.black_flag
        return inner


class SiziRandomAgent(SiziAgent):
    def perform(self, sizi: Sizi0, *args, **kwargs):
        pot = random.choice(sizi.acts)
        return pot[1]


class Sizi1StepAgent(SiziAgent):

    def perform_process(self, sizi: Sizi0, ):
        self.inner = self._copy(sizi)
        # 一步就赢
        for act in self.inner.acts:
            inner = self._copy(self.inner)
            flag = inner.step(act[1])
            if inner.end:
                return [act[1]], 1
        # 避免一步输
        good_acts = []
        for act in self.inner.acts:
            inner = self._copy(self.inner)
            inner.step(act[1])
            good = True
            for nact in inner.acts:
                ninner = self._copy(inner)
                ninner.step(nact[1])
                if ninner.end:
                    good = False
                    break
            if good:
                good_acts.append(act[1])
        # 这里没辙了
        if len(good_acts) == 0:
            return [], -1
        if len(good_acts) == 1:
            return good_acts, 0
        #
        strict_acts = []
        for r in range(sizi.height):
            for c in range(sizi.width):
                p = sizi.board[r][c]
                if p == DEFAULT or p == self.me:
                    continue
                # 左右
                if (0 < c < sizi.width - 3
                    and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][c + 1] == p and sizi.board[r][
                        c + 2] == DEFAULT and sizi.board[r][c + 3] == DEFAULT and (
                            r == 0 or (sizi.board[r - 1][c - 1] != DEFAULT and sizi.board[r-1][
                        c + 2] != DEFAULT and sizi.board[r-1][c + 3] != DEFAULT))) \
                        or (1 < c < sizi.width - 2 and
                            sizi.board[r][c - 2] == DEFAULT and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][
                                c + 1] == p and sizi.board[r][c + 2] == DEFAULT and (r == 0 or (
                                sizi.board[r-1][c - 2] != DEFAULT and sizi.board[r-1][c - 1] != DEFAULT and sizi.board[r-1][
                            c + 2] != DEFAULT))):
                    strict_acts.append(c - 1)
                    strict_acts.append(c + 2)
                # 中间
                if 0 < c < sizi.width - 3 and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][c + 1] == DEFAULT and \
                        sizi.board[r][c + 2] == p and sizi.board[r][c + 3] == DEFAULT and (
                        r == 0 or sizi.board[r][c - 1] != DEFAULT and sizi.board[r][c + 1] != DEFAULT and sizi.board[r][
                    c + 3] != DEFAULT):
                    strict_acts.append(c - 1)
                    strict_acts.append(c + 1)
                    strict_acts.append(c + 3)
        if strict_acts:
            return strict_acts, 0
        #
        brilliant_acts = []
        for r in range(sizi.height):
            for c in range(sizi.width):
                p = sizi.board[r][c]
                if p != self.me:
                    continue
                # 左右
                if (0 < c < sizi.width - 3
                        and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][c + 1] == p and sizi.board[r][
                            c + 2] == DEFAULT and sizi.board[r][c + 3] == DEFAULT and (
                                r == 0 or (sizi.board[r - 1][c - 1] != DEFAULT and sizi.board[r][
                            c + 2] != DEFAULT and sizi.board[r][c + 3] != DEFAULT))):
                    brilliant_acts.append(c + 2)
                elif (1 < c < sizi.width - 2 and
                      sizi.board[r][c - 2] == DEFAULT and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][
                          c + 1] == p and sizi.board[r][c + 2] == DEFAULT and (r == 0 or (
                                sizi.board[r][c - 2] != DEFAULT and sizi.board[r][c - 1] != DEFAULT and sizi.board[r][
                            c + 2] != DEFAULT))):
                    brilliant_acts.append(c - 1)
                # 中间
                elif 0 < c < sizi.width - 3 and sizi.board[r][c - 1] == DEFAULT and sizi.board[r][c + 1] == DEFAULT and \
                        sizi.board[r][c + 2] == p and sizi.board[r][c + 3] == DEFAULT and (
                        r == 0 or sizi.board[r][c - 1] != DEFAULT and sizi.board[r][c + 1] != DEFAULT and sizi.board[r][
                    c + 3] != DEFAULT):
                    brilliant_acts.append(c + 1)
        if brilliant_acts:
            return brilliant_acts, 0
        return good_acts, 0

    def perform(self, sizi: Sizi0, *args, **kwargs):
        good_acts, flag = self.perform_process(sizi)
        if flag == -1:
            return random.choice(sizi.acts)[1]
        return random.choice(good_acts)


if __name__ == '__main__':
    # 输入坐标, 比如  "0,0"
    import random

    use_black = True

    agent = Sizi1StepAgent(me=WHITE if use_black else BLACK)
    sz = Sizi0(6, 8)

    # 下面这行代码, 启动后, 黑方一步获胜, 方便调试
    sz.board[0] = [0, 2, 2, 1, 1, 1, 2, 0]
    sz.board[1] = [0, 0, 0, 1, 0, 0, 0, 0]

    if not use_black:
        pot = agent.perform(sz)
        sz.step(pot)
    #
    while not sz.end:
        sz.print_board()
        print("========")

        while sz.black_flag == use_black:
            txt = input().strip()
            try:
                c = int(txt.split(",")[0])
            except:
                print(txt)
                continue
            sz.step(c)
        if sz.end:
            break
        #
        pot = agent.perform(sz)
        sz.step(pot)
    print("winner: ", sz.result)
    sz.print_board()
