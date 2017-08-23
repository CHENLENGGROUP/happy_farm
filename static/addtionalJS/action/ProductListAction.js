/**
 * Created by Administrator on 2017/8/23 0023.
 */
$(document).ready(function () {
    $(".delete_product").click(function () {
        product_id = $(this).attr("name");
        sweet_alert_btn("确认删除吗？","删除后，可以使用最高权限恢复","info","true", "ajax_delete()")
    })
})

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

function ajax_delete(){
    $.ajax({
       type: "get",
       dataType: "json",
       url: "http://127.0.0.1:8000/managerdelproduct?product_id="+product_id,
       timeout:10000,
       success: function(Data){
           var ret = Data.ret;
           if(ret !== re_code.success){
               sweet_alert_btn("连接失败，请稍候再试","错误代码"+ret, "error", false, "");
           }
           sweet_alert_btn("删除成功","删除后，可以使用最高权限恢复", "success", false, "window.location.reload()");
       },
       error: function (Data) {
            sweet_alert_btn("连接失败，请稍候再试","错误代码"+ret, "error", false, "");
       }
   });
}