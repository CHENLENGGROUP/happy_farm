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
from system_logic.po.ManagerProductDetailPO import ManagerProductDetailPO
from system_logic.po.PageAddProductPO import PageAddProductPO

class BrowseProductDetailHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        if not self.get_login_status():
            self.redirect('/managerlogin')
            return


        product_id = int(self.get_argument('product_id'))

        #获取近10天的销售量
        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        count_sales_list, delta_date, date_list = Manager().get_count_quantity(10,current_date,1,{'product_id=':product_id},
                                                                               'create_time','hf_order', 'product_quantity')
        #获取近10天的点击量
        count_click_list, delta_date, date_list = Manager().get_count_manager(10,current_date,1,
                                                  {'product_id=':product_id},'click_time','hf_product_click_log')
        #获取此前每月销售量
        c_date = current_date[0:5]+'12-01'
        count_sales_list_m, delta_date_m, date_list_m = Manager().get_count_quantity(12,c_date,2,{'product_id=':product_id},
                                                                                     'create_time', 'hf_order', 'product_quantity')
        count_sales_list_m.reverse()
        #获取此前每月营业额
        count_income_m, delta_date_m, date_list_m = Manager().get_count_quantity(12,c_date, 2,{'product_id=':product_id},
                                                                                 'create_time','hf_order', 'order_subtotal')
        count_income_m.reverse()
        #获取此商品总共的销售量
        sales_product = Manager().get_sales_total({'product_id=':product_id})
        #获取全部商品的销售量
        sales_all = Manager().get_sales_total({'1=':1})
        #获取此商品的营业额
        income_product = Manager().get_income_total({'product_id=':product_id})
        #获取所有商品的营业额
        income_all = Manager().get_income_total({'1=':1})

        sales_data_list = [sales_product, sales_all-sales_product]
        income_data_list = [income_product, income_all-income_product]
        areachart_data = ManagerProductDetailPO().handle_areachart_data(count_sales_list,count_click_list, date_list)

        #获取昨日浏览量以及涨幅
        yesteday_visit, visit_increase = ManagerProductDetailPO().handle_box_data(count_click_list[1], count_click_list[2])
        visit_info = {'yesteday_visit':yesteday_visit,'visit_increase':visit_increase}

        # 获取昨日销售量以及涨幅
        yesteday_sales, sales_increase = ManagerProductDetailPO().handle_box_data(count_sales_list[1], count_sales_list[2])
        sales_info = {'yesteday_sales':yesteday_visit, 'sales_increase':sales_increase}

        #获取商品信息
        product_info, count = Manager().browse_product({'hf_product.product_id=':product_id},1,None,0)
        product_info = product_info[0][0]

        #获取商品类型信息
        product_type = Manager().get_product_type({'product_type=':product_info['product_type']})[0]

        product_info['type_name'] = product_type['type_name']

        #获取分类信息
        product_category = Manager().get_product_category({'product_id=':product_info['product_id']})

        #获取商品特性
        property_info = Manager().get_product_property({'product_id=':product_id,'is_delete=':0})
        property_str = ManagerProductDetailPO().handle_property_info(property_info)
        product_info['property_str'] = property_str

        #获取商品订单信息
        order_list = Manager().get_product_order({'product_id=':product_id},None)

        head_info = self.get_head_info('商品明细',str(product_info['product_name']))

        payment_log = Manager().get_

        self.refresh_session()
        self.render('productdetail.html', head_info=head_info, sales_data_list=sales_data_list,
                    income_data_list=income_data_list, areachart_data=areachart_data, visit_info=visit_info,
                    sales_info=sales_info, product_info=product_info, product_category = product_category,
                    count_sales_list_m=count_sales_list_m, count_income_m=count_income_m, order_list=order_list,
                    payment_logs=[1,2,3,4,5,6,7])