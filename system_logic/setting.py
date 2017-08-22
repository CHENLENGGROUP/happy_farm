# -*- coding: utf-8 -*-

#---------------mysql---------------
host = '127.0.0.1'
user = 'root'
passwd = ''
db = 'happyfarm'

#---------------rule for calculating bouns---------------



prefix = 'hf_'

session_valid_days = 50


#---------------云之讯连接参数---------------
account_sid = '354fbfb43d1644ddb6d98218210247d8'
account_token = '235cc862b5502b5f8c8f5d4c43cbb451'
api_url = 'https://api.ucpaas.com'
app_id = '3ed6a9f4cfc045cab23cd752f1869a28'
template_id = '77509'
template_id_notify = '103870'
code_expire = '10'
port = ''
soft_version = '2014-06-30'
JSON = 'json'


#---------------返回码---------------
re_code = {
    'connect_error':'000001',
    'session_error':'000002',
    'passwd_incorrect':'000003',
    'username_exist':'000004',
    'telephon_exist':'000005',
    'verify_error':'000006',
    'parameter_error':'000007',
    'limit_exceeded':'000008',
    'success':'000000'
}

#---------------头像储存位置---------------
profile_pic_prifix = 'propic_'
profile_pic_extension = '.jpg'
profile_pic_store_address = '../../../static/img/profile_pic/'

#---------------管理页面title---------------
webpage_title = {
    '主页':'幸福农场后端管理-首页',
    '添加商品':'幸福农场后端管理-添加商品',
    '消息列表':'幸福农场后端管理-查看信息',
    '用户列表':'幸福农场后端管理-查看用户',
    '商品列表':'幸福农场后端管理-商品列表',
    '员工列表':'幸福农场后端管理-员工列表',
<<<<<<< HEAD
    '添加文章':'幸福农场后端管理-添加文章'
=======
    '添加管理员':'幸福农场后端管理-添加管理员',
>>>>>>> 7af4bfcb10379bde62c29e92ad33ee0ce9a12d58
}

#---------------管理页面关系---------------
webpage_relationship = {
    '主页':{'parent':'','grandparent':''},
    '添加商品':{'parent':'商品管理','grandparent':'主页'},
    '消息列表':{'parent':'消息管理','grandparent':'主页'},
    '用户列表':{'parent':'用户管理','grandparent':'主页'},
    '商品列表':{'parent':'商品管理','grandparent':'主页'},
    '员工列表':{'parent':'员工管理','grandparent':'主页'},
<<<<<<< HEAD
    '添加文章':{'parent':'文章管理','grandparent':'主页'},
=======
    '添加管理员':{'parent':'员工管理','grandparent':'主页'},
>>>>>>> 7af4bfcb10379bde62c29e92ad33ee0ce9a12d58
}

