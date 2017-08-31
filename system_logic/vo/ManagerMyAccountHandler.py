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

class BrowseMyAccountHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('个人信息')

        manager_info = [
            {'username':'singlesjjj','password':'*******','real_name':'之轩','telephone':'13000001111','authority':'1','register_time':'2017-06-26 17:43:12','profile_pic_url':'../static/img/timg.jpg','last_login_time':'2017-08-31 20:25:03','last_login_ip':'127.0.0,1','country':'中国','province':'浙江','city':'杭州'},
        ]
        self.render('myaccount.html', head_info=head_info,manager_info=manager_info)