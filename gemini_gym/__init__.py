#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/11/8
description:
history:
"""
# import sys
# import os
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)

import gym

from gym.envs.registration import register


register(id="sizi-v0",
         entry_point="modeling:SiziModeling",
         max_episode_steps=100000,
         reward_threshold=999)

__all__ = ['gym']