# -*- coding: utf-8 -*-

#引入高速缓存模块
import  memcache
import time
#引入对象——人
from system_logic.bo.object.People import People
#引入数据库操作模块
from system_logic.dao.DataBaseEngine import DataBaseEngine
#引入数据处理模块
from system_logic.po.ManagerPO import ManagerPO
#引入session验证模块
from  system_logic.po.VerifySession import VerifySession
#引入session信息中获取用户id模块
from  system_logic.po.GetIdFromSession import GetIdFromSession
#引入md5加密模块
from system_logic.po.EncryptString import EncryptString
#引入查询IP模块
from system_logic.po.SearchLocationByIP import SearchLocationByIP
#引入商品对象
from system_logic.bo.object.static_object.Product import Product
#引入订单对象
from system_logic.bo.object.static_object.Order import Order
from system_logic.bo.object.static_object.NewEvent import NewEvent

class Manager:

    def __init__(self):
        self.mp = ManagerPO()
        self.mc = memcache.Client(['127.0.0.1:11211'])

    def login(self, username, passwd, login_ip):
        '''
        此方法用以实现允许用户登录,调用people类里面的login方法
        :param username                 用户名
        :param passwd                   密码
        :param login_ip                 登录ip

        :return: result
            -1                               连接失败
            -2                               验证失败
            else                             成功
        '''
        passwd = EncryptString().encrypt_string(passwd)
        condition = {'username=':username, 'passwd=':passwd}
        de = DataBaseEngine('hf_manager')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)

        if result == -1:
            return -1
        elif result == []:
            return -2

        location_info = SearchLocationByIP().search_location(login_ip)
        login_info, current_time = self.mp.handle_login_info(result[0]['manager_id'], location_info)

        #将登录时间,最后登录ip更新入管理员表
        update_item = {'last_login_time':current_time, 'last_login_ip':login_info['login_ip']}
        condition = {'manager_id=':result[0]['manager_id']}
        operate_type = 'update'
        de.operate_database(operate_type=operate_type, operate_item=update_item, operate_condition=condition)

        #将登录信息写入登录日志表
        de = DataBaseEngine('hf_login_log_manager')
        operate_type = 'insert'
        de.operate_database(operate_type=operate_type, operate_item=login_info)

        return result[0]['real_name'], result[0]['profile_pic_url'],result[0]['manager_id']

    def register(self, apply_info):
        '''
        此方法用以实现允许高权限管理员添加低权限管理员
            1.判断session有效性
            2.判断登录用户权限
            3.将新增管理员信息写入数据库
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
        数据结构
        apply_info = {
            'session_info':{'session_id','verify_code'},
            'register_info':{'username','passwd', 'real_name', 'telephone', 'authority', 'manager_menu':[1,2,...]}}

        :return:
            -1                               连接失败
            -2                               session失效
            -3                               权限不足
            -4                               用户名重复
            1                                成功
        '''
        #处理传入信息
        session_info, add_manager_info, manager_menu_info = self.mp.hanlde_registerInfo(apply_info)

        #验证session的有效性
        vs = VerifySession()
        verify_result = vs.verify_session_manager(session_info)

        #如果无效，返回-2
        if not verify_result:
            return -2

        #获取当前用户的id和对应表名
        gis = GetIdFromSession()
        manager_id, table_name = gis.get_id_from_session(session_info)

        #获取当前用户的权限
        condition = {'manager_id = ':manager_id}
        manager_info = self.get_manager(condition)

        #判断用户权限是否足够
        if manager_info == -1:
            return manager_info
        elif manager_info[0]['authority'] != 1:
            return -3

        # 验证用户名是否已经被注册
        c = {'username=': add_manager_info['username']}
        manager_if = self.get_manager(c)
        if manager_if:
            return -4

        #将管理员信息加密后写入管理员表
        e = EncryptString()
        add_manager_info['passwd'] = e.encrypt_string(add_manager_info['passwd'])
        de = DataBaseEngine('hf_manager')
        operate_type = 'insert'
        result = de.operate_database(operate_type=operate_type, operate_item=add_manager_info)
        if result == -1:
            return result

        #将管理员菜单信息存入管理员菜单关系表
        #处理管理员菜单数据
        de = DataBaseEngine('hf_manager_menu')
        manager_menu_list = self.mp.handle_managerMenu(result, manager_menu_info)
        operate_type = 'insertMany'
        result = de.operate_database(operate_type=operate_type, operate_item=manager_menu_list)
        return result

    def get_manager(self, condition):

        de = DataBaseEngine("hf_manager")
        operate_type = "select"
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        return result

    def delete_manager(self, condition):
        pass

    def add_product(self, product_info, manager_id):
        '''
        此方法用以允许管理员添加商品
        :param product_info                             商品信息
            :param basic_info                           基本信息
                :param product_name                     商品名字
                :param brief                            简介
                :param description                      描述
                :param product_type                     商品类型 0普通商品，1认领模式的商品
                :param is_hot                           是否是热门商品,
                :param stock                            库存量（认领模式的商品，默认为1而且不能修改）
                :param attribute                        属性
            :param sub_info                             补充信息(普通商品)
                :param  market_price                    市场价
                :param shop_price                       电商价
                :param promote_price                    折扣价
                :param promote_start_date               折扣开始时间
                :param promote_end_date                 折扣结束时间
            :param sub_info                             补充信息（认领商品）
                :param first_pay                        首次所需付款
                :param each_month_pay                   每月所需付款
                :param need_to_pay_month                需付多少个月
            :param product_category_info                商品类别信息
                :param category_id                      类别id
            :param product_gallery_info                 商品图片信息
                :param img_url                          图片地址
                :param is_main                          是否是主图
            :param product_property_info                商品特性信息
                :param property_name                    特性名字
                :param property_content                 特性内容
        ps:根据商品类型选择对应的sub_info所需要的参数
        数据结构(此次以普通商品为例)
        apply_info = {
            'session_info':{'session_id','verify_code'},
            'product_info':{
                'basic_info':{'product_name','brief','description','product_type','is_hot','stock'},
                'sub_info':{'market_price', 'shop_price', 'promote_price','promote_start_date','promote_end_date'},
                'product_category_info':[id1, id2, di3...],
                'product_gallery_info':[{'img_url','is_main'},{'img_url','is_main'}],
                'product_property_info':[{'property_name','property_content'}]
            }
        }

        :return:
        -1                                                   连接失败
        -2                                                   session失效
        1                                                    成功
        '''
        product_basic_info, product_sub_info, product_category_info, \
        product_act_log_info, product_property_info \
            = self.mp.handle_product_info(product_info, manager_id)

        #存入商品基本信息
        product_id = Product().insert_product(product_basic_info)
        if product_id == -1:
            return product_id

        product_sub_info['product_id'] = product_id
        product_act_log_info['product_id'] = product_id
        product_category_info = self.mp.handle_product_category_info(product_id, product_category_info)
        product_property_info = self.mp.handle_product_property_info(product_id, product_property_info)

        if product_basic_info['product_type'] != 1:
            sub_table = 'hf_product_normal'
        else:
            sub_table = 'hf_product_subscription'

        #存入商品补充信息
        de = DataBaseEngine(sub_table)
        operate_type = 'insert'
        de.operate_database(operate_type=operate_type, operate_item=product_sub_info)

        #存入商品类别信息
        de = DataBaseEngine('hf_product_category')
        operate_type = 'insertMany'
        de.operate_database(operate_type=operate_type, operate_item=product_category_info)

        #存入商品特性信息
        de = DataBaseEngine('hf_product_property')
        operate_type = 'insertMany'
        if len(product_property_info)!=0:
            de.operate_database(operate_type=operate_type, operate_item=product_property_info)

        #存入商品操作信息
        return 1, product_act_log_info

    def delete_product(self, product_id, manager_id):

        '''
        删除商品
        :param product_id:          商品id
        :param manager_id           管理员id
        :return:
        '''
        #删除商品，将商品is_delete字段修改为1
        de = DataBaseEngine('hf_product')
        operte_type = 'update'
        up_item = {'is_delete':1}
        condition = {'product_id=':product_id}
        result = de.operate_database(operate_type=operte_type, operate_item=up_item, operate_condition=condition)

        if result == -1:
            return result

        #将操作更新入操作表
        log_info = {'product_id':product_id, 'manager_id':manager_id,
                    'act_type_id':2, 'act_time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}
        self.add_product_log_act(log_info)

        return result

    def add_product_log_act(self, log_info):

        de = DataBaseEngine('hf_product_act_log')
        operate_type = 'insert'
        de.operate_database(operate_type=operate_type, operate_item=log_info)

    def modify_product(self, apply_info):
        pass

    def get_new_event(self):

        '''
        获取新事件
        :return:
        '''
        de = DataBaseEngine('hf_new_event')
        select_item = {'COUNT(*)':0}
        operate_type = 'select'
        #新增用户
        condition_1 = {'event_type=':1}
        #新收消息
        condition_2 = {'event_type=': 2}
        #新接订单
        condition_3 = {'event_type=': 3}

        result_1 = de.operate_database(operate_type=operate_type, operate_item=select_item, operate_condition=condition_1)
        result_2 = de.operate_database(operate_type=operate_type, operate_item=select_item, operate_condition=condition_2)
        result_3 = de.operate_database(operate_type=operate_type, operate_item=select_item, operate_condition=condition_3)

        operate_type = 'delete'
        condition = {'1=':0}
        de.operate_database(operate_type=operate_type, operate_condition=condition)

        return result_1[0]['COUNT(*)'],result_2[0]['COUNT(*)'],result_3[0]['COUNT(*)']

    def get_sales_quantity(self, delta_number, right_date, get_type):

        '''
        获取最近10天的商品销售量
        :param delta_days
        :param right_date                   时间右区间
        :param get_type                     获取类型，1-按天，2-按月，3-按年
        :param
        :return:
        '''
        quantity_list_all = []

        date_list, delta_date = self.mp.handle_sale_quantity_date(right_date, delta_number, get_type)
        de = DataBaseEngine('hf_order')
        operate_type = 'select'
        operate_item = {'product_quantity':0}

        #获取普通商品的销售量
        quantity_list_nor = []
        for item in date_list:
            condition = {'NOT product_type=':1, 'create_time LIKE':item+'%%'}
            result = de.operate_database(operate_type=operate_type,operate_item=operate_item,
                                         operate_condition=condition)
            if result == -1:
                return result

            if len(result) != 0:
                temp_quan = 0
                for item_1 in result:
                    temp_quan = temp_quan + int(item_1['product_quantity'])
                quantity_list_nor.append(temp_quan)
            else:
                quantity_list_nor.append(0)
        quantity_list_all.append(quantity_list_nor)
        # 获取领养商品的销售量
        quantity_list_sub = []
        for item in date_list:
            condition = {'product_type=': 1, 'create_time LIKE ': item + '%%'}
            result = de.operate_database(operate_type=operate_type, operate_item=operate_item,
                                         operate_condition=condition)
            if result == -1:
                return result

            if len(result) != 0:
                temp_quan = 0
                for item_1 in result:
                    temp_quan = temp_quan + int(item_1['product_quantity'])
                    quantity_list_sub.append(temp_quan)
            else:
                quantity_list_sub.append(0)
        quantity_list_all.append(quantity_list_sub)

        return quantity_list_all, delta_date

    def get_income(self, get_type, right_date, delta_number, product_type=-1):

        '''
        获取营业额
        :param condition
        :param get_type                     获取类型，1-按天，2-按月，3-按年
        :return:
        '''
        date_list, delta_date = self.mp.handle_sale_quantity_date(right_date, delta_number, get_type)
        subtotal_list = []

        table_list = [{'hf_order-hf_order_sub_payment_log':'order_id'}]
        operate_type = 'selectconnect'
        de = DataBaseEngine(table_list)
        for item in date_list:
            condition = self.mp.handle_income_condition(product_type, item)
            result = de.operate_database(operate_type=operate_type, operate_condition=condition)
            subtotal = self.mp.handle_income(result)
            subtotal_list.insert(0,subtotal)
        return subtotal_list, date_list

    def get_product_type(self, condition = None):

        if condition == None:
            condition = {'1=':1}
        de = DataBaseEngine('hf_product_type')
        result = de.operate_database(operate_type='select',operate_condition=condition)
        return result

    def get_category(self, condition, supstring):

        condition['is_delete='] = 0
        result = People().get_category(condition, supstring)
        return result

    def browse_message(self, condition, supstring, page_number, manager_id):

        '''
        获取管理员信息
        :param condition:
        :param supstring:
        :return:
        '''
        msg_start = (page_number-1)*10
        supstring = supstring + " LIMIT %d, 10 "%(msg_start)

        de = DataBaseEngine('hf_message')
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type,operate_condition=condition,supstring=supstring)

        count = int(self.count_message(condition))

        if result == -1:
            return -1,-1

        message_info = []
        #获取发送者信息
        for item in result:
            message_type_id = item['message_type_id']
            condition_s, table_name = self.mp.handle_message_type(message_type_id, item, manager_id)
            de_s = DataBaseEngine(table_name)
            operate_type = 'select'
            result_s = de_s.operate_database(operate_type=operate_type, operate_condition=condition_s)

            if result_s == -1 or len(result_s) == 0:
                return -1,-1

            temp_dict = ManagerPO().handle_browse_message_info(item, result_s[0], message_type_id)
            message_info.append(temp_dict)

        return message_info, count

    def count_message(self, condition):

        de = DataBaseEngine('hf_message')
        operate_type = 'select'
        select_item = {'COUNT(*)': 0}
        count = de.operate_database(operate_type=operate_type, operate_condition=condition, operate_item=select_item)
        count = int(count[0]['COUNT(*)'])
        return count

    def delete_message(self, message_id_list):

        result = People().delete_message(message_id_list)
        return result

    def mark_messageReaded(self, message_id_list, manager_id):

        result = People().mark_messageReaded(message_id_list, manager_id)
        return result

    def mark_messageImportant(self, message_id_list):

        result = People().mark_messageImportant(message_id_list)
        return result

    def send_message(self,message_info, manager_id):

        '''
        允许管理员发送消息
        :param message_info:
            :param content
            :param title
            :param reciver_id_list                  [id1, id2, id3]
            :param is_important
            :param message_type_id
        :return:
        '''
        insert_item = self.mp.handle_send_message_info(message_info, manager_id)
        de = DataBaseEngine('hf_message')
        operate_type = 'insertMany'
        result = de.operate_database(operate_type=operate_type, operate_item=insert_item)

        return result

    def browse_product(self, condition, page_number, supstring, need_count=1):

        '''
        查看商品列表
        :param condition:
        :param page_number:
        :param substring:
        :return:
        '''
        condition['is_delete='] = 0
        if need_count==1:
            result, count = People().browse_product(condition,page_number,12,supstring, need_count)
        else:
            count = 1
            result = People().browse_product(condition,page_number,12,supstring, need_count)
        product_list = self.mp.handle_product_list_info(result)

        return product_list, count

    def browse_product_by_category(self, condition, page_number, supstring):

        result, count = People().browse_product_by_category(condition=condition, page_number=page_number,
                                                            supstring=supstring, need_count=1)
        product_list = self.mp.handle_product_list_info(result)
        return product_list, count

    def get_user(self):

        condition = {'1=':1}
        supstring = ' ORDER BY register_time DESC'
        result = People().get_user(condition, supstring)
        return result

    def get_login_log(self, condition):

        table_name = [{'hf_manager-hf_login_log_manager':'manager_id'}]
        condition['hf_login_log_manager.manager_id IS NOT NULL'] = ''
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return result
        login_log = self.mp.handle_login_log(result)
        return login_log

    def get_order_act_log(self, condition):

        table_name = [
            {'hf_manager-hf_manager_actorder_log':'manager_id'},
            {'hf_manager_actorder_log-hf_order':'order_id'},
            {'hf_manager_actorder_log-hf_actorder_type':'act_type_id'}
        ]
        condition['hf_manager_actorder_log.manager_id IS NOT NULL']=''
        condition['hf_order.order_id IS NOT NULL']=''
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return result

        order_act_log = self.mp.handle_orderact_log(result)
        return order_act_log

    def get_product_act_log(self, condition):

        table_name = [
            {'hf_manager-hf_product_act_log':'manager_id'},
            {'hf_product_act_log-hf_product':'product_id'},
            {'hf_product_act_log-hf_act_type':'act_type_id'}
        ]
        condition['hf_product_act_log.manager_id IS NOT NULL'] = ''
        condition['hf_product.product_id IS NOT NULL'] = ''
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return -1

        product_act_log = self.mp.handle_product_act_log(result)
        return product_act_log

    def get_count_manager(self, delta_number, right_date, get_type, condition, time_name, table_name):

        #get_type           1-days, 2-month, 3-years
        count_msg_list = []

        date_list, delta_date = self.mp.handle_sale_quantity_date(right_date, delta_number, get_type)

        de = DataBaseEngine(table_name)
        operate_type = 'select'
        operate_item = {'COUNT(*)':0}

        for item in date_list:
            condition[time_name + ' LIKE '] = item + '%%'
            result = de.operate_database(operate_type=operate_type, operate_condition=condition, operate_item=operate_item)
            if result == -1:
                return result

            count_msg_list.append(int(result[0]['COUNT(*)']))

        return count_msg_list, delta_date, date_list

    def get_count_quantity(self, delta_number, right_date, get_type, condition, time_name, table_name, feild_name):

        count_msg_list = []

        date_list, delta_date = self.mp.handle_sale_quantity_date(right_date, delta_number, get_type)

        de = DataBaseEngine(table_name)
        operate_type = 'select'


        for item in date_list:
            count_total = 0
            condition[time_name + ' LIKE '] = item + '%%'
            result = de.operate_database(operate_type=operate_type, operate_condition=condition)
            if result == -1:
                return result
            for item in result:
                count_total = count_total + float(item[feild_name])
            count_msg_list.append(count_total)

        return count_msg_list, delta_date, date_list

    def get_sales_total(self,condition):

        de = DataBaseEngine('hf_order')
        operate_item = {'COUNT(*)':0}
        operate_type = 'select'
        result = de.operate_database(operate_type=operate_type, operate_item=operate_item, operate_condition=condition)
        return int(result[0]['COUNT(*)'])

    def get_income_total(self, condition):

        table_list = [{'hf_order-hf_order_sub_payment_log': 'order_id'}]
        de = DataBaseEngine(table_list)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        if result == -1:
            return -1

        subtotal = self.mp.handle_income_total(result)
        return subtotal

    def get_product_category(self, condition):

        table_name = [{'hf_product_category-hf_category':'category_id'}]
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type, operate_condition=condition)
        return result

    def get_product_property(self, condition):

        property_info = People().get_product_property(condition)
        return property_info

    def get_product_order(self, condition, supstring):

        table_name = [{'hf_order-hf_user':'user_id'}]
        de = DataBaseEngine(table_name)
        operate_type = 'selectconnect'
        result = de.operate_database(operate_type=operate_type,operate_condition=condition,supstring=supstring)

        if result == -1:
            return result

        order_list = self.mp.handle_product_order(result)
        return order_list

    def get_payment_log(self, condition, supstring):
        pass


