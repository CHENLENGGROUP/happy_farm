<<<<<<< HEAD
# -*- coding: utf-8 -*-

import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic.vo.BaseHandler import BaseHandler

class ManagerLogOut(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        self.log_out()
=======
# -*- coding: utf-8 -*-

import tornado
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic.vo.BaseHandler import BaseHandler

class ManagerLogOut(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        self.log_out()
>>>>>>> dc5cf191e38ea9711dbc7643b5da028859ab8a09
        self.redirect('/managerlogin')