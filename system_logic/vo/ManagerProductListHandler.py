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

        condition = {}
        supstring = None
        search_item = ''
        try:
            page_number = self.get_argument('page_number')
        except:
            page_number = 1
        try:
            if(int(self.get_argument('category_id'))!=0):
                condition['category_id='] = int(self.get_argument('category_id'))
        except:
            pass
        try:
            supstring = self.get_argument('sort_rule')
        except:
            pass
        try:
            search_item = str(self.get_argument('search_item'))
        except:
            pass
        if search_item != '':
            try:
                search_item = int(search_item)
                search_len = len(str(search_item))
                if search_len == 16:
                    condition['product_sn='] = int(search_item)
                else:
                    condition['product_name LIKE'] = '%%'+str(search_item)+'%%'
            except:
                condition['product_name LIKE'] = '%%'+search_item+'%%'
        page_number = int(page_number)

        if condition.has_key('category_id='):
            product_total, count = Manager().browse_product_by_category(condition, page_number, supstring)
        else:
            product_total, count = Manager().browse_product(condition, page_number, supstring)
        category_list = Manager().get_category({'1=':1},' ORDER BY category_id ASC ')
        if count%12!=0:
            page_count = count/12+1
        else:
            page_count = count/12
        # reMsg = {'product_list':product_total, 'count':count}
        # self.write(reMsg)

        self.refresh_session()
        self.render('productlist.html', head_info=head_info,product_total=product_total,
                    category_list=category_list, page_count=page_count, page_number=page_number)