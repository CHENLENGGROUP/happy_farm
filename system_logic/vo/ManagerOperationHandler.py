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
from system_logic.po.WebMessagePO import WebMessagePO
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseManagerOperationHanlder(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        manager_id = int(self.get_secure_cookie('loginuser_id'))

        head_info = self.get_head_info('员工列表')
        login_log = Manager().get_login_log({'hf_manager.manager_id=':manager_id})
        order_act_log = Manager().get_order_act_log({'hf_manager.manager_id=':manager_id})
        product_act_log = Manager().get_product_act_log({'hf_manager.manager_id=':manager_id})

        self.refresh_session()
        self.render('manageroperation.html', head_info=head_info, product_act_log=product_act_log, login_log=login_log,order_act_log=order_act_log)

class AddManagerHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return