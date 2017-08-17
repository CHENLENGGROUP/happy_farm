/**
 * Created by Administrator on 2017/8/16 0016.
 */
(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r !== null) return unescape(r[2]); return null;
    }
})(jQuery);
var page_number_init=0;

$(document).ready(function () {

    //翻页
    $("#paging_ui li").each(function () {
        if ($(this).hasClass("active")) {
            page_number_init=parseInt($(this).find("a").html());
        }
        $(this).click(function () {
            var box_type =  $.getUrlParam("box_type");
            var is_read = $.getUrlParam("is_read");
            var page_number = 1;
            if($(this).hasClass("disabled")||$(this).hasClass("active")){
                return false;
            }
            if($(this).hasClass("arrow-left")){
                page_number=page_number_init-1;
                page_number_init--;
            }
            else if($(this).hasClass("arrow-right")){
                page_number=page_number_init+1;
                page_number_init++;
            }
            else {
                page_number=parseInt($(this).find("a").html());
                page_number_init = page_number;
            }
            do_ajax(page_number,box_type,is_read);
        })
    });

    //点击跳转邮件详细页
    $("table tbody tr ").on("click", ".view-message",function () {
        var href = $(this).attr("href");
        window.open("http://www.baidu.com");
    });

    //勾选全选
    $("#checkbox051").click(function () {
        if($(this).is(":checked")){
            $("[name = msg_checkbox]:checkbox").prop("checked",'true');
        }
        else {
            $("[name = msg_checkbox]:checkbox").removeAttr("checked");
        }
    });

    //删除,标记已读,重要邮件
    $(".handle_msg").click(function () {
        url = $(this).attr("url");
        act_type = $(this).attr("title");
        var title = act_type+"选中信息";
        var text = $(this).attr("text");
        var cb_list = $("tbody").find("input[type='checkbox']:checked");
        message_id_list = new Array();
        for(var i=0;i<cb_list.length;i++){
            message_id_list.push($(cb_list[i]).attr("msg_id"));
        }
        if(message_id_list.length===0){
            sweetAlert("违规操作","请至少选中一条数据", "error");
            return false;
        }
        var succ_func = "do_ajax_nor(text)";
        var a = sweet_alert_btn(title,text,"info", true, succ_func);
    });

    //发送信息
    $("#send_msg").click(function () {
        var input_list = $(this).parent().parent().parent().find(".send_msg_info");
        for(var i=0;i<input_list.length;i++){
            var tag_name = $(input_list[i]).context.tagName;
            if(tag_name.toUpperCase()==="SELECT"){
                var receiver_id_list = [];
                var select_list = $(input_list[i]).find("option:selected");
                for(var j=0;j<select_list.length;j++){
                    receiver_id_list.push(parseInt($(select_list[j]).attr("value")));
                }
                console.log(receiver_id_list);
            }
            else {
                var content = $(".wysihtml5-sandbox").contents().find("body")[0].innerHTML;
                console.log(content)
            }
        }
    })
});

function do_ajax(page_number, box_type,is_read){
    var json_data = {
        "page_number":page_number,
        "box_type":box_type,
        "is_read":is_read
    };
    $.ajax({
        type:"post",
        dataType:"json",
        url:"http://127.0.0.1:8000/managerbrowsemessage",
        data:JSON.stringify(json_data),
        timeout:10000,
        success:function (Data) {
            if(Data.ret===re_code.connect_error){
                sweetAlert("连接失败，请稍候再试","错误代码:"+Data.ret, "error");
                return false;
            }
            clear_table();
            for(var i=0;i<Data.message_list.length;i++){
                var h_str = set_html_str(Data.message_list[i]);
                $('table tbody').append(h_str);
            }
            switch_active(page_number);
        },
        error:function () {
            sweetAlert("连接失败，请稍候再试","错误代码:000001", "error");
        }
    })
}

function clear_table(){
    $("table tbody").empty();
}

function set_html_str(item){
    var is_read_str = '';
    if(parseInt(item.is_read)===0){
        is_read_str = 'unread'
    }
    var star_color = "#adadad";
    if(parseInt(item.is_important)===1){
        star_color = "#fcb03b"
    }
    var message_id = parseInt(item.message_id);
    var sender_id = parseInt(item.sender_id);
    var sender_type = item.sender_type;
    var sender_name = item.sender_name;
    var content = item.content;
    var sende_tiem = item.send_time;
    var html_str =
        '<tr class="'+is_read_str+'" href="/managerbrowsemessageDetail?message_id='+message_id+'&sender_id='+sender_id+'&sender_type='+sender_type+'">' +
            '<td class="inbox-small-cells">' +
                '<div class="checkbox checkbox-default">' +
                    '<input type="checkbox" id="checkbox'+message_id+'" name="msg_checkbox"/>' +
                    '<label for="checkbox'+message_id+'"></label>' +
                '</div>' +
            '</td>' +
            '<td class="inbox-small-cells"><i class="fa fa-star" style="color:'+star_color+'"></i></td>' +
            '<td class="view-message  dont-show">'+sender_name+'</td>' +
            '<td class="view-message ">'+content+'</td>' +
            '<td class="view-message  text-right">'+sende_tiem+'</td>' +
        '</tr>';
    return html_str
}

function switch_active(page_number){
    var ul_list = $("#paging_ui").find("li");
    var len = ul_list.length;
    if(page_number===1){
        $(ul_list[0]).addClass("disabled");
        $(ul_list[len-1]).removeClass("disabled");
    }
    else if(page_number===len-2){
        $(ul_list[len-1]).addClass("disabled");
        $(ul_list[0]).removeClass("disabled");
    }
    else{
        $(ul_list[len-1]).removeClass("disabled");
        $(ul_list[0]).removeClass("disabled");
    }

    for(var i=1;i<len-1;i++){
        var number = parseInt($(ul_list[i]).find("a").html());
        if(number===page_number){
            $(ul_list[i]).addClass("active");
        }
        else {
            $(ul_list[i]).removeClass("active");
        }
    }
}

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
            if(Data.ret===re_code.connect_error){
                sweetAlert(title_e,"错误代码:"+Data.ret, "error");
                return false;
            }
            else{
                sweet_alert_btn(title_s, text, "success", false, "window.location.reload()")
            }
        },
        error:function () {
            sweetAlert(title_e,"错误代码:000001", "error");
        }
    })
}

function do_ajax_send_msg(reciver_id_list, content){

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