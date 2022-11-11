#!/usr/bin/env python
"""
author: yangchaogege
create date: 2022/10/31
description:
history:
"""
import sys
import os
import traceback

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
sys.path.append(project_path)

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
from gemini.sizi0 import Sizi0, WHITE, BLACK
from web.conf import cols, rows
from gemini.qlearning_agent import SiziQLearningAgent


class Agent(tornado.web.RequestHandler):
    def _perform(self, board, rows, cols, use_black, *args, **kwargs):
        action, end, result = None, None, None
        return action, end, result

    def post(self):
        status = 0
        try:
            data = json.loads(self.request.body)
            board = data['board']
            rows = data['rows']
            cols = data['cols']
            use_black = data.get('use_black', True)
            action, end, result = self._perform(board, rows, cols, use_black, data=data)
            resp = {'action': action, 'end': end, "winner": result}
        except:
            status = -1
            resp = {"msg": traceback.format_exc()}
            print(traceback.format_exc())
        rst = json.dumps({"status": status, "resp": resp})
        self.write(rst)

    def get(self):
        cnt = open(f"{project_path}/web/sizi_index.html", 'r').read()
        self.write(cnt)


class RandomAgent(Agent):
    def _perform(self, board, rows, cols, use_black, *args, **kwargs):
        from gemini.sizi0 import Sizi0, SiziRandomAgent, WHITE, BLACK
        sz = Sizi0(rows, cols)
        sz.shuffle_board(board)
        if sz.end:
            action = -1
        else:
            sz.black_flag = not use_black
            agent = SiziRandomAgent(me=WHITE if use_black else BLACK)
            action = agent.perform(sz)
            sz.step(action)
        return action, sz.end, sz.result


class OneStepAgent(Agent):
    def _perform(self, board, rows, cols, use_black, *args, **kwargs):
        from gemini.sizi0 import Sizi0, Sizi1StepAgent, WHITE, BLACK
        sz = Sizi0(rows, cols)
        sz.shuffle_board(board)
        if sz.end:
            action = -1
        else:
            sz.black_flag = not use_black
            agent = Sizi1StepAgent(me=WHITE if use_black else BLACK)
            action = agent.perform(sz)
            sz.step(action)
        return action, sz.end, sz.result


from web.conf import q_learning_models

q_w_agents = {}
for mdl in q_learning_models:
    w = SiziQLearningAgent(mdl=mdl, cols=cols, me=WHITE)
    q_w_agents[w.name] = w


class QLearningAgent(Agent):
    def _perform(self, board, rows, cols, use_black, *args, **kwargs):
        sz = Sizi0(rows, cols)
        sz.shuffle_board(board)
        if sz.end:
            action = -1
        else:
            sz.black_flag = not use_black
            data = kwargs['data']
            mdl = data['mdl']
            agent = q_w_agents[mdl]
            action = agent.perform(sz)
            sz.step(action)
        return action, sz.end, sz.result


class Index(tornado.web.RequestHandler):
    def get(self):
        modelsx = [f"<div><a href='/random'>random</a> </div>",
                   f"<div><a href='/random#use_white'>random[use white]</a> </div>",
                   f"<div><a href='/one_step'>one_step</a> </div>",
                   f"<div><a href='/one_step#use_white'>one_step[use white]</a> </div>",
                   ]
        for m in q_w_agents:
            modelsx.append(f"<div><a href='/q_learning?mdl={m}'>{m}</a> </div>")
            modelsx.append(f"<div><a href='/q_learning#use_white?mdl={m}'>{m}[use white]</a> </div>")
        self.write(
            "\n".join(modelsx)
        )


routes = [
    ("/", Index),
    ("/random", RandomAgent),
    ("/one_step", OneStepAgent),
    ("/q_learning", QLearningAgent),
]

if __name__ == '__main__':
    from web.log_util import set_logger
    set_logger("server.log")
    ###
    application = tornado.web.Application(routes)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    ###
    port = 18020
    if len(sys.argv) == 2:
        port = int(sys.argv[1].strip())
    http_server.listen(port)
    #
    import platform
    if platform.system().lower() == 'darwin':
        os.system(f"open 'http://localhost:{port}'")
    #
    tornado.ioloop.IOLoop.current().start()


