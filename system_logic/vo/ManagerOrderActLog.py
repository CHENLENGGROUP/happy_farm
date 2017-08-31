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
from system_logic.po.WebOrderActLogPO import WebOrderActLogPO
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseOrderActLog(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        order_id = self.get_argument('order_id')

        act_log_list_m = Manager().get_order_act_log({'hf_manager_actorder_log.order_id=':order_id})
        act_log_list_u = Manager().get_order_act_log_user({'hf_user_actorder_log.order_id=':order_id})

        if act_log_list_m != -1 and act_log_list_u != -1:
            act_log_list = WebOrderActLogPO().merge_two_order_act_log(act_log_list_m, act_log_list_u)
            reMsg = {'ret':setting.re_code['success'], 'act_log_list':act_log_list}
        else:
            reMsg = {'ret': setting.re_code['connect_error']}

        self.write(reMsg)
