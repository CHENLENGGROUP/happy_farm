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
from system_logic.po.WebManagerAnalysisPO import WebManagerAnalysisPO

class BrowseManagerAnalysisHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        try:
            if not self.get_login_status():
                self.redirect('/managerlogin')
                return

            head_info = self.get_head_info('员工分析')

            #计算上月日期
            last_mon_date = WebManagerAnalysisPO().calculate_last_month_date()

            #获取上月各个员工的工作量
            product_workingload, order_workingload = Manager().get_manager_workingload(last_mon_date)
            manager_list = Manager().get_manager({'1=':1})
            message_workingload = []
            for item in manager_list:
                result = Manager().count_message({'sender_id=':item['manager_id'],
                                                  'message_type_id=':2, 'send_time LIKE':last_mon_date})
                message_workingload.append(result)
            manager_real_name_lable, workingload = WebManagerAnalysisPO().handle_workingload(
                product_workingload, order_workingload, message_workingload, manager_list)

            #获取上月各个员工迟到量
            mistake_count_list = []
            for item in manager_list:
                last_mon_login_time = Manager().get_last_mon_login({'manager_id=':item['manager_id'], 'login_time LIKE':last_mon_date})
                mistake = WebManagerAnalysisPO().handle_mistake_info(last_mon_login_time, last_mon_date)
                mistake_count_list.append(mistake)

            #获取上月优秀员工
            best_top3_career = WebManagerAnalysisPO().handle_best_top3_career(manager_real_name_lable,workingload,mistake_count_list)

            #获取员工处理事件——日

            current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            delta_number_day = int(current_date[8:])
            right_date_day = current_date
            if delta_number_day < 15:
                delta_number_day = 15
                right_date_day = right_date_day[0:8] + '15'

            manager_handle_message_list = []
            manager_handle_product_list = []
            manager_handle_order_list = []
            date_list = []
            for item in manager_list:
                # 获取员工处理消息数
                count_message, delta_date, date_list = Manager().get_count_manager(delta_number_day,right_date_day,1,
                                                    {'message_type_id=':2,'sender_id=':item['manager_id']},
                                                    'send_time','hf_message')
                manager_handle_message_list.append(count_message)

                # 获取员工处理商品数
                count_product, delta_date, date_list = Manager().get_count_manager(delta_number_day, right_date_day,1,
                                                        {'manager_id=':item['manager_id']},'act_time','hf_product_act_log')
                manager_handle_product_list.append(count_product)

                #获取员工处理订单数
                count_order, delta_date, date_list = Manager().get_count_manager(delta_number_day, right_date_day,1,
                                                    {'manager_id=':item['manager_id']},'log_time','hf_manager_act_log')
                manager_handle_order_list.append(count_order)

            manager_handle_event_data = WebManagerAnalysisPO().handle_manager_event(manager_handle_message_list,manager_handle_product_list,
                                                                                    manager_handle_order_list,date_list, manager_list)

            self.refresh_session()
            self.render('manageranalysis.html', head_info=head_info, manager_real_name_lable=manager_real_name_lable,
                        workingload=workingload, mistake_count_list=mistake_count_list, best_top3_career=best_top3_career,
                        manager_handle_event_data=[manager_handle_event_data], manager_list=manager_list)

        except Exception as e:
            self.render('404.html', error_reason=e)