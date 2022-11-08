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

from gemini.sizi0 import SiziAgent, WHITE, Sizi0,BLACK


class SiziQLearningAgent(SiziAgent):
    def __init__(self, mdl, me=WHITE):
        super(SiziQLearningAgent, self).__init__(me)
        assert me == BLACK

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
        arr = [(i,v) for v,i in enumerate(state_action)]
        arr.sort(key=lambda t:t[1])
        return arr[-1][0]

    def perform(self, sizi: Sizi0, *args, **kwargs):
        s = tuple([i for row in sizi.board for i in row])
        if s not in self.q_table:
            return random.choice(sizi.acts)[1]
        else:
            state_action = self.q_table[s]
            action = self.arg_max(state_action)
            return action


if __name__ == '__main__':
    q_b_agent = SiziQLearningAgent(mdl=f"{project_path}/models/sizi_q_g0_teacher.121000.qtable", me=BLACK)
