# -*- coding: utf-8 -*-

import tornado
import memcache
import tornado.web
import tornado.gen
from system_logic.bo.object.Manager import Manager
from system_logic.po.WebMainPO import WebMainPO

mc = memcache.Client(['127.0.0.1:11211'])

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def get_login_status(self):

        if not self.get_secure_cookie('loginuser'):
            return False
        real_name = self.get_secure_cookie('loginuser')
        if not mc.get(real_name):
            return False
        return True

    def get_head_info(self, title, add_info=None):
        # 获取新事件
        count_new_user, count_new_msg, count_new_order = Manager().get_new_event()
        # 获取头像url
        profile_img = self.get_secure_cookie('profile_img')
        head_info = WebMainPO().handle_head_info(count_new_user, count_new_msg, count_new_order, title, profile_img, add_info)
        return head_info

    def refresh_session(self):

        real_name = self.get_secure_cookie('loginuser')
        mc.set(real_name, 1, time=1800)

    def log_out(self, *args, **kwargs):

        real_name = self.get_secure_cookie('loginuser')
        self.clear_all_cookies()
        mc.delete(real_name)
