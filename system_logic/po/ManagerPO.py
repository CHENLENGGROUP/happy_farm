# -*- coding: utf-8 -*-

import random
import time
import datetime
from system_logic.po.ProduceRandomStr import ProduceRandomStr

class ManagerPO:

    def __init__(self):
        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def handle_login_info(self, manager_id, location_info):

        location_info['manager_id'] = manager_id
        location_info['login_time'] = self.current_time
        return location_info, self.current_time

    def hanlde_registerInfo(self, apply_info):
        '''
        处理注册管理员用户的输入信息
        :param apply_info:                  请求信息
            :param session_info             session信息
                :param session_id           session号
                :param verify_code          验证码
            :param register_info            注册信息
                :param username             用户名
                :param passwd               密码
                :param real_name            真实姓名
                :param telephone            电话号码
                :param authority            权限
                :param manager_menu         拥有菜单

        :return:
            session_info                     session信息
            add_manager_info                 管理员信息
            manager_menu_info                管理员菜单权限信息
        '''
        session_info = apply_info['session_info']
        add_manager_info = {}
        manager_menu_info = []
        for key in apply_info['register_info']:
            if key != 'manager_menu':
                add_manager_info[key] = apply_info['register_info'][key]
            else:
                manager_menu_info = apply_info['register_info'][key]
        add_manager_info['add_time'] = self.current_time
        return session_info, add_manager_info, manager_menu_info

    def handle_managerMenu(self, manager_id, manager_menu):
        '''
        此方法用以处理管理员和菜单权限的数据
        :param manager_id:                  管理员id
        :param manager_menu:                管理员菜单权限列表
        :return:
        :param manager_menu_list            管理员菜单权限插入列表
        数据结构
        '''
        manager_menu_list=[]
        for item in manager_menu:
            temp_dict = {'manager_id':manager_id, 'menu_id':item}
            manager_menu_list.append(temp_dict)
        return manager_menu_list

    def handle_product_info(self, product_info, manager_id):
        '''

        :param apply_info:                  内容同Manager类中的add_product方法的apply_info
        :return:
        :param session_info                 session信息
        :param product_basic_info           商品基本信息
        :param prodcut_sub_info             商品补充信息
        :param product_attribute_info       商品属性信息
        :param product_act_log_info         商品操作日志信息
        :param product_gallery_info         商品图片信息
        '''
        product_basic_info = product_info['basic_info']
        product_sub_info = product_info['sub_info']
        product_category_info = product_info['product_category_info']
        product_property_info = product_info['product_property_info']

        #生成商品编号 xxxxxx-xx-xxxx-xxxx
        # 前6位是日期，7-8位是商品类型，00普通商品，01认领商品, 9-12位是添加者id，13到16位是随机数
        first_part = time.strftime('%Y%m%d', time.localtime(time.time()))[2:]
        second_part = '0'+ str(product_basic_info['product_type'])
        thrid_part = str(manager_id)
        for i in range(len(manager_id),4):
            thrid_part = '0' + thrid_part
        fouth_part = ProduceRandomStr().product_randomInt()
        product_sn = first_part + second_part + thrid_part + fouth_part
        product_basic_info['product_sn'] = product_sn

        product_basic_info['add_time'] = self.current_time

        product_act_log_info = {'manager_id':manager_id, 'act_type_id':1, 'act_time':self.current_time}

        return product_basic_info, product_sub_info, product_category_info, \
               product_act_log_info, product_property_info

    def handle_product_category_info(self, product_id, category):
        product_category_list = []
        for item in category:
            temp_dict = {'product_id': product_id, 'category_id': item}
            product_category_list.append(temp_dict)
        return product_category_list

    def handle_product_gallery_info(self, product_id, gallery):
        product_category_list = []
        for item in gallery:
            temp_dict = item
            temp_dict['product_id'] = product_id
            product_category_list.append(temp_dict)
        return product_category_list

    def handle_product_property_info(self, product_id, property):
        product_property_list = []
        for item in property:
            temp_dict = {}
            property_name = item.keys()[0]
            property_content = item[property_name]
            temp_dict['property_name'] = property_name
            temp_dict['property_content'] = property_content
            temp_dict['product_id'] = product_id
            product_property_list.append(temp_dict)
        return product_property_list

    def handle_sale_quantity_date(self, right_date, delta_number, get_type):

        date_list = []
        delta_date = 0
        for i in range(0, delta_number):
            if get_type == 1:
                right_datetime = datetime.datetime.strptime(right_date, '%Y-%m-%d').date()
                d2 = datetime.date(int(right_date[0:4]), 1, 10)
                delta_date = (right_datetime - d2).days
                datetime_temp = str(right_datetime-datetime.timedelta(days=i))
                date_list.append(datetime_temp)
            elif get_type == 2:
                month_number = int(right_date[5:7])
                month_number_1 = month_number-i
                if month_number_1 > 0:
                    if len(str(month_number_1)) == 1:
                        month_temp = '0'+str(month_number_1)
                    else:
                        month_temp = str(month_number_1)
                    datetime_temp = right_date[0:4] + '-' + month_temp
                    date_list.append(datetime_temp)
            else:
                year_number = int(right_date[0:4])
                year_num = year_number - i
                if year_num > 0:
                    if len(str(year_num)) == 1:
                        _temp = '000' + str(year_num)
                    elif len(str(year_num)) == 2:
                        _temp = '00' + str(year_num)
                    elif len(str(year_num)) == 3:
                        _temp = '0' + str(year_num)
                    else:
                        _temp = str(year_num)
                    datetime_temp = _temp
                    date_list.append(datetime_temp)

        return date_list,delta_date

    def handle_income_condition(self, product_type, date_item):

        if product_type == -1:
            condition = [
                {'(payment_date IS NULL': {'value': '', 'symbol': 'AND'}},
                {'create_time LIKE': {'value': date_item + '%%', 'symbol': ') OR'}},
                {'payment_date LIKE': {'value': date_item + '%%', 'symbol': ''}}
            ]
        else:
            condition = [
                {'((payment_date IS NULL': {'value': '', 'symbol': 'AND'}},
                {'create_time LIKE': {'value': date_item + '%%', 'symbol': ') OR'}},
                {'payment_date LIKE': {'value': date_item + '%%', 'symbol': ') AND'}},
                {'product_type=': {'value':product_type, 'symbol':''}}
            ]
        return condition

    def handle_income(self, info_list):
        subtotal = 0
        for item in info_list:
            if item['product_type'] == 0 or item['product_type'] == 2:
                subtotal = subtotal + float(item['order_subtotal'])
            else:
                subtotal = subtotal + float(item['amount'])
        return subtotal

    def handle_browse_message_info(self, msg_info, sender_info, message_type_id):

        temp_dict = {}
        for key in msg_info:
            if key != 'reader_id' and key!='message_type_id' and key!='is_delete'\
                    and key!='is_alert':
                temp_dict[key] = msg_info[key]

        if sender_info.has_key('real_name'):
            temp_dict['show_name'] = sender_info['real_name']
            temp_dict['sender_type'] = 'manager'
        else:
            temp_dict['show_name'] = sender_info['username']
            temp_dict['sender_type'] = 'user'
        temp_dict['sender_pic'] = sender_info['profile_pic_url']

        return temp_dict

    def handle_send_message_info(self, message_info, manager_id):

        message_info_list = []

        reciver_id_list = message_info['receiver_id_list']

        for item in reciver_id_list:
            temp_dict = {}
            for key in message_info:
                if key != 'receiver_id_list':
                    temp_dict[key] = message_info[key]
            temp_dict['receiver_id'] = int(item)
            temp_dict['send_time'] = self.current_time
            temp_dict['sender_id'] = manager_id
            message_info_list.append(temp_dict)

        return message_info_list

    def handle_message_type(self, message_type_id, item, manager_id):

        condition_s = {}
        if message_type_id == 1:
            table_name = 'hf_user'
            condition_s['user_id='] = item['sender_id']
        elif message_type_id == 2:
            table_name = 'hf_user'
            condition_s['user_id='] = item['receiver_id']
        else:
            table_name = 'hf_manager'
            if int(item['sender_id']) == manager_id:
                condition_s['manager_id='] = item['receiver_id']
            else:
                condition_s['manager_id='] = item['sender_id']

        return condition_s, table_name

    def handle_product_list_info(self, product_list):

        product_list_re = []

        for item in product_list:
            temp_dict = {}
            for key in item:
                if not item[key] is None and key!='product_id1' and key != 'product_id2':
                    temp_dict[key] = item[key]
            product_list_re.append(temp_dict)

        product_list_fi = []
        temp_list = []
        if len(product_list_re) > 4:
            for i in range(0, len(product_list_re)):
                temp_list.append(product_list_re[i])
                if (i+1)%4 == 0 or i == len(product_list_re)-1:
                    product_list_fi.append(temp_list)
                    temp_list = []
        else:
            product_list_fi = [product_list_re]

        return product_list_fi

    def handle_login_log(self, login_log):

        login_log_re = []
        for item in login_log:
            temp_dict = {
                'username':item['username'],
                'telephone':item['telephone'],
                'authority':item['authority'],
                'register_time':item['register_time'],
                'profile_pic_url':item['profile_pic_url'],
                'manager_id':item['manager_id'],
                'real_name':item['real_name'],
                'login_time':item['login_time'],
                'login_ip':item['login_ip'],
                'country':item['country'],
                'province':item['province'],
                'city':item['city']
            }
            login_log_re.append(temp_dict)
        return login_log_re

    def handle_orderact_log(self, orderact_log):

        orderact_log_re = []
        for item in orderact_log:
            temp_dict = {
                'manager_id':item['manager_id'],
                'real_name':item['real_name'],
                'act_name':item['act_name'],
                'act_time':item['act_time'],
                'order_id':item['order_id'],
                'order_sn':item['order_sn'],
                'product_name':item['product_name']
            }
            orderact_log_re.append(temp_dict)
        return orderact_log_re

    def handle_orderact_log_user(self, orderact_log):

        orderact_log_re = []
        for item in orderact_log:
            temp_dict = {
                'user_id':item['user_id'],
                'username':item['username'],
                'act_name':item['act_name'],
                'act_time':item['act_time'],
                'order_id':item['order_id'],
                'order_sn':item['order_sn'],
                'product_name':item['product_name']
            }
            orderact_log_re.append(temp_dict)

        return orderact_log_re

    def handle_product_act_log(self, product_act_log):

        product_act_log_re = []
        for item in product_act_log:
            temp_dict = {
                'manager_id':item['manager_id'],
                'real_name':item['real_name'],
                'act_type_exp':item['act_type_exp'],
                'act_time':item['act_time'],
                'product_id':item['product_id'],
                'product_sn':item['product_sn'],
                'product_name':item['product_name']
            }
            if item['act_type_id'] != 3:
                act_detail = '%s商品，商品编号为%s'\
                             %(item['act_type_exp'], item['product_sn'])
            else:
                act_detail = '将%s从 "%s"修改为 "%s"'\
                             %(item['act_data_name'], item['original_data'], item['modified_data'])
            temp_dict['act_detail'] = act_detail
            product_act_log_re.append(temp_dict)

        return product_act_log_re

    def handle_income_total(self, order_info):

        subtotal = 0
        for item in order_info:
            if item['amount']:
                subtotal = subtotal + float(item['amount'])
            else:
                subtotal = subtotal + float(item['order_subtotal'])

        return subtotal

    def handle_product_order(self, order_list):

        order_list_re = []

        for item in order_list:

            del item['address_id']
            del item['thumb_img_url']
            del item['product_price']
            del item['is_alert']
            del item['zipcode']
            del item['contact_name']
            del item['contact_number']
            del item['user_id1']

            order_list_re.append(item)

        return order_list_re

    def handle_modify_product_info(self, product_info):

        product_type = product_info['product_type']
        product_id = product_info['product_id']
        basic_info = product_info['basic_info']
        sub_info = product_info['sub_info']
        product_property_info = product_info['product_property_info']

        basic_info_new, basic_info_old = self.split_old_new_value(basic_info)
        sub_info_new, sub_info_old = self.split_old_new_value(sub_info)
        product_property_info_new, product_property_info_old = self.split_old_new_value(product_property_info)

        product_info_old = {
            'product_type':product_type,
            'product_id':product_id,
            'basic_info':basic_info_old,
            'sub_info':sub_info_old,
            'product_property_info':product_property_info_old
        }
        product_info_new = {
            'product_type':product_type,
            'product_id':product_id,
            'basic_info':basic_info_new,
            'sub_info':sub_info_new,
            'product_property_info':product_property_info_new
        }
        return product_info_old, product_info_new

    def split_old_new_value(self, target_dict):

        temp_new = {}
        temp_old = {}
        for key in target_dict:
            temp_new[key] = target_dict[key]['new_value']
            temp_old[key] = target_dict[key]['old_value']

        return temp_new, temp_old

    def handle_update_info_diff(self, target_dict, manager_id):

        product_act_log = []
        product_id = target_dict['product_id']
        del target_dict['product_id']
        del target_dict['product_type']
        for key in target_dict:
            for key1 in target_dict[key]:
                temp_dict = {
                    'product_id': int(product_id),
                    'manager_id': int(manager_id),
                    'act_type_id': 3,
                    'act_time': self.current_time,
                }
                if key == 'product_property_info':
                    old_v = ''
                    new_v = ''
                    for key2 in target_dict[key][key1]:
                        for item in target_dict[key][key1][key2]:
                            for key3 in item:
                                if key2 == 'new_value':
                                    new_v = new_v + ',' + str(key3) + '：' + item[key3]
                                else:
                                    old_v = old_v + ',' + str(key3) + '：' + item[key3]
                    temp_dict['original_data'] = old_v
                    temp_dict['modified_data'] = new_v
                    temp_dict['act_data_name'] = key1

                elif key1 == 'is_hot':
                    if int(target_dict[key][key1]['old_value']) == 0 :
                        old_v = '非热门商品'
                    else:
                        old_v = '热门商品'
                    temp_dict['original_data'] = old_v
                    temp_dict['modified_data'] = target_dict[key][key1]['new_value']
                    temp_dict['act_data_name'] = key1
                else:
                    temp_dict['original_data'] = target_dict[key][key1]['old_value']
                    temp_dict['modified_data'] = target_dict[key][key1]['new_value']
                    temp_dict['act_data_name'] = key1

                product_act_log.append(temp_dict)

        return product_act_log

    def handle_article_list(self, article_list):

        article_total = []

        temp_list = []
        for i in range(0, len(article_list)):
            if (i!=0 and i%4 == 0):
                article_total.append(temp_list)
                temp_list = []
            temp_list.append(article_list[i])
            if i == len(article_list)-1:
                article_total.append(temp_list)

        return article_total
