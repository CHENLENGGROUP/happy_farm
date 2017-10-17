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

class BrowseManagerListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('员工列表')

        manager_list = Manager().get_manager({'is_delete=':0})

        self.refresh_session()
        self.render('managerlist.html', head_info=head_info,manager_list=manager_list)

class DeleteManagerHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        login_manager_id = self.get_secure_cookie('loginuser_id')
        manager_id = self.get_argument('manager_id')

        result = Manager().delete_manager(login_manager_id,{'manager_id=':manager_id})

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result ==-2:
            reMsg = {'ret':setting.re_code['authority_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)
