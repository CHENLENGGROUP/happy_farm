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

class addArticletHandler(BaseHandler):

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

        head_info = self.get_head_info('添加文章')

        self.render('addarticle.html', head_info=head_info)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        '''
        :param body
            :param title
            :param subtitle
            :param brief
            :param content
            :param author
        :return:
        '''
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        author = self.get_secure_cookie('loginuser')

        argus = _decode_dict(json.loads(self.request.body))
        reMsg = {'ret':setting.re_code['success']}
        self.write(reMsg)