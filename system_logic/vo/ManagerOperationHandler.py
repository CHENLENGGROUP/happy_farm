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
        if manager_id == 1:
            login_info = [
                {'login_ip':'112.10.134.299','login_time':'2017-08-08 14:35:03','country':'中国','province':'浙江','city':'杭州'},
                {'login_ip': '112.10.134.295', 'login_time': '2017-08-06 14:35:03', 'country': '中国', 'province': '浙江',
                 'city': '丽水'},
                {'login_ip': '112.10.134.293', 'login_time': '2017-08-01 14:35:03', 'country': '中国', 'province': '浙江',
                 'city': '温州'},
                {'login_ip': '112.10.134.291', 'login_time': '2017-08-02 14:35:03', 'country': '中国', 'province': '浙江',
                 'city': '宁波'},

            ]
            order_list = [
                {'order_sn':'123456789101','order_subtotal':'300','operation_type':'0','operation_time':'2017-08-01 15:22:22'},
                {'order_sn': '123456789103', 'order_subtotal': '2300', 'operation_type': '1',
                 'operation_time': '2017-08-02 15:22:22'},
                {'order_sn': '123456789105', 'order_subtotal': '100', 'operation_type': '0',
                 'operation_time': '2017-08-04 15:22:22'},
                {'order_sn': '123456789102', 'order_subtotal': '200', 'operation_type': '0',
                 'operation_time': '2017-08-06 15:22:22'},
            ]
            product_list = [
                {'product_sn': '1707030000061010', 'operation_type': '0', 'previous_data': '100', 'new_data': '200',
                 'operation_time': '2017-06-22 11:35'},
                {'product_sn': '1707030000061040', 'operation_type': '1', 'previous_data': '102', 'new_data': '202',
                 'operation_time': '2017-06-24 11:35'},

            ]
        self.render('manageroperation.html', head_info=head_info, product_list=product_list,login_info=login_info,order_list=order_list)