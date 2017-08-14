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

class BrowseProductListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('商品列表')
        try:
            category_id = int(self.get_argument('category_id'))
        except:
            category_id = 0

        try:
            count = int(self.get_argument('count'))
        except:
            count = None

        try:
            page_number = int(self.get_argument('page_number'))
        except:
            page_number = 1

        try:
            sort_by = int(self.get_argument('sort_by'))
        except:
            sort_by = 0

        try:
            search_content = self.get_argument('search_content')
        except:
            search_content = ""

        product_list = []

        count = 48

        category_list = [
            {'category_id':'1','category_content':'动物','parent_category_id':'0','is_delete':0},
            {'category_id': '2', 'category_content': '植物', 'parent_category_id': '0', 'is_delete': 0},
            {'category_id': '3', 'category_content': '蔬菜', 'parent_category_id': '2', 'is_delete': 0},
            {'category_id': '4', 'category_content': '水果', 'parent_category_id': '2', 'is_delete': 0},
            {'category_id': '5', 'category_content': '猪', 'parent_category_id': '1', 'is_delete': 0},
            {'category_id': '6', 'category_content': '牛', 'parent_category_id': '1', 'is_delete': 0},
            {'category_id': '7', 'category_content': '羊', 'parent_category_id': '1', 'is_delete': 0},
        ]
        if category_id == 1:
            product_list = [
                {'product_name': 'p_name', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                 'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20','category_id':'1'},
                {'product_name': 'p_name1', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                 'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20','category_id':'1'},
                {'product_name': 'p_name5', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                 'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20','category_id':'1'},
                {'product_name': 'p_name7', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                 'thumb_img_url': '../static/dist/img/chair.jpg','shop_price':'20','category_id':'1'},

            ]
        elif category_id == 2:
            if sort_by == 1:
                product_list = [
                    {'product_name': 'p_name2', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                     'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2'},
                    {'product_name': 'p_name3', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                     'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2'},
                    {'product_name': 'p_name4', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                     'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2'},
                    {'product_name': 'p_name6', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                     'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2'},
                ]
        else:
            if page_number == 1:
                if search_content == "aaaa":
                    product_list = [
                        {'product_name': 'p_name', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '1','product_id':'2'},
                        {'product_name': 'p_name1', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '1','product_id':'3'},
                        {'product_name': 'p_name5', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '1','product_id':'4'},
                        {'product_name': 'p_name7', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '1','product_id':'5'},
                        {'product_name': 'p_name2', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2','product_id':'6'},
                        {'product_name': 'p_name3', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2','product_id':'7'},
                        {'product_name': 'p_name4', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2','product_id':'8'},
                        {'product_name': 'p_name6', 'product_sn': '987654321', 'brief': 'yy', 'description': 'yyd',
                         'thumb_img_url': '../static/dist/img/chair.jpg', 'shop_price': '20', 'category_id': '2','product_id':'1'},
                    ]
                    category_id = 0
        self.render('productlist.html', head_info=head_info,product_list=product_list,category_list=category_list,category_id=category_id,count=count,page_number=page_number,sort_by=sort_by,search_content=search_content)