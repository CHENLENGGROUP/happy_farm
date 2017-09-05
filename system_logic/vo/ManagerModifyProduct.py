# -*- coding: utf-8 -*-

import json
import time
import types
import tornado
import memcache
import tornado.web
import tornado.ioloop
import tornado.gen
from system_logic import setting
from system_logic.vo.BaseHandler import BaseHandler
from system_logic.bo.object.Manager import Manager
from system_logic.vo.method.DecodeJson import _decode_dict
from system_logic.po.ManagerProductDetailPO import ManagerProductDetailPO
from system_logic.po.PageAddProductPO import PageAddProductPO

class ModifyProductHandler(BaseHandler):

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

        product_id = int(self.get_argument('product_id'))

        #获取商品信息
        product_info, count = Manager().browse_product({'hf_product.product_id=':product_id},1,None,0)
        product_info = product_info[0][0]

        #获取商品类型信息
        product_type = Manager().get_product_type({'product_type=':product_info['product_type']})[0]

        product_info['type_name'] = product_type['type_name']

        #获取分类信息
        category_list = Manager().get_category({'1=':1},' ORDER BY category_id ASC ')
        category_list = PageAddProductPO().handle_category_list(category_list)
        product_category = Manager().get_product_category({'product_id=':product_info['product_id']})
        product_category = PageAddProductPO().handle_category_list(product_category)
        category_list = PageAddProductPO().handle_category_list_disabled(category_list, product_category)

        #获取商品特性
        property_info = Manager().get_product_property({'product_id=':product_id,'is_delete=':0})
        property_str = ManagerProductDetailPO().handle_property_info(property_info)
        product_info['property_str'] = property_str

        head_info = self.get_head_info('商品明细',str(product_info['product_name']))

        self.refresh_session()
        self.render('product_modify.html', head_info=head_info, product_info=product_info,
                    category_list=category_list, product_category = product_category)

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
        result = Manager().modify_product(argus, manager_id)
        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}
        self.write(reMsg)