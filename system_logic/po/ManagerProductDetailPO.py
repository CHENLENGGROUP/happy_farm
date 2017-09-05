# -*- coding: utf-8 -*-

class ManagerProductDetailPO:

    def handle_areachart_data(self, count_sales_list, count_click_list, date_list):

        data_list = []
        for i in range(0, len(count_click_list)):
            temp_dict = {
                'period':date_list[i],
                'count_sales':count_sales_list[i],
                'count_click':count_click_list[i]
            }
            data_list.insert(0, temp_dict)

        return data_list

    def handle_box_data(self, data1, data2):

        if data2 == 0:
            data2 = 1
            data_increase = float(data1)/float(data2)*100
        else:
            data_increase = float(data1-data2)/float(data2)*100

        return data1, data_increase

    def handle_property_info(self, property_info):

        property_str = ''

        for item in property_info:
            property_str = '%s,%s：%s'%(property_str,item['property_name'], item['property_content'])

        return property_str[1:]