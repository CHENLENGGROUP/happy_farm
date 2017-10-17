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
from system_logic.po.WebProductAnalysisPO import WebProductAnalysisPO

class BrowseProductAnalysisHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return

        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        head_info = self.get_head_info('商品分析')

        #获取本月销售量
        count_sale_total, delta_date, date_list = Manager().get_count_quantity(1,current_date,2,{'1=':1},
                                                'create_time','hf_order', 'product_quantity')
        count_sale_total = int(count_sale_total[0])

        #获取本月点击量
        count_click_total = Manager().get_count_manager(1,current_date,2,
                                                  {'1=':1},'click_time','hf_product_click_log')[0][0]

        #获取本月评论量
        count_comment_total = Manager().get_count_manager(1, current_date, 2,
                                                    {'1=':1}, 'comment_time', 'hf_comment')[0][0]

        #获取商品类型
        product_type_list = Manager().get_product_type({'1=':1})

        label_list = []
        count_sd_list_temp = Manager().get_top5_sale({'1=':1},'product_type')
        count_sd_list = []
        count_cd_list = []
        #获取各个类型销量
        for item in product_type_list:
            label_list.append(item['type_name'])
            temp_count_c = Manager().get_count_manager(5,current_date,3,{'product_type=':item['product_type']},
                                                       'click_time','hf_product_click_log')[0]
            _sum = 0
            for item2 in temp_count_c:
                _sum = item2 + _sum

            for item1 in count_sd_list_temp:
                if item['product_type'] == item1['product_type']:
                    count_sd_list.append(int(item1['SUM(product_quantity)']))
            count_cd_list.append(_sum)

        #获取商品每天总销量
        delta_number_day = int(current_date[8:])
        right_date_day = current_date
        if delta_number_day < 15:
            delta_number_day = 15
            right_date_day = right_date_day[0:8]+'15'
        count_sale_total_day, delta_date, date_list = Manager().get_count_quantity(delta_number_day,right_date_day,1,{'1=':1},
                                                    'create_time', 'hf_order', 'product_quantity')
        sale_list_day = WebProductAnalysisPO().handle_total_sale_info(count_sale_total_day, date_list)

        #获取商品每月总销量
        delta_number_mon = int(current_date[5:7])
        right_date_mon = current_date
        if delta_number_mon < 6:
            delta_number_mon = 6
            right_date_mon = right_date_mon[0:5] + '06'
        count_sale_total_mon, delta_date, date_list = Manager().get_count_quantity(delta_number_mon,right_date_mon,2,{'1=':1},
                                                    'create_time', 'hf_order', 'product_quantity')
        sale_list_mon = WebProductAnalysisPO().handle_total_sale_info(count_sale_total_mon, date_list)

        #获取top5销量的产品
        top5_sale_products = Manager().get_top5_sale({'1=':1},supstring=' LIMIT 0, 5')
        for i in range(0,5-len(top5_sale_products)):
            top5_sale_products.append({'product_name':'N/A','SUM(product_quantity)':'N/A'})

        #获取top5库存预警,比较库销比
        #比较库销比，先获取上个月各个商品销量
        condition = {'create_time LIKE':current_date[0:7]+'%%', 'NOT hf_order.product_type = ':1}
        last_month_sale = Manager().get_top5_saleStockRadio(condition)
        last_month_stock_radio = WebProductAnalysisPO().handle_stock_radio(last_month_sale)
        for i in range(0,5-len(last_month_stock_radio)):
            last_month_stock_radio.append({'product_name':'N/A','stock':'N/A', 'stock_radio':'N/A'})

        #获取各类商品的销售量-日
        count_msg_list, date_list = Manager().get_group_count({'1=':1},'product_type',
                                    {'SUM(product_quantity)':0, 'product_type':0},
                                    '','hf_order', delta_number_day, right_date_day, 1, 'create_time')
        each_type_sale_day = WebProductAnalysisPO().handle_group_data_info(count_msg_list, date_list)

        #获取各类商品的销售量-月
        count_msg_list, date_list = Manager().get_group_count({'1=':1},'product_type',
                                    {'SUM(product_quantity)':0,'product_type':0},'','hf_order',
                                    delta_number_mon,right_date_mon,2,'create_time')
        each_type_sale_mon = WebProductAnalysisPO().handle_group_data_info(count_msg_list, date_list)

        #获取各类商品的点击量-日
        count_msg_list, date_list = Manager().get_group_count({'1=':1},'product_type',
                                    {'SUM(count_click)':0, 'product_type':0},'','hf_product_click_log',
                                    delta_number_day, right_date_day, 1, 'click_time')
        each_type_click_day = WebProductAnalysisPO().handle_group_data_info_click(count_msg_list, date_list)
        #获取各类商品的点击量-月
        count_msg_list, date_list = Manager().get_group_count({'1=': 1}, 'product_type',
                                    {'SUM(count_click)': 0, 'product_type': 0}, '','hf_product_click_log',
                                    delta_number_mon, right_date_mon, 2, 'click_time')
        each_type_click_mon = WebProductAnalysisPO().handle_group_data_info_click(count_msg_list, date_list)

        #获取散点图数据
        condition_list = []
        for i in range(0,11):
            temp_dict = {}
            temp_dict['product_price>'] = i*100
            if i!=10:
                temp_dict['product_price<='] = (i+1)*100
            condition_list.append(temp_dict)
        each_price_sale_list = []
        for item in product_type_list:
            temp_list = []
            for item2 in condition_list:
                item2['product_type='] = item['product_type']
                result = Manager().get_count_order(item2)
                temp_list.append(result)
            each_price_sale_list.append(temp_list)
        scatterplot_nor, scatterplot_sup, scatterplot_ele = \
            WebProductAnalysisPO().handle_scatterplot_info(each_price_sale_list, product_type_list, condition_list)


        self.refresh_session()
        self.render('productanalysis.html', head_info=head_info, count_sale_total=count_sale_total,
                    count_comment_total=count_comment_total, count_click_total=count_click_total, label_list=label_list,
                    count_sd_list=count_sd_list, count_cd_list=count_cd_list, sale_list_day=sale_list_day,
                    sale_list_mon=sale_list_mon, top5_sale_products=top5_sale_products,
                    last_month_stock_radio=last_month_stock_radio, each_type_sale_day=each_type_sale_day,
                    each_type_sale_mon=each_type_sale_mon, each_type_click_day=each_type_click_day,
                    each_type_click_mon=each_type_click_mon, scatterplot_nor=scatterplot_nor,
                    scatterplot_sup=scatterplot_sup, scatterplot_ele=scatterplot_ele)