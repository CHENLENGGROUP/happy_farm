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
from system_logic.po.PageAddProductPO import PageAddProductPO
from system_logic.vo.method.DecodeJson import _decode_dict

class AddProductHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        '''
        渲染添加商品页面
        :param args:
        :param kwargs:
        :return:
        '''
        #判断用户是否登录
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('添加商品')
        product_type_list = Manager().get_product_type()
        category_list = Manager().get_category({'1=':1},'ORDER BY category_id ASC')
        category_list = PageAddProductPO().handle_category_list(category_list)

        self.refresh_session()
        self.render('addproduct.html', head_info=head_info, product_type_list=product_type_list,
                    category_list=category_list)

    def post(self, *args, **kwargs):

        # 判断用户是否登录
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        manager_id = self.get_secure_cookie("loginuser_id")
        product_info = _decode_dict(json.loads(self.request.body))
        result, product_act_log_info = Manager().add_product(product_info, manager_id)
        Manager().add_product_log_act(product_act_log_info)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'product_id':result}

        self.refresh_session()
        self.write(reMsg)

class DeleteProductHandler(BaseHandler):

    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        product_id = int(self.get_argument('product_id'))
        manager_id = self.get_secure_cookie('loginuser_id')
        result = Manager().delete_product(product_id,manager_id)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)