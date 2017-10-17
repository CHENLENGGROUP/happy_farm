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
from system_logic.po.WebUserAnalysisPO import WebUserAnalysisPO

class BrowseUserAnalysisHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        head_info = self.get_head_info('用户分析')
        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        try:
            #获取昨日新增用户
            new_user_list = Manager().get_count_manager(3,current_date,1,{'1=':1},'register_time','hf_user')[0]
            new_user_yes, increase_rate = WebUserAnalysisPO().handle_increase_rate(new_user_list[1],new_user_list[2])
            new_user_info = {'new_data':new_user_yes,'increase_rate':increase_rate}

            #获取昨日访问
            visit_list = Manager().get_count_manager(3,current_date,1,{'1=':1},'login_time','hf_login_log_user')[0]
            visit_yes, increase_rate = WebUserAnalysisPO().handle_increase_rate(visit_list[1], visit_list[2])
            new_visit_info = {'new_data':visit_yes,'increase_rate':increase_rate}

            #获取昨日订单
            new_order_list = Manager().get_count_manager(3,current_date,1,{'1=':1},'create_time','hf_order')[0]
            order_yes, increase_rate = WebUserAnalysisPO().handle_increase_rate(new_order_list[1],new_order_list[2])
            new_order_info = {'new_data':order_yes,'increase_rate':increase_rate}

            #获取性别比例
            sex_property_list = []
            sex_lable_list = ['男','女', ' ']
            for item in sex_lable_list:
                condition = {'sex = ':item}
                result = Manager().count_user(condition)
                sex_property_list.append(int(result[0]['COUNT(*)']))
            sex_lable_list = [u'男',u'女', u'未知']

            #获取年龄比例
            condition_list = WebUserAnalysisPO().hanlde_age_condition()
            count_user_age_list = []
            for item in condition_list:
                result = Manager().count_user(item)
                count_user_age_list.append(int(result[0]['COUNT(*)']))
            count_user_age_list.reverse()
            age_lable_list = [u'小于20',u'20~25',u'25~30',u'30~35',u'35~40',u'大于40',u'未知']

            #获取用户活跃度
            result = Manager().get_user_active()
            user_active_list = WebUserAnalysisPO().handle_user_active_result(result)
            active_lable_list = [u'活跃用户',u'普通用户',u'非活跃用户']


            #获取右日期——天
            delta_number_day = int(current_date[8:])
            right_date_day = current_date
            if delta_number_day < 15:
                delta_number_day = 15
                right_date_day = right_date_day[0:8] + '15'
            #获取右日期——月
            delta_number_mon = int(current_date[5:7])
            right_date_mon = current_date
            if delta_number_mon < 6:
                delta_number_mon = 6
                right_date_mon = right_date_mon[0:5] + '06'

            # 获取注册用户——天
            count_reg_user_day, delta_date, date_list = Manager().get_count_manager(delta_number_day,right_date_day,
                                                        1,{'1=':1},'register_time','hf_user')
            reg_user_day = WebUserAnalysisPO().handle_reg_user_info(count_reg_user_day, date_list)
            #获取注册用户——月
            count_reg_user_mon, delta_date, date_list = Manager().get_count_manager(delta_number_mon,right_date_mon,2,
                                                        {'1=':1},'register_time', 'hf_user')
            reg_user_mon = WebUserAnalysisPO().handle_reg_user_info(count_reg_user_mon, date_list)

            #获取用户访问——日
            count_visit_user_day, delta_date, date_list = Manager().get_count_manager(delta_number_day, right_date_day,1,
                                                        {'1=':1},'login_time', 'hf_login_log_user')
            visit_user_day = WebUserAnalysisPO().handle_reg_user_info(count_visit_user_day,date_list)
            #获取用户访问——月
            count_visit_user_mon, delta_date, date_list = Manager().get_count_manager(delta_number_mon, right_date_mon, 2,
                                                        {'1=':1}, 'login_time', 'hf_login_log_user')
            visit_user_mon = WebUserAnalysisPO().handle_reg_user_info(count_visit_user_mon, date_list)

            #获取用户搜索关键字top5
            user_searching_list = Manager().get_user_searching({'1=':1},' GROUP BY keyword_content order by count(*) desc limit 5 ')
            for i in range(0, 5-len(user_searching_list)):
                temp_dict = {'COUNT(*)':'N/A', 'keyword_content':'N/A'}
                user_searching_list.append(temp_dict)

            #获取各个地域用户数量
            region_user_count = Manager().count_region_user()
            custom_data_set, region_users = WebUserAnalysisPO().handle_region_user(region_user_count)

            self.refresh_session()
            self.render('useranalysis.html', head_info=head_info, new_user_info=new_user_info,
                        new_visit_info=new_visit_info, new_order_info=new_order_info, sex_property_list=sex_property_list,
                        sex_lable_list=sex_lable_list,count_user_age_list=count_user_age_list,
                        age_lable_list=age_lable_list, user_active_list=user_active_list,active_lable_list=active_lable_list,
                        reg_user_day=reg_user_day, reg_user_mon=reg_user_mon, visit_user_day=visit_user_day,
                        visit_user_mon=visit_user_mon, user_searching_list=user_searching_list, region_users=region_users,
                        custom_data_set=[custom_data_set])
        except Exception as e:
            self.render('404.html', error_reason=e)