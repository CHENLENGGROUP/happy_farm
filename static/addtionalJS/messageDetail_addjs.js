/**
 * Created by Administrator on 2017/8/18 0018.
 */
(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r !== null) return unescape(r[2]); return null;
    }
})(jQuery);

$(document).ready(function () {

	$(".modal-body ul").on("blur", "input",function () {
        var len = $(this).parent().prev().length;
        if(len===0){
            $(this).parent().parent().parent().parent().parent().parent().parent().addClass("has-error has-danger");
        }
        else {
            $(this).parent().parent().parent().parent().parent().parent().parent().removeClass("has-error has-danger");
        }
    })

    $("#tt").blur(function () {
        if($(this).val()===""){
            $(this).parent().parent().addClass("has-error has-danger");
        }
        else {
            $(this).parent().parent().removeClass("has-error has-danger");
        }
    })

    //回复信息
    $("#replay_msg").click(function () {
        var info_list = $(this).parent().parent().parent().find('.send_msg_info')
        if($(info_list[1]).val()===""){
            $(info_list[1]).parent().parent().addClass("has-error has-danger");
            return false;
        }
        var reciver_id_list = []
        reciver_id_list.push($(info_list[0]).attr("sender_id"));
        var sender_type = $(info_list[0]).attr("sender_type");
        var title = $(info_list[1]).val()
        var is_important = $(info_list[2]).find("option:selected").attr("db_id");
        var content = $($(".wysihtml5-sandbox")[1]).contents().find("body")[0].innerHTML;
        var message_type_id = 2
        if(sender_type === "manager"){
            message_type_id = 3;
        }

        do_ajax_send_msg(reciver_id_list, title, is_important, content, message_type_id, "myModal_replay");
    })

    //点击删除
    $("#delete_btn").click(function () {
        var message_id = $.getUrlParam("message_id");
        url = "/managerdeletemsg";
        message_id_list = [];
        message_id_list.push(parseInt(message_id));
        act_type = "删除";
        sweet_alert_btn("确认删除信息","删除后，最高权限管理员可以恢复","info",true,"do_ajax_nor(text)");
    })
})

function do_ajax_nor(text){
    var title_e = act_type+"失败，请稍候再试";
    var title_s = act_type+"成功";
    var json_data = {
        'message_id_list':message_id_list
    };
    $.ajax({
        type:"post",
        dataType:"json",
        url:url,
        data:JSON.stringify(json_data),
        timeout:10000,
        success:function (Data) {
            if(Data.ret!==re_code.success){
                sweetAlert(title_e,"错误代码:"+Data.ret, "error");
                return false;
            }
            else{
                sweet_alert_btn(title_s, text, "success", false, "history.back()")
            }
        },
        error:function () {
            sweetAlert(title_e,"错误代码:000001", "error");
        }
    })
}

function sweet_alert_btn(title, text, type, show_cb,succ_func){
    swal({
        title: title,
        text: text,
        type: type,
        showCancelButton: show_cb,
        confirmButtonColor: "#566FC9",
        confirmButtonText: "确定",
        cancelButtonText:"取消",
        closeOnConfirm: false
    },function () {
        eval(succ_func)
    })
}