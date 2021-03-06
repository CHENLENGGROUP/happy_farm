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
from system_logic.po.WebProductAnalysisPO import WebProductAnalysisPO

class BrowseOrderHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        try:
            if not self.get_login_status():
                self.redirect('/managerlogin')
                return

            head_info = self.get_head_info('订单列表')

            order_list = Manager().get_order({'1=':1})

            self.refresh_session()
            self.render('order_list.html',head_info=head_info, order_list=order_list)

        except Exception as e:
            self.render('404.html',error_reason=e)


class ConfirmOrderHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        order_id = self.get_argument('order_id')
        update_item = {'order_status':1}
        result = Manager().update_order({'order_id=':order_id}, update_item)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)