# -*- coding: utf-8 -*-


class WebMessagePO:

    def handle_input_condition(self, box_type, condition, manager_id):
        #用户收件箱
        if box_type == 1:
            condition['message_type_id='] = 1
            condition['receiver_id='] = 0
            condition['is_delete='] = 0
            title_name = '用户收件箱'
        #内部收件箱
        elif box_type == 2:
            condition['message_type_id='] = 3
            condition['receiver_id='] = manager_id
            condition['is_delete='] = 0
            title_name = '内部收件箱'
        #发件箱
        elif box_type == 3:
            condition['sender_id='] = manager_id
            condition['is_delete='] = 0
            title_name = '发件箱'

        #重要邮件
        elif box_type == 4:
            condition = [
                {'is_delete=': {'value': 0, 'symbol': 'AND'}},
                {'is_important=':{'value':1, 'symbol':'AND'}},
                {'(receiver_id=': {'value': manager_id, 'symbol': 'OR'}},
                {'receiver_id=': {'value': 0, 'symbol': ')'}}
            ]
            title_name = '重要邮件'
        #垃圾箱
        elif box_type == 5:
            condition = [
                {'is_delete=':{'value':1,'symbol':'AND'}},
                {'(receiver_id=':{'value':manager_id,'symbol':'OR'}},
                {'receiver_id=':{'value':0, 'symbol':')'}}
            ]
            title_name = '垃圾箱'
        else:
            title_name = ''

        return condition, title_name

    def handle_manager_list(self, manager_list):

        manager_list_re = []

        if manager_list == -1:
            return manager_list_re

        for item in manager_list:
            temp_dict = {'manager_id':item['manager_id'], 'real_name':item['real_name']}
            manager_list_re.append(temp_dict)

        return manager_list_re