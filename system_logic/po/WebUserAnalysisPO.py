# -*- coding: utf-8 -*-
import time
import datetime
from system_logic import setting

class WebUserAnalysisPO:

    def __init__(self):
        self.current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def handle_increase_rate(self, data1, data2):

        if data2 == 0:
            result = float(data1)*100
        else:
            result = float(data1-data2)*100

        return data1, result

    def hanlde_age_condition(self):

        current_year = int(self.current_date[0:4])

        age_list = []
        for i in range(0,5):
            age_list.append(current_year-(40-(i*5)))

        condition_list = [{'birthday=':' '}]
        for i in range(0, len(age_list)):
            if i==0:
                birthday = str(age_list[i]) + '-01-01'
                temp_dict = {'birthday<':birthday,'birthday !=':' '}
            else:
                birthday_left = str(age_list[i-1])+'-01-01'
                birthday_right = str(age_list[i]) + '-12-31'
                temp_dict = {'birthday>':birthday_left,'birthday<':birthday_right}
            condition_list.append(temp_dict)

        temp_dict = {'birthday>':str(age_list[len(age_list)-1])+'-12-31'}
        condition_list.append(temp_dict)
        return condition_list

    def handle_user_active_result(self, active_info):

        active_user = 0
        normal_user = 0
        inactive_user = 0

        for item in active_info:
            rt = item['register_time']
            d1 = datetime.datetime(int(self.current_date[0:4]),int(self.current_date[5:7]), int(self.current_date[8:]))
            d2 = datetime.datetime(int(rt[0:4]),int(rt[5:7]),int(rt[8:10]))
            delta_date = float((d1-d2).days)
            day_active_rate = float(item['COUNT(*)'])/delta_date
            if day_active_rate >= 0.2:
                active_user = active_user+1
            elif day_active_rate < 0.2 and day_active_rate > 0.03:
                normal_user = normal_user + 1
            else:
                inactive_user = inactive_user + 1

        return [active_user, normal_user, inactive_user]

    def handle_reg_user_info(self, reg_user_list, date_list):

        reg_user_info = []

        for i in range(0, len(reg_user_list)):
            temp_dict = {
                'period':date_list[i],
                'count':reg_user_list[i],
            }
            reg_user_info.append(temp_dict)

        reg_user_info.reverse()
        return reg_user_info

    def handle_region_user(self, region_user):

        region_users = setting.default_region_user
        custom_color = {}

        for item in region_user:

            count = item['COUNT(DISTINCT user_id)']

            if item['province'] == '':
                for item2 in region_users:
                    if item2.keys()[0] == '未知':
                        item2[u'未知'] = count
            else:
                for item2 in region_users:
                    if item2.keys()[0] == item['province']:
                        item2[item['province']] = count

                region_code = setting.region_code[item['province']]

                if count == 0:
                    pass
                elif count>0 and count<50:
                    custom_color[region_code] = setting.region_color_dict['0-50']
                elif count>=50 and count < 100:
                    custom_color[region_code] = setting.region_color_dict['50-100']
                elif count>=100 and count<150:
                    custom_color[region_code] = setting.region_color_dict['100-150']
                elif count>=150 and count<200:
                    custom_color[region_code] = setting.region_color_dict['150-200']
                elif count>=200 and count<250:
                    custom_color[region_code] = setting.region_color_dict['200-250']
                elif count>=250 and count<300:
                    custom_color[region_code] = setting.region_color_dict['250-300']
                else:
                    custom_color[region_code] = setting.region_color_dict['300']

        return custom_color, region_users
