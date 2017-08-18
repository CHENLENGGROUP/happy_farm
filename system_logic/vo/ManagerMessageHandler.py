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
from system_logic.po.WebMessagePO import WebMessagePO
from system_logic.vo.method.DecodeJson import _decode_dict

class BrowseManagerMessageHanlder(BaseHandler):

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

        real_name = self.get_secure_cookie('loginuser')
        manager_id = int(self.get_secure_cookie('loginuser_id'))

        head_info = self.get_head_info('消息列表')

        condition = {}

        try:
            box_type = int(self.get_argument('box_type'))
        except:
            box_type = 1

        try:
            condition['is_read='] = int(self.get_argument('is_read'))
        except:
            pass
        page_number = 1

        condition, title_name = WebMessagePO().handle_input_condition(box_type,condition,manager_id)

        box_li_id = 'box_li_'+str(box_type)
        manager_info = {'real_name':real_name, 'img_url':head_info['profile_img']}
        supstring = 'ORDER BY is_read ASC, send_time DESC, is_important DESC'

        message_list, count = Manager().browse_message(condition,supstring,page_number, manager_id)
        page_count = count/10
        if count%10 != 0:
            page_count = page_count + 1

        result = Manager().get_manager({'1=':1})
        manager_list = WebMessagePO().handle_manager_list(result)

        self.refresh_session()
        self.render('message.html', head_info=head_info, message_list=message_list, manager_list=manager_list,
                    box_li_id=box_li_id,manager_info=manager_info, title_name=title_name,
                    page_count=page_count)

    def post(self, *args, **kwargs):

        manager_id = int(self.get_secure_cookie('loginuser_id'))
        post_args = _decode_dict(json.loads(self.request.body))
        condition ={}
        if post_args.has_key('is_read') and post_args['is_read']:
            condition['is_read='] = int(post_args['is_read'])
        box_type = int(post_args['box_type'])
        page_number = int(post_args['page_number'])
        supstring = 'ORDER BY is_read ASC, send_time DESC, is_important DESC'

        condition, title_name = WebMessagePO().handle_input_condition(box_type, condition, manager_id)

        message_list, count = Manager().browse_message(condition, supstring, page_number, manager_id)

        if message_list == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success'], 'message_list':message_list}

        self.write(reMsg)

class DeletaManagerMessageHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self, *args, **kwargs):
        '''

        :param message_id_list              消息id的list
        :return:
        '''
        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        argus = _decode_dict(json.loads(self.request.body))

        result = Manager().delete_message(argus['message_id_list'])

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class MarkManagerMessageReadedHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        argus = _decode_dict(json.loads(self.request.body))
        manager_id = self.get_secure_cookie('loginuser_id')
        result = Manager().mark_messageReaded(argus['message_id_list'],manager_id)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class MarkManagerMessageImportantHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        argus = _decode_dict(json.loads(self.request.body))

        result = Manager().mark_messageImportant(argus['message_id_list'])

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class ManagerSendMessageHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self, *args, **kwargs):

        post_args = _decode_dict(json.loads(self.request.body))
        manager_id = self.get_secure_cookie('loginuser_id')

        result = Manager().send_message(post_args, manager_id)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)

class BrowseMessgeDetailHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('消息列表')

        message_id = int(self.get_argument('message_id'))
        manager_id = self.get_secure_cookie('loginuser_id')
        condition = {'message_id=':message_id}
        message_info, count = Manager().browse_message(condition,'',1,manager_id)
        message_info = message_info[0]

        #标记此信息已读
        Manager().mark_messageReaded([message_id], manager_id)

        real_name = self.get_secure_cookie('loginuser')
        manager_info = {'real_name': real_name, 'img_url': head_info['profile_img']}
        manager_list = WebMessagePO().handle_manager_list(Manager().get_manager({'1=': 1}))

        for key in message_info:
            print key + ':' + str(message_info[key])

        self.refresh_session()
        self.render('messagedetail.html', head_info = head_info,message_info=message_info,
                    manager_info=manager_info, manager_list=manager_list)