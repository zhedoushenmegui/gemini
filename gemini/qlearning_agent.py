#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/11/8
description:
history:
"""
import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.append(project_path)
import random
import traceback
import logging
from gemini.sizi0 import SiziAgent, WHITE, Sizi0, BLACK

logger = logging.getLogger()

class SiziQLearningAgent(SiziAgent):
    def __init__(self, mdl, cols, me=WHITE):
        """
        :param mdl: qtable 的路径
        :param me: 白棋还是黑棋
        :param cols:
        """
        super(SiziQLearningAgent, self).__init__(me)
        self.cols = cols
        self.name = mdl.split("/")[-1][:-7]
        #
        self.q_table = {}
        with open(mdl, "r") as f:
            cnt = f.read()
            arr = cnt.split("\n")
            try:
                for line in arr:
                    if len(line) == 0:
                        continue
                    brr = line.split(":")
                    s = eval(brr[0])
                    q = eval(brr[1])
                    self.q_table[s] = q
            except:
                print(traceback.format_exc())
                print(brr)
        print("size:", len(self.q_table))

    @staticmethod
    def arg_max(state_action):
        arr = [(i, v) for i, v in enumerate(state_action)]
        arr.sort(key=lambda t: t[1])
        return arr[-1][0]

    def _state_func(self, board):
        state = [i for row in board for i in row]
        left = [p for row in board for p in row[:self.cols // 2]]
        right = [p for row in board for p in row[-self.cols // 2:]]

        #
        state_reverse_flag = False
        if left < right:
            state_reverse_flag = True
            state = state[::-1]
        return tuple(state), state_reverse_flag

    def _action_func(self, action, reverse_flag=False):
        return self.cols - action - 1 if reverse_flag else action

    def perform(self, sizi: Sizi0, *args, **kwargs):
        state, reverse_flag = self._state_func(sizi.board)
        if state not in self.q_table:
            logger.info("q learning random")
            return random.choice(sizi.acts)[1]
        else:
            logger.info("q learning")
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
            action = self._action_func(action, reverse_flag)
            return action


if __name__ == '__main__':
    q_b_agent = SiziQLearningAgent(mdl=f"{project_path}/models/sizi_q_g0_teacher.121000.qtable", me=BLACK)
