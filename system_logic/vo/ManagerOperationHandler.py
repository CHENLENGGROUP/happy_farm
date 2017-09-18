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
from system_logic.po.WebManagerOperationPO import WebManagerOperationPo

class BrowseManagerOperationHanlder(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        manager_id = int(self.get_secure_cookie('loginuser_id'))
        real_name = self.get_secure_cookie('loginuser')
        head_info = self.get_head_info('员工明细',add_info=real_name)

        #获取登录日志
        login_log = Manager().get_login_log({'hf_manager.manager_id=':manager_id})
        #获取订单操作日志
        order_act_log = Manager().get_order_act_log({'hf_manager.manager_id=':manager_id})
        #获取商品操作日志
        product_act_log = Manager().get_product_act_log({'hf_manager.manager_id=':manager_id})

        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #获取消息阅读数
        msg_count_read, delta_date, date_list = Manager().get_count_manager(10,current_date, 1,
                                                              {'message_type_id=':1, 'reader_id=':manager_id},
                                                                                     'read_time', 'hf_message')
        #获取消息回复数
        msg_count_reply, delta_date, date_list = Manager().get_count_manager(10,current_date, 1,
                                                               {'message_type_id=':2, 'sender_id=':manager_id},
                                                                                      'send_time', 'hf_message')

        msg_chart_data_list = WebManagerOperationPo().handle_count_msg(msg_count_read,msg_count_reply,date_list)

        #获取订单操作数
        order_act_count, delta_date, date_list = Manager().get_count_manager(10, current_date, 1,
                                                                             {'manager_id=':manager_id},
                                                                             'act_time', 'hf_manager_actorder_log')
        order_chart_data_list = WebManagerOperationPo().handle_count_order(order_act_count, date_list)

        self.refresh_session()
        self.render('manageroperation.html', head_info=head_info, product_act_log=product_act_log,
                    login_log=login_log,order_act_log=order_act_log, msg_chart_data_list = msg_chart_data_list,
                    order_chart_data_list=order_chart_data_list)

class AddManagerHandler(BaseHandler):

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

        head_info = self.get_head_info('添加员工')

        self.render('addmanager.html', head_info=head_info)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''
        :param body
            :param username
            :param real_name
            :param password
            :param password_com
            :param telephone
            :param authority
        :return:
        '''
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        argus = _decode_dict(json.loads(self.request.body))
        manager_id = self.get_secure_cookie('loginuser_id')

        result = Manager().register(argus, manager_id)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        elif result == -3:
            reMsg = {'ret':setting.re_code['verify_error']}
        elif result == -4:
            reMsg = {'ret':setting.re_code['username_exist']}
        else:
            reMsg = {'ret':setting.re_code['success']}
        self.write(reMsg)
