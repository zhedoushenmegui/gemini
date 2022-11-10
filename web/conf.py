#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/11/10
description:
history:
"""
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
# sys.path.append(project_path)

cols = 8
rows = 6

# q learning models
q_learning_models = [f"{project_path}/models/{s}" for s in os.listdir(f"{project_path}/models") if s.endswith("qtable")]
