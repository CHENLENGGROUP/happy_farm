/**
 * Created by franksmac on 10/18/17.
 */
$(document).ready(function () {
    // 动态绑定事件
    $("tbody").on('click', '#operation .confirm_btn', function(){
        var order_id = $(this).attr("data-content");
        swal({
            title: "确认订单？",
            text: "是否确认订单，确认后无法更改",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#566FC9",
            confirmButtonText: "确定",
            cancelButtonText:"取消",
            closeOnConfirm: false
        },function () {
            var url = "/managerupdateorder?order_id="+order_id;
            do_ajax(url);
        });
    });

    $("tbody").on('click', '#operation .confirmed_btn', function(){
      swal("该订单已被确认");
    });
});

function do_ajax(url) {
    $.ajax({
        type:"get",
        url:url,
        timeout:10000,
        success:function (Data) {
            if(Data.ret!==re_code.success){
                swal("操作失败","错误代码:"+Data.ret, "error");
                return false;
            }
            else{
                swal("操作成功", "确认订单成功", "success");
            }
        },
        error:function () {
            swal("操作失败","错误代码:000001", "error");
        }
    })
}

