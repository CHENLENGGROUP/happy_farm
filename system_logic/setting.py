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
    '员工分析':'员工分析-幸福农场后端管理',

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
    '商品列表':{'parent':'商品管理','url':'/managerbrowseproductlist'},
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
    '员工分析':{'parent':'员工管理', 'url':'/manageruseranalysis'},
}

#---------------颜色代码---------------
region_color_dict = {
    '0-50':'#2894FF',
    '50-100':'#0080FF',
    '100-150':'#0072E3',
    '150-200':'#0066CC',
    '200-250':'#005AB5',
    '250-300':'#004B97',
    '300':'#003D79'
}

#---------------颜色代码---------------
region_code = {
    u'江苏':'CN-32',
    u'贵州':'CN-52',
    u'云南':'CN-52',
    u'重庆':'CN-50',
    u'四川':'CN-51',
    u'上海':'CN-31',
    u'西藏':'CN-54',
    u'浙江':'CN-33',
    u'内蒙古':'CN-15',
    u'山西':'CN-14',
    u'福建':'CN-',
    u'天津':'CN-12',
    u'河北':'CN-13',
    u'北京':'CN-11',
    u'安徽':'CN-34',
    u'江西':'CN-36',
    u'山东':'CN-37',
    u'河南':'CN-41',
    u'湖南':'CN-43',
    u'湖北':'CN-42',
    u'广西':'CN-45',
    u'广东':'CN-44',
    u'海南':'CN-46',
    u'新疆':'CN-65',
    u'宁夏':'CN-64',
    u'青海':'CN-63',
    u'甘肃':'CN-62',
    u'陕西':'CN-61',
    u'黑龙江':'CN-23',
    u'吉林':'CN-22',
    u'辽宁':'CN-21',
}

default_region_user = [
    {u'江苏': 0},
    {u'贵州': 0},
    {u'云南': 0},
    {u'重庆': 0},
    {u'四川': 0},
    {u'上海': 0},
    {u'西藏':0},
    {u'浙江': 0},
    {u'内蒙古': 0},
    {u'山西': 0},
    {u'福建': 0},
    {u'天津': 0},
    {u'河北': 0},
    {u'北京': 0},
    {u'安徽': 0},
    {u'江西': 0},
    {u'山东': 0},
    {u'河南': 0},
    {u'湖南': 0},
    {u'湖北': 0},
    {u'广西': 0},
    {u'广东': 0},
    {u'海南': 0},
    {u'新疆': 0},
    {u'宁夏': 0},
    {u'青海': 0},
    {u'甘肃': 0},
    {u'陕西': 0},
    {u'黑龙江': 0},
    {u'吉林': 0},
    {u'辽宁': 0},
    {u'未知':0}
]