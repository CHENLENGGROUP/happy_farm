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
        self.redirect('/managerlogin')