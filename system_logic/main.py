# -*- coding: utf-8 -*-

import os.path
import tornado
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
from system_logic.vo.LoginPartHandler import UserLoginHandler
from system_logic.vo.LoginPartHandler import ManagerLoginHandler
from system_logic.vo import SendMessagePartHandler
from system_logic.vo import RegisterPartHandle
from system_logic.vo import BrowseProductPartHandler
from system_logic.vo import CartPartHandler
from system_logic.vo import CommentPartHandler
from system_logic.vo import CategoryPartHandler
from system_logic.vo import AddressPartHandler
from system_logic.vo import UserPartHandler
from system_logic.vo import OrderPartHandler
from system_logic.vo import MessagePartHandler
from system_logic.vo import ArticlePartHandler
from system_logic.vo import ManagerLoginHandler
from system_logic.vo import ManagerIndexHandler
from system_logic.vo import ManagerOperateProductHandler
from system_logic.vo import ManagerMessageHandler
from system_logic.vo import ManagerProductListHandler
from system_logic.vo import ManagerUserList
from system_logic.vo import ManagerProductDetailHandler
from system_logic.vo import ManagerInfoListHandler
from system_logic.vo import ManagerOperationHandler
from system_logic.vo import ManagerLogout
from system_logic.vo import ManagerAddArticleHandler
from system_logic.vo import ManagerArticleHandler
from system_logic.vo import ManagerProductAnalysisHandler
from system_logic.vo import ManagerModifyProduct
from system_logic.vo import ManagerPaymentLogHandler
from system_logic.vo import ManagerOrderActLog
from system_logic.vo import ManagerMyAccountHandler
from system_logic.vo import ManagerModifyPasswordHandler
from system_logic.vo import ManagerProductImgUpload
from system_logic.vo import ManagerUserAnalysisHandler
from system_logic.vo import ManagerAnalysisHandler
from system_logic.vo import ManagerOrderListHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/loginuser', UserLoginHandler),
            (r'/loginmanager', ManagerLoginHandler),
            (r'/registeruser', RegisterPartHandle.UserRegisterHandler),
            (r'/registermanager', RegisterPartHandle.ManagerRegisterHandler),
            (r'/sendverifysms', SendMessagePartHandler.SendVerifyMessagePartHandler),
            (r'/changetelephone', SendMessagePartHandler.ChangeTelePhoneHandler),
            (r'/browseproductuser',BrowseProductPartHandler.UserBrowseProductHandler),
            (r'/browseproductcategoryuser', BrowseProductPartHandler.UserBrowserProductCategoryHandler),
            (r'/getproductimg', BrowseProductPartHandler.GetProductImgHandler),
            (r'/getproductproperty', BrowseProductPartHandler.GetProductPropertyHandler),
            (r'/getproductcate', BrowseProductPartHandler.GetProductCategoryHanlder),
            (r'/getcartproduct',CartPartHandler.BrowseCart),
            (r'/addprotocart', CartPartHandler.AddProductToCart),
            (r'/changecartamount', CartPartHandler.ChangeCartAmount),
            (r'/deletecart', CartPartHandler.DeleteCart),
            (r'/writecomment',CommentPartHandler.WriteCommentHandler),
            (r'/getcommentuser', CommentPartHandler.UserBrowseCommentHanndler),
            (r'/getcategory', CategoryPartHandler.GetCategoryHandler),
            (r'/getaddressuser',AddressPartHandler.BrowseAddressUser),
            (r'/addaddress', AddressPartHandler.AddAddress),
            (r'/deladdress', AddressPartHandler.DeleteAddress),
            (r'/getuserinfo', UserPartHandler.BrowseUserInfoUserHandler),
            (r'/modiuserinfo', UserPartHandler.ModifyUserInfoHandler),
            (r'/uploadprofilepic', UserPartHandler.UploadProfilePicHandler),
            (r'/updatetele', UserPartHandler.UpdateUserTelephoneHandler),
            (r'/changepasswd', UserPartHandler.ChangeUserPasswordHandler),
            (r'/sendmsgtouser', MessagePartHandler.UserSendMsgToManagerHanlder),
            (r'/getnewmsgcount', MessagePartHandler.GetNewMessageCountHanlder),
            (r'/getmsg', MessagePartHandler.BrowseMessageHanlder),
            (r'/markmsgreaded', MessagePartHandler.MarkMessageReadedHandler),
            (r'/deletemsg', MessagePartHandler.DeleteMessageHanlder),
            (r'/browseorder', OrderPartHandler.BrwoseOrderHandler),
            (r'/getarticlelist', ArticlePartHandler.BrowseArticleListHandler),
            (r'/getarticledetail', ArticlePartHandler.BrowseArticleDetailHandler),
            #管理员
            (r'/managerlogin', ManagerLoginHandler.ManagerLoginHandler),
            (r'/Managerogout', ManagerLogout.ManagerLogOut),
            (r'/managerindex', ManagerIndexHandler.BrowseIndexHandle),
            (r'/manageraddproduct', ManagerOperateProductHandler.AddProductHandler),
            (r'/managerdelproduct', ManagerOperateProductHandler.DeleteProductHandler),
            (r'/managerbrowsemessage',ManagerMessageHandler.BrowseManagerMessageHanlder),
            (r'/managerbrowsemessagedetail', ManagerMessageHandler.BrowseMessgeDetailHandler),
            (r'/managerdeletemsg', ManagerMessageHandler.DeletaManagerMessageHandler),
            (r'/managermarkreaded',ManagerMessageHandler.MarkManagerMessageReadedHandler),
            (r'/managermarkimportant',ManagerMessageHandler.MarkManagerMessageImportantHandler),
            (r'/managersendmsg', ManagerMessageHandler.ManagerSendMessageHandler),
            (r'/managerbrowseproductlist', ManagerProductListHandler.BrowseProductListHandler),
            (r'/managerbrowseuserlist', ManagerUserList.BrowseUserListHandler),
            (r'/managerbrowseproductdetail', ManagerProductDetailHandler.BrowseProductDetailHandler),
            (r'/managermodiproduct', ManagerModifyProduct.ModifyProductHandler),
            (r'/managerbrowsemanagerlist', ManagerInfoListHandler.BrowseManagerListHandler),
            (r'/managerbrowseoperation', ManagerOperationHandler.BrowseManagerOperationHanlder),
            (r'/manageraddmanager', ManagerOperationHandler.AddManagerHandler),
            (r'/manageraddarticle', ManagerAddArticleHandler.addArticletHandler),
            (r'/managerarticlelist', ManagerArticleHandler.BrowseArticleListHandler),
            (r'/managerproductanalysis', ManagerProductAnalysisHandler.BrowseProductAnalysisHandler),
            (r'/managerbrowsearticledetail', ManagerArticleHandler.BrowseArticleDetailHandler),
            (r'/managerbrowsepaymentlog', ManagerPaymentLogHandler.BrowsePaymentLogHandler),
            (r'/managerbrowseorderactlog', ManagerOrderActLog.BrowseOrderActLog),
            (r'/managerbrowsemyaccount', ManagerMyAccountHandler.BrowseMyAccountHandler),
            (r'/managerresetpassword', ManagerModifyPasswordHandler.ModifyPasswordHandler),
            (r'/manageruploadproductimg', ManagerProductImgUpload.UploadProductImg),
            (r'/managerdeletearticle', ManagerArticleHandler.DeleteArticleHandler),
            (r'/manageruseranalysis', ManagerUserAnalysisHandler.BrowseUserAnalysisHandler),
            (r'/manageruploadprofileimg', ManagerProductImgUpload.UploadManagerProfileImg),
            (r'/manageranalysis', ManagerAnalysisHandler.BrowseManagerAnalysisHandler),
            (r'/managerdeletemanager',ManagerInfoListHandler.DeleteManagerHandler),
            (r'/managerbrowseorder',ManagerOrderListHandler.BrowseOrderHandler),
            (r'/managerupdateorder', ManagerOrderListHandler.ConfirmOrderHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), '../templates'),
            static_path=os.path.join(os.path.dirname(__file__), '../static'),
            debug=True,
            cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            login_url='/login',
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_secure_cookie('user')
        self.write('hello, world'+name)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
