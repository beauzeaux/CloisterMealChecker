#!/usr/bin/env python2
import thread
import json
import time

import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado
from tornado import *
from tornado.gen import *

from swipe import get_swipe

from models import Person, Swipe, GuestSwipe, Blacklist, person_by_id

class SwipeHandler(tornado.websocket.WebSocketHandler):
    participents = set()
    guestSwipe = False
    
    @tornado.web.asynchronous
    def open(self):
        self.participents.add(self)  # add to the participents
        self.guestSwipe = False
        
    @tornado.web.asynchronous
    def on_message(self, message):
        pass;

    @tornado.web.asynchronous
    def on_close(self):
        self.participents.remove(self)
        
    @tornado.web.asynchronous
    def swipe(self, swipe):
        swipe["type"] = "swipe"
        out = json.dumps(swipe);
        self.write_message(out)

    @classmethod
    def broadcast_message(cls, msg):
        for p in cls.participents:
            p.write_message(msg);
        
    @classmethod
    def broadcast_swipe(cls, swipe):
        for p in cls.participents:
            p.swipe(swipe)
            

application = tornado.web.Application([
    (r'/ws', SwipeHandler),
])

def swipe_loop():
    print("Swipe loop started");
    while True:
        swipe = get_swipe()
        def callback():
            SwipeHandler.broadcast_swipe(swipe)
            
        tornado.ioloop.IOLoop.instance().add_callback(callback)

def keep_alive_loop(timeout):
    print("Keep alive loop started");
    while True:
        time.sleep(timeout);
        def callback():
            SwipeHandler.broadcast_message("keep-alive")

        tornado.ioloop.IOLoop.instance().add_callback(callback)
        
    
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    thread.start_new_thread(swipe_loop, ())
    thread.start_new_thread(keep_alive_loop, (3, ))
    tornado.ioloop.IOLoop.instance().start()

