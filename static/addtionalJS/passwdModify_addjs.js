/**
 * Created by Administrator on 2017/10/11 0011.
 */

$(document).ready(function () {

    $("#info_submit").click(function () {
        var input_list = $("form").find("input");

        var _track = 0
        input_list.each(function () {
            if($(this).val()==""){
                $(this).parent().parent().addClass("has-error has-danger");
                _track = 1;
            }
            else{
                $(this).parent().parent().removeClass("has-error has-danger");
            }
        })
        if(_track==1){
            swal("请完善必填信息","","error");
            return;
        }

        var old_passwd = $(input_list[0]).val();
        var new_passwd = $(input_list[1]).val();
        var confirm_passed = $(input_list[2]).val();

        if(new_passwd!=confirm_passed){
            swal("新密码跟确认密码不一致","","error");
            return;
        }

        if(new_passwd.length<6){
            swal("密码长度必须大于6位","","error");
            $(input_list[1]).parent().parent().addClass("has-error has-danger");
            return;
        }
        else{
            $(input_list[1]).parent().parent().removeClass("has-error has-danger");
        }

        var data = {
            "old_passwd":old_passwd,
            "new_passwd":new_passwd,
            "confirm_passed":confirm_passed,
        };

        swal({
            title: '确定提交？',
            text: '提交后，可在管理员列表查看',
            type: 'info',
            showCancelButton: true,
            confirmButtonColor: "#566FC9",
            confirmButtonText: "确定",
            cancelButtonText:"取消",
            closeOnConfirm: false
        },function () {
            do_ajax(data);
        })
    })

})

function do_ajax(data){
    $.ajax({
       type: "post",
       dataType: "json",
       url: "http://127.0.0.1:8000/managerresetpassword",
       timeout:10000,
       data: JSON.stringify(data),
       success: function(Data){
           var ret = Data.ret;
           if(ret === re_code.connect_error) {
               swal("连接失败，请稍候再试", "错误代码" + ret, 'error');
           }
           else if(ret === re_code.passwd_incorrect) {
               swal("旧密码输入错误", "错误代码" + ret, 'error');
           }
           else{
               swal({
                    title: '修改成功',
                    text: '',
                    type: 'success',
                    showCancelButton: false,
                    confirmButtonColor: "#566FC9",
                    confirmButtonText: "确定",
                    cancelButtonText:"取消",
                    closeOnConfirm: false
                },function () {
                    window.location.href="/managerbrowsemyaccount"
                })

           }
       },
       error: function (Data) {
            swal("连接失败","错误代码000001","error");
       }
   });
}