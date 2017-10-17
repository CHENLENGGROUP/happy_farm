# -*- coding: utf-8 -*-

import time
import calendar

class WebManagerAnalysisPO:

    def handle_workingload(self, product_work, order_work, message_workingload, manager_list):

        manager_name_lable = []
        workingload = []

        for i in range(0, len(manager_list)):
            item = manager_list[i]
            manager_name_lable.append(item['real_name'])
            count = 0
            for item2 in product_work:
                if item2['real_name'] == item['real_name']:
                    count = count + item2['COUNT(*)']
                    break
            for item2 in order_work:
                if item2['real_name'] == item['real_name']:
                    count = count + item2['COUNT(*)']
                    break
            count = count + message_workingload[i]
            workingload.append(int(count))

        return manager_name_lable, workingload

    def calculate_last_month_date(self):

        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        mon = int(current_date[5:7])
        year = int(current_date[0:4])
        if mon == 1:
            mon = '12'
            year = str(year - 1)
        else:
            mon = str(mon - 1)
            if len(mon) == 1:
                mon = '0' + mon
            year = str(year)
        last_mon_date = year + '-' + mon + '%%'

        return last_mon_date

    def handle_mistake_info(self, mistake_info_list, last_mon_date):

        count = 0
        year = int(last_mon_date[0:4])
        mon = int(last_mon_date[5:7])
        days = calendar.monthrange(year,mon)[1]

        unlogin_days = days - len(mistake_info_list)

        for item in mistake_info_list:
            if item['MIN(login_time)'][11:] > '09:00:00':
                count = count+1

        return count+unlogin_days

    def handle_best_top3_career(self,manager_real_name_lable,workingload, mistake_count_list):

        work_fault_rate_list = [{'rate': 0}, {'rate': 0}, {'rate': 0}]
        for i in range(0, len(manager_real_name_lable)):
            if mistake_count_list[i] == 0:
                temp_rate = workingload[i]
            else:
                temp_rate = float(workingload[i]) / float(mistake_count_list[i])
            temp_dict = {'real_name': manager_real_name_lable[i], 'rate': temp_rate}
            for j in range(0, len(work_fault_rate_list)):
                if temp_rate >= work_fault_rate_list[j]['rate']:
                    work_fault_rate_list.insert(j, temp_dict)
                    break

        return work_fault_rate_list[0:3]

    def handle_manager_event(self, m_list, p_list, o_list, date_list, manager_list):

        manager_event_data = {}
        for i in range(0, len(manager_list)):
            temp_list = []
            for j in range(0, len(date_list)):
                temp_dict = {
                    'period':date_list[j],
                    'msg_reply':m_list[i][j],
                    'product_h':p_list[i][j],
                    'order_h':o_list[i][j],
                }
                temp_list.append(temp_dict)
            temp_list.reverse()
            manager_event_data[int(manager_list[i]['manager_id'])] = temp_list

        return manager_event_data


