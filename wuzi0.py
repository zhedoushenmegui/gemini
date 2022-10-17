#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/10/14
description:
history:
"""
# import sys
# import os
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)
import random

BLACK = 1
WHITE = 2


class Wuzi0:
    def __init__(self, s, ln=5, black_first=True, record_flag=False):
        self.width = self.height = s
        self.board = [[0] * s for i in range(s)]
        #
        self.stepn = 0
        # 执黑先行 且黑为1 白为2
        self.black_flag = black_first
        # 记录
        self.record_flag = record_flag
        self.records = []
        #
        self.end = False
        self.result = 0
        #
        self.ln = ln
        self.to_check_idx = []
        self._prepare()
        self.win_idx = []

    def step(self, r, c):
        if self.end:
            return False
        if c >= self.width:
            return False
        if r >= self.height:
            return False
        if self.board[r][c] != 0:
            return False
        # 1 黑 2白
        pot = BLACK if self.black_flag else WHITE
        self.board[r][c] = pot

        self.black_flag = not self.black_flag
        #
        self.check()
        #
        if self.record_flag:
            self.records.append((self.stepn, r, c, pot,))
        #
        self.stepn += 1
        #
        return True

    def _prepare(self):
        for rowi in range(self.height):
            row = []
            for coli in range(self.width):
                row.append((rowi, coli))
            self.to_check_idx.append(row)
        ###
        for coli in range(self.width):
            col = []
            for rowi in range(self.height):
                col.append((coli, rowi))
            self.to_check_idx.append(col)
        #
        rowstart = 0
        colstart = self.width - 1
        for i in range(self.width):
            arr = []
            for j in range(self.width):
                rowi = rowstart + j
                coli = colstart + j - i
                if 0 <= rowi < self.width and 0 <= coli < self.height:
                    arr.append((rowi, coli))
                else:
                    break
            if len(arr) >= self.ln:
                self.to_check_idx.append(arr)
        #
        rowstart = 0
        colstart = 0
        for i in range(self.width):
            arr = []
            for j in range(self.width):
                rowi = rowstart + j + i
                coli = colstart + j
                if 0 <= rowi < self.width and 0 <= coli < self.height:
                    arr.append((rowi, coli))
                else:
                    break
            if len(arr) >= self.ln:
                self.to_check_idx.append(arr)
        #
        rowstart = 0
        colstart = 0
        for i in range(self.width):
            arr = []
            for j in range(self.width):
                rowi = rowstart + j
                coli = colstart - j + i
                if 0 <= rowi < self.width and 0 <= coli < self.height:
                    arr.append((rowi, coli))
                else:
                    break
            if len(arr) >= self.ln:
                self.to_check_idx.append(arr)
        #
        rowstart = 0
        colstart = self.width - 1
        for i in range(self.width):
            arr = []
            for j in range(self.width):
                rowi = rowstart + j + i
                coli = colstart - j
                if 0 <= rowi < self.width and 0 <= coli < self.height:
                    arr.append((rowi, coli))
                else:
                    break
            if len(arr) >= self.ln:
                self.to_check_idx.append(arr)

    def _check_process(self, arr):
        cur = 0
        n = 0
        for pot in arr:
            if pot == 0:
                n = 0
            elif pot == cur:
                n += 1
            else:
                cur = pot
                n = 1
            if n >= self.ln:
                return pot
        return None

    def check(self):
        # None 表示继续
        for arr in self.to_check_idx:
            to_check = [self.board[tp[0]][tp[1]] for tp in arr]
            flag = None
            flag = self._check_process(to_check)
            # flag is not None 结束,判定胜负
            if flag is not None:
                winner = flag
                self.end = True
                self.result = winner
                self.win_idx = arr
                return
        ###
        acts = [[r, c] for r in range(self.height) for c in range(self.width) if self.board[r][c] == 0]
        if len(acts) == 0:
            self.end = True

    def pprint(self):
        for row in self.board:
            print(row)
        print(self.win_idx)


if __name__ == '__main__':
    sz = 10
    wz = Wuzi0(sz, record_flag=True)
    print(wz.board)
    while not wz.end:
        acts = [[r, c] for r in range(sz) for c in range(sz) if wz.board[r][c] == 0]
        act = random.choice(acts)
        wz.step(*act)
    wz.pprint()
    print(wz.result)
    print(wz.records)

