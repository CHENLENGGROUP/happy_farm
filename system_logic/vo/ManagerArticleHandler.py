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

class BrowseArticleListHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('文章列表')

        condition = {}
        supstring = ''
        search_item = ''
        try:
            page_number = self.get_argument('page_number')
        except:
            page_number = 1

        try:
            supstring = ' ORDER BY '+self.get_argument('sort_rule')
        except:
            pass
        try:
            search_item = str(self.get_argument('search_item'))
        except:
            pass
        if search_item != '':
            condition['title LIKE '] = '%%' + search_item + '%%'
        page_number = int(page_number)

        if condition == {}:
            condition = {'is_delete=':0}

        article_total, count = Manager().get_article(condition,page_number,supstring)
        if count%12!=0:
            page_count = count/12+1
        else:
            page_count = count/12

        self.refresh_session()
        self.render('articlelist.html', head_info=head_info,article_total=article_total,
                    page_count=page_count, page_number=page_number)

class BrowseArticleDetailHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('文章详细')

        article_list = [
            {'thumb_img_url':'../static/img/blog-6.jpg','title':'标题','subtitle':'副标题','brief':'摘要','content':'<p>你再瞅一个试试，试试就试试</p>，<p>我真TM无语了</p>','author':'作者','hits_count':'2','add_time':'2017-05-24'},
        ]
        self.render('articledetail.html', head_info=head_info,article_list=article_list)

class DeleteArticleHandler(BaseHandler):

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

        article_id = self.get_argument('article_id')

        condition = {'article_id=':article_id}

        result = Manager().delete_article(condition)

        if result == -1:
            reMsg = {'ret':setting.re_code['connect_error']}
        else:
            reMsg = {'ret':setting.re_code['success']}

        self.write(reMsg)
        