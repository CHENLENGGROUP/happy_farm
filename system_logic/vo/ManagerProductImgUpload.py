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
from system_logic.po.UploadImg import UploadImg
from system_logic.po.EncryptString import EncryptString

class UploadProductImg(BaseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        argus = _decode_dict(json.loads(self.request.body))
        sequence_num = argus['sequence_num']
        product_id = argus['product_id']
        try:
            base64str = argus['base64_str']
            # 储存图片
            en_base64 = EncryptString().encrypt_string(base64str)
            file_name = en_base64+ '.jpg'
            store_address = '../static/img/product_img/' + file_name
            s_add = UploadImg().create_img(base64str, store_address)
        except:
            s_add = argus['img_url']

        #更新图片
        condition = {'product_id=':int(product_id),'sequence_num=':int(sequence_num)}
        update_item = {'img_url':s_add}
        result = Manager().update_product_img(condition, update_item)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)