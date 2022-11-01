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


class RandomAgent(tornado.web.RequestHandler):
    def post(self):
        resp = {}
        status = 0
        try:
            data = json.loads(self.request.body)
            board = data['board']

            from gemini.sizi0 import Sizi0, SiziRandomAgent, WHITE, BLACK
            use_black = data.get('use_black', True)
            sz = Sizi0()
            sz.shuffle_board(board)
            if sz.end:
                resp = {'action': -1, 'end': sz.end, "winner": sz.result}
            else:
                sz.black_flag = not use_black
                agent = SiziRandomAgent(me=WHITE if use_black else BLACK)
                action = agent.perform(sz)
                sz.step(action // sz.width, action % sz.width)
                resp = {'action': action, 'end':sz.end, "winner":sz.result}
        except:
            status = -1
            print(traceback.format_exc())
        rst = json.dumps({"status": status, "resp":resp})
        self.write(rst)


    def get(self):
        cnt = open(f"{project_path}/web/sizi_index.html", 'r').read()
        self.write(cnt)


class OneStepAgent(tornado.web.RequestHandler):
    def post(self):
        resp = {}
        status = 0
        try:
            data = json.loads(self.request.body)
            board = data['board']

            from gemini.sizi0 import Sizi0, Sizi1StepAgent, WHITE, BLACK
            use_black = data.get('use_black', True)
            sz = Sizi0()
            sz.shuffle_board(board)
            if sz.end:
                resp = {'action': -1, 'end': sz.end, "winner": sz.result}
            else:
                sz.black_flag = not use_black
                agent = Sizi1StepAgent(me=WHITE if use_black else BLACK)
                action = agent.perform(sz)
                sz.step(action // sz.width, action % sz.width)
                resp = {'action': action, 'end':sz.end, "winner":sz.result}
        except:
            status = -1
            print(traceback.format_exc())
        rst = json.dumps({"status": status, "resp":resp})
        self.write(rst)

    def get(self):
        cnt = open(f"{project_path}/web/sizi_index.html", 'r').read()
        self.write(cnt)


class Index(tornado.web.RequestHandler):
    def get(self):
        self.write("""
        <div><a href='/one_step'>one_step[use black]</a> </div>
        <div><a href='/random'>random[use black]</a> </div>
        <div><a href='/one_step#use_white'>one_step[use white]</a> </div>
        <div><a href='/random#use_white'>random[use white]</a> </div>
        """)


routes = [
    ("/", Index),
    ("/random", RandomAgent),
    ("/one_step", OneStepAgent)]

if __name__ == '__main__':
    application = tornado.web.Application(routes)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    ###
    port = 18020
    if len(sys.argv) == 2:
        port = int(sys.argv[1].strip())
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()
