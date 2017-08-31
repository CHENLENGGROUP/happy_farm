# -*- coding: utf-8 -*-

class WebOrderActLogPO:

    def merge_two_order_act_log(self, order_log_manager, order_log_user):

        order_log_list = []
        i=0
        j=0
        while i<len(order_log_manager) and j<len(order_log_user):
            if order_log_manager[i]['act_time']<=order_log_user[j]['act_time']:
                order_log_manager[i]['actor_type'] = "管理员"
                order_log_manager[i]['actor_name'] = order_log_manager[i]['real_name']
                order_log_list.append(order_log_manager[i])
                i = i+1
            else:
                order_log_user[j]['actor_type'] = "用户"
                order_log_user[j]['actor_name'] = order_log_user[j]['username']
                order_log_list.append(order_log_user[j])
                j = j+1

        while i<len(order_log_manager):
            order_log_manager[i]['actor_type'] = "管理员"
            order_log_manager[i]['actor_name'] = order_log_manager[i]['real_name']
            order_log_list.append(order_log_manager[i])
            i = i + 1

        while j<len(order_log_user):
            order_log_user[j]['actor_type'] = "用户"
            order_log_user[j]['actor_name'] = order_log_user[j]['username']
            order_log_list.append(order_log_user[j])
            j = j + 1

        return order_log_list