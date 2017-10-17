# -*- coding: utf-8 -*-

class WebProductAnalysisPO:

    def handle_total_sale_info(self, data_list, date_list):

        sale_list = []

        for i in range(0, len(data_list)):
            temp_dict = {
                'period':date_list[i],
                'sale_data': data_list[i],
            }
            sale_list.append(temp_dict)

        return sale_list

    def handle_stock_radio(self, product_list):

        temp_list = []
        product_list_re = []

        for item in product_list:
            if item['stock/SUM(product_quantity)'] < 1:
                temp_dict = {
                    'stock_radio':item['stock/SUM(product_quantity)'],
                    'product_name':item['product_name'],
                    'product_id':item['product_id'],
                    'stock':item['stock'],
                }
                temp_list.append(temp_dict)

        for item in temp_list:

            if len(product_list_re) == 0:
                product_list_re.append(item)
                continue

            for i in range(0, len(product_list_re)):
                if i == len(product_list_re)-1:
                    if item['stock_radio'] < product_list_re[0]['stock_radio']:
                        product_list_re.insert(0, item)
                        break

                    if item['stock_radio'] > product_list_re[len(product_list_re)-1]['stock_radio']:
                        product_list_re.append(item)
                        break
                else:
                    if item['stock_radio'] > product_list_re[i]['stock_radio']\
                            and item['stock_radio'] < product_list_re[i+1]['stock_radio']:
                        product_list_re.insert(i+1, item)
                        break

        return product_list_re
#
# d = [
#     {'stock':1,'stock/SUM(product_quantity)':0.5,'product_name':'p1','product_id':1},
#     {'stock':1,'stock/SUM(product_quantity)':0.3,'product_name':'p1','product_id':2},
#     {'stock':1,'stock/SUM(product_quantity)':0.7,'product_name':'p1','product_id':3},
#     {'stock':1,'stock/SUM(product_quantity)':0.6,'product_name':'p1','product_id':4},
#     {'stock':1,'stock/SUM(product_quantity)':0.4,'product_name':'p1','product_id':5},
# ]
#
# print WebProductAnalysisPO().handle_stock_radio(d)

    def handle_group_data_info(self, data_list, date_list):

        data_info_list = []

        for i in range(0, len(data_list)):

            temp_dict = {
                'period':date_list[i],
                'normal_sale':0,
                'sup_sale':0,
                'elec_sale':0,
            }
            for item in data_list[i]:
                if item['product_type'] == 0:
                    temp_dict['normal_sale'] = int(item['SUM(product_quantity)'])
                elif item['product_type'] == 1:
                    temp_dict['sup_sale'] = int(item['SUM(product_quantity)'])
                else:
                    temp_dict['elec_sale'] = int(item['SUM(product_quantity)'])

            data_info_list.append(temp_dict)

        return data_info_list

    def handle_group_data_info_click(self, data_list, date_list):

        click_list = []

        for i in range(0, len(data_list)):
            temp_dict = {
                'period': date_list[i],
                'normal_click': 0,
                'sup_click': 0,
                'elec_click': 0,
            }

            for item in data_list[i]:
                if item['product_type'] == 0:
                    temp_dict['normal_click'] = int(item['SUM(count_click)'])
                elif item['product_type'] == 1:
                    temp_dict['sup_click'] = int(item['SUM(count_click)'])
                else:
                    temp_dict['elec_click'] = int(item['SUM(count_click)'])

            click_list.append(temp_dict)
        click_list.reverse()
        return click_list

    def handle_scatterplot_info(self, each_price_sale_list, product_type_list, condition_list):

        scatterplot_nor, scatterplot_sup, scatterplot_ele = [],[],[]

        for i in range(0,len(each_price_sale_list)):
            temp_list = []
            for j in range(0, len(each_price_sale_list[i])):
                temp_dict = {
                    'y':each_price_sale_list[i][j],
                    'r':10
                }
                try:
                    temp_dict['x'] = condition_list[j]['product_price<=']
                except:
                    temp_dict['x'] = condition_list[j]['product_price>'] + 100
                temp_list.append(temp_dict)
            if product_type_list[i]['product_type'] == 0:
                scatterplot_nor = temp_list
            elif product_type_list[i]['product_type'] == 1:
                scatterplot_sup = temp_list
            else:
                scatterplot_ele = temp_list

        return scatterplot_nor, scatterplot_sup, scatterplot_ele


