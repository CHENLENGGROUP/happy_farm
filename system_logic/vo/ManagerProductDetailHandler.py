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

class BrowseProductDetailHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('商品明细')

        try:
            product_id = int(self.get_argument('product_id'))
        except:
            product_id = None

        if product_id == 2:
            product_list = [
                {'product_id':'2','product_name': 'p_name2', 'shop_price':'123', 'brief': 'lallalalkklsdfjklsdf', 'description': 'Activist, criteria planned giving dignity, committed democratizing the global financial system progressive. Nelson Mandela equal opportunity change accelerate pathway to a better life invest our ambitions catalyst. Making progress contribution compassion Ford Foundation, cross-agency coordination Bill and Melinda Gates development. Overcome injustice tackling activism, promising development equality hack meaningful working families. Foundation; open source; organization volunteer, replicable think tank carbon emissions reductions.',
                 'stock': '10', 'thumb_img_url':''},
            ]

            property_list = [
                {'property_content':'1.5斤','property_name':'重量'},
                {'property_content': '高山羊', 'property_name': '品种'},

            ]

        self.render('productdetail.html', head_info=head_info)