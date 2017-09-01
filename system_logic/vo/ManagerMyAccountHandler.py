# -*- coding: utf-8 -*-

import json
import time
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.vo.BaseHandler import BaseHandler
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseMyAccountHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('个人信息')
        manager_id = self.get_secure_cookie('loginuser_id')

        manager_info = Manager().get_login_log({'hf_manager.manager_id=':manager_id}, ' ORDER BY login_time DESC')
        manager_info = manager_info[0]

        self.refresh_session()
        self.render('myaccount.html', head_info=head_info,manager_info=manager_info)