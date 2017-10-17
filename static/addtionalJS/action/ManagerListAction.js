/**
 * Created by Administrator on 2017/10/17 0017.
 */
$(document).ready(function () {
    $(".delete_manager").click(function () {
        //managerdeletemanager
        var manager_id = $(this).attr("data-content");
        swal({
            title: "是否确定删除",
            text: "删除后，可以使用最高权限管理员恢复",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#566FC9",
            confirmButtonText: "确定",
            cancelButtonText:"取消",
            closeOnConfirm: false
        },function () {
            do_ajax(manager_id);
        })
    })
})

function do_ajax(manager_id){
    $.ajax({
       type: "get",
       url: "http://127.0.0.1:8000/managerdeletemanager?manager_id="+manager_id,
       timeout:10000,
       success: function(Data){
           var ret = Data.ret;
           if(ret !== re_code.success) {
               swal("连接失败，请稍候再试", "错误代码" + ret,"error");
           }
           else{
               swal("删除成功","","success");
           }
       },
       error: function (Data) {
            swal("连接失败，请稍候再试", "错误代码" + ret,"error");
       }
   });
}