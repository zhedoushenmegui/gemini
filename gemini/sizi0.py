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
BLACK = 1
WHITE = 2


class Sizi0:
    """
    一个四子棋引擎
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
        self.acts = [[r, c] for r in range(self.height) for c in range(self.width) if
                     self.board[r][c] == 0 and (r == 0 or self.board[r - 1][c] != 0)]
        #
        self.end = False
        self.result = 0

    def step(self, r, c):
        if self.end:
            return False
        if c >= self.width or c < 0:
            return False
        if r >= self.height or r < 0:
            return False
        if self.board[r][c] != 0:
            return False
        if r > 0 and self.board[r - 1][c] == 0:
            return False

        #
        pot = BLACK if self.black_flag else WHITE
        self.board[r][c] = pot
        self.black_flag = not self.black_flag
        #
        self.check(r, c, pot)
        #
        if self.record_flag:
            self.records.append((self.stepn, r, c, pot,))
        #
        self.stepn += 1
        #
        return True

    def check(self, r, c, pot):
        # 换个思路
        tobe_check = [
            [(r - i, c) for i in range(self.ln) if 0 <= r - i < self.width],
            [(r, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.height],
            [(r + i, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.height and 0 <= r + i < self.width],
            [(r - i, c + i) for i in range(-self.ln, self.ln) if 0 <= c + i < self.height and 0 <= r - i < self.width],
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
        self.acts = [[r, c] for r in range(self.height) for c in range(self.width) if
                     self.board[r][c] == 0 and (r == 0 or self.board[r - 1][c] != 0)]
        if len(self.acts) == 0:
            self.end = True

    def print_board(self):
        for row in self.board[::-1]:
            print(row)


if __name__ == '__main__':
    import random

    sz = Sizi0()
    sz.board[0] = [1, 1, 1, 0, 0, 0]
    while not sz.end:
        sz.print_board()
        while sz.black_flag:
            txt = input()
            r = int(txt.split(",")[0])
            c = int(txt.split(",")[1])

            sz.step(r, c)
        if sz.end:
            break
        #
        pot = random.choice(sz.acts)
        sz.step(*pot)
    print("winner: ", sz.result)
