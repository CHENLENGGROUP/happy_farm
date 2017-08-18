/**
 * Created by Administrator on 2017/8/18 0018.
 */

$(document).ready(function () {

    $("#cc").blur(function () {
        if($(this).val()===""){
            $(this).parent().parent().addClass("has-error has-danger");
        }
        else {
            $(this).parent().parent().removeClass("has-error has-danger");
        }
    })

    $("#send_msg").click(function () {
        var input_list = $(this).parent().parent().parent().find(".send_msg_info");
        var receiver_id_list = [];
        var select_list = $(input_list[0]).find("option:selected");
        for(var j=0;j<select_list.length;j++){
            receiver_id_list.push(parseInt($(select_list[j]).attr("db_id")));
        }
        var title = $((input_list[1])).val();
        var is_important = $(input_list[2]).find("option:selected").attr("db_id");
        var content = $(".wysihtml5-sandbox").contents().find("body")[0].innerHTML;

        if(receiver_id_list.length===0&&title!=""){
            $(input_list[0]).parent().parent().addClass("has-error has-danger");
            return false;
        }
        else if(receiver_id_list.length!=0&&title==""){
            $(input[1]).parent().parent().addClass("has-error has-danger");
            return false
        }
        else if(receiver_id_list.length===0&&title==""){
            $(input_list[0]).parent().parent().addClass("has-error has-danger");
            $(input_list[1]).parent().parent().addClass("has-error has-danger");
            return false
        }

        do_ajax_send_msg(receiver_id_list, title, is_important, content, 3, "myModal")
    })
})

function do_ajax_send_msg(reciver_id_list, title, is_important, content, message_type_id, modal_name){

    var json_data = {
        'receiver_id_list':reciver_id_list,
        'title':title,
        'is_important':is_important,
        'content':content,
        'message_type_id':message_type_id
    }
    $.ajax({
        type:"post",
        dataType:"json",
        url:"http://127.0.0.1:8000/managersendmsg",
        data:JSON.stringify(json_data),
        timeout:10000,
        success:function (Data) {
            if(Data.ret!==re_code.success){
                sweetAlert("发送失败,请稍后再试","错误代码:"+Data.ret, "error");
                return false;
            }
            sweetAlert("发送成功","已成功发送，等待对方查收","success");
            $('#'+modal_name).modal("hide")
        },
        error:function () {
            sweetAlert("发送失败,请稍后再试","错误代码:000001", "error");
        }
    })
}