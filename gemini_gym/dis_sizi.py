#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/10/28
description:
history:
"""
# import sys
# import os
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)
import logging

import gym
from gym import spaces
from gemini.sizi0 import Sizi0

logger = logging.getLogger()


class BaseAgent:
    def perform(self, *args, **kwargs):
        return None


class SiziModeling(gym.Env):
    def __init__(self, blue, red_first=True, rows=6, cols=8, *args, **kwargs):
        """
        red first 等价于 use black
        :param blue:
        :param red_first:
        :param rows:
        :param cols:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.cols = cols
        self.handler: Sizi0 = None
        #
        self.red_first = red_first
        self.state = None
        self.end = False
        self.info = {}
        #
        self.blue: BaseAgent = blue
        #
        self.actions = list(range(cols))
        #
        self.history = []
        #
        self.action_space = spaces.Discrete(cols)
        self.observation_space = spaces.MultiDiscrete([2] * rows * cols)

    def set_blue(self, blue):
        self.blue = blue
        self.reset()
        #

    def _state_func(self):
        self.state = [i for row in self.handler.board for i in row]
        return self.state

    def _end_func(self):
        self.end = self.handler.end
        if len(self.handler.acts) == 0:
            self.end = True

    def _reward_func(self):
        pass

    def _action_func(self, action):
        return action

    def _info_func(self):
        self.info = {"board": self.handler.board}
        return self.info

    def reset(self, *args, **kwargs):
        self.handler = Sizi0(rows=self.rows, cols=self.cols)
        if not self.red_first:
            action = self.blue.perform(self)
            col = self._action_func(action)
            flag = self.handler.step(col)
            if not flag:
                logger.info(f"blue agent failed")
                raise Exception("blue agent perform an invalid action")

        self._state_func()
        self._info_func()
        self.history = []
        self.history.append([[p for p in row] for row in self.handler.board])
        return self.state

    def step(self, action, *args, **kwargs):
        if action is None:
            return self.state, -10, self.end, self.info
        #
        flag = self.handler.step(action)

        if not flag:
            return self.state, -10, self.end, self.info

        self.history.append([[p for p in row] for row in self.handler.board])
        self._info_func()
        self._state_func()
        self._end_func()
        if self.handler.end:
            rew = 1000 if self.handler.result == 1 else -1000
            return self.state, rew, self.end, self.info
        #
        col = self.blue.perform(self)
        flag = self.handler.step(col)
        if not flag:
            logger.info(f"blue agent failed")
            logger.info(f"{col}")
            logger.info(f"{self.handler.board}")
            raise Exception("blue agent perform an invalid action")
        self.history.append([[p for p in row] for row in self.handler.board])
        self._info_func()
        self._state_func()
        self._end_func()
        if self.handler.end:
            rew = 1000 if self.handler.result == 1 else -1000
            return self.state, rew, self.end, self.info
        ###
        return self.state, 0, self.end, self.info
