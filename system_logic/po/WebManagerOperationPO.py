# -*- coding: utf-8 -*-

class WebManagerOperationPo:

    def handle_count_msg(self, msg_count_read, msg_count_reply, date_list):

        chart_data_list = []
        for i in range(0, len(msg_count_read)):
            index = len(msg_count_read)-1 - i
            temp_dict = {
                'y':date_list[index][5:],
                'a':int(msg_count_read[index]),
                'b':int(msg_count_reply[index])
            }
            chart_data_list.append(temp_dict)

        return chart_data_list

    def handle_count_order(self, order_act_count, date_list):

        chart_data_list = []
        for i in range(0, len(order_act_count)):
            index = len(order_act_count)-1-i
            temp_dict = {
                'y':date_list[index][5:],
                'a':int(order_act_count[index])
            }
            chart_data_list.append(temp_dict)

        return chart_data_list