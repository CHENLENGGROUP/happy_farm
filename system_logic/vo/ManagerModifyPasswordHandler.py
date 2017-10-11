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
from system_logic.po.EncryptString import EncryptString

class ModifyPasswordHandler(BaseHandler):

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

        head_info = self.get_head_info('修改密码')

        self.refresh_session()
        self.render('password_modify.html', head_info=head_info)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        try:
            argus = _decode_dict(json.loads(self.request.body))
            for key in argus:
                argus[key] = EncryptString().encrypt_string(argus[key])

            manager_id = self.get_secure_cookie('loginuser_id')
            old_passwd = Manager().get_manager({'manager_id=':manager_id})[0]['passwd']

            #验证密码输入是否正确
            if argus['old_passwd'] != old_passwd:
                reMsg = {'ret':setting.re_code['passwd_incorrect']}
            else:
                update_item = {'passwd':argus['new_passwd']}
                condition = {'manager_id=':manager_id}
                result = Manager().update_manager(condition,update_item)
                if result == -1:
                    reMsg = {'ret':setting.re_code['connect_error']}
                else:
                    reMsg = {'ret':setting.re_code['success']}

            self.write(reMsg)

        except Exception as e:
            reMsg = {'ret':setting.re_code['connect_error']}
            self.write(reMsg)


