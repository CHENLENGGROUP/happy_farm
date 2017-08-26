# -*- coding: utf-8 -*-

class PageAddProductPO:

    def handle_category_list(self, category_list):

        '''

        :param category_list:
        :return:
        category_info = {'level_count', 'category_info':{'cate_1','cate_2'...}}
        '''
        category_info = {}

        #计算有多少级
        cate_sperate_list = []
        temp_list = category_list
        root_list = [0]
        count_used = 0
        while True:
            temp_sperate_list = []
            temp_root_list = []
            for item in temp_list:
                for parent_id in root_list:
                    if item['parent_category_id'] == parent_id:
                        temp_sperate_list.append(item)
                        temp_root_list.append(item['category_id'])
                        count_used = count_used+1
            cate_sperate_list.append(temp_sperate_list)
            root_list = temp_root_list
            if count_used == len(temp_list):
                break

        return cate_sperate_list

    def handle_category_list_disabled(self, category_list, product_category_list):

        p_id = 0
        for i in range(0, len(category_list)):
            temp_p_id = -1
            track = 0
            for j in range(0, len(category_list[i])):

                try:
                    s_id = product_category_list[i][0]['category_id']
                except:
                    s_id = -1

                if category_list[i][j]['parent_category_id'] == p_id:
                    if track == 0:
                        temp_p_id = category_list[i][j]['category_id']
                        track = 1
                    if category_list[i][j]['category_id'] == s_id:
                        temp_p_id = category_list[i][j]['category_id']
                        category_list[i][j]['selected'] = 'true'
                    else:
                        category_list[i][j]['selected'] = 'false'
                    category_list[i][j]['disabled'] = 'false'
                else:
                    category_list[i][j]['disabled'] = 'true'
                    category_list[i][j]['selected'] = 'false'

            p_id = temp_p_id
        return category_list
