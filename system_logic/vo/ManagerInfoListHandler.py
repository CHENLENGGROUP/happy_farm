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

class BrowseManagerListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('员工列表')

        manager_list = [
            {'manager_id':'1','username':'singlesjjj','real_name':'乔峰','authority':'1','telephone':'123456789','sex':'女','birthday':'1993-01-01','balance':'10.0',
             'credit':'100','last_login_ip':'112.10.134.299','last_login_time':'2017-08-08 14:35:02','register_time':'2017-06-22 11:35'},
            {'manager_id':'1','username': 'lengzhiyuan123', 'real_name':'虚竹','authority':'0','telephone': '11111111111', 'sex': '男', 'birthday': '1994-01-01',
             'balance': '11.0', 'credit': '101', 'last_login_ip': '112.10.134.297',
             'last_login_time': '2017-08-06 14:35:02', 'register_time': '2017-06-23 11:35'}

        ]
        self.render('managerlist.html', head_info=head_info,manager_list=manager_list)