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
    '添加商品':'添加商品-幸福农场后端管理',
    '消息列表':'查看信息-幸福农场后端管理',
    '用户列表':'查看用户-幸福农场后端管理',
    '商品列表':'商品列表-幸福农场后端管理',
    '商品明细':'商品明细-幸福农场后端管理',
    '员工列表':'员工列表-幸福农场后端管理',
    '员工明细':'员工明细-幸福农场后端管理',
    '添加文章':'添加文章-幸福农场后端管理',
    '添加管理员':'添加管理员-幸福农场后端管理',
    '文章列表':'文章列表-幸福农场后端管理',
    '商品分析':'商品分析-幸福农场后端管理',
    '文章详细':'文章详细-幸福农场后端管理',
    '添加员工':'添加员工-幸福农场后端管理',
    '个人信息':'个人信息-幸福农场后端管理',
    '修改密码':'修改密码-幸福农场后端管理',
    '用户分析':'用户分析-幸福农场后端管理',
}

#---------------管理页面关系---------------
webpage_relationship = {
    '主页':{'parent':'','url':'/managerindex'},
    '商品管理':{'parent':'主页', 'url':'#'},
    '消息管理':{'parent':'主页', 'url':'#'},
    '用户管理':{'parent':'主页', 'url':'#'},
    '员工管理':{'parent':'主页', 'url':'#'},
    '文章管理':{'parent':'主页', 'url':'#'},
    '订单管理':{'parent':'主页', 'url':'#'},
    '添加商品':{'parent':'商品管理','url':'/manageraddproduct'},
    '商品列表':{'parent':'商品管理','url':'/managerbrowseuserlist'},
    '商品明细':{'parent':'商品列表','url':'/managerbrowseproductdetail'},
    '用户列表':{'parent':'用户管理','url':'/managerbrowseuserlist'},
    '员工列表':{'parent':'员工管理','url':'/managerbrowsemanagerlist'},
    '员工明细':{'parent':'员工列表','url':'/managerbrowseoperation'},
    '消息列表':{'parent':'消息管理','url':'/managerbrowsemessage'},
    '添加文章':{'parent':'文章管理','url':'/manageraddarticle'},
    '文章列表':{'parent':'文章管理','url':'/managerarticlelist'},
    '商品分析':{'parent':'商品管理','url':'//managerproductanalysis'},
    '文章详细':{'parent':'文章列表','url':'/managerarticlelist'},
    '添加员工':{'parent':'员工管理','url':'/manageraddmanager'},
    '个人信息':{'parent':'主页', 'url':'/managerbrowsemyaccount'},
    '修改密码':{'parent':'主页', 'url':'/managerresetpassword'},
    '用户分析':{'parent':'用户管理', 'url':'/manageruseranalysis'},
}
