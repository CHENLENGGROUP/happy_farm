$('#manager_info_form').submit(function(){
    var username = $('#username').val();
    var real_name = $('#real_name').val();
    var telephone = $('#telephone').val();
    var password = $('#password').val();
    var confirmpassword = $('#confirmPassword').val();
    var authority = $('#authority').find("option:selected").attr("db_id")

    if(authority == "-1"){
        $("#authority").parent().parent().addClass("has-error has-danger");
        swal("请选择管理员权限","","error");
        return;
    }
    else{
        $("#authority").parent().parent().removeClass("has-error has-danger");
    }

    if(!verify_input(username, password, confirmpassword, telephone)){
        swal("输入不符合规则","请检查后重新输入","error");
        return
    }

    var data = {
        "username":username,
        "real_name":real_name,
        "telephone":telephone,
        "passwd":password,
        "authority":authority
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
        switch_button_status($('#manager_info_sub'));
        do_ajax(data);
    })
});

function verify_input(username, passwd, confirm_passwd, telephone){

    var result = 0;
    if(!/[a-z]/.test(username)){
        $('#username').parent().addClass('has-error has-danger');
        result = 1;
    }
    else{
        $('#username').parent().removeClass('has-error has-danger');
    }
    if(passwd.length<6){
        $('#password').parent().addClass('has-error has-danger');
        result = 1;
    }
    else{
        $('#password').parent().removeClass('has-error has-danger');
    }
    if(passwd!=confirm_passwd){
        $('#confirmPassword').parent().addClass('has-error has-danger');
        result=1;
    }
    else{
        $('#confirmPassword').parent().removeClass('has-error has-danger');
    }
    if(!/^1[34578]\d{9}$/.test(telephone)){
        $('#telephone').parent().addClass('has-error has-danger');
        result = 1;
    }
    else{
        $('#telephone').parent().removeClass('has-error has-danger');
    }
    if(result==1){
        return false
    }
    return true
}

function do_ajax(data){
    $.ajax({
       type: "post",
       dataType: "json",
       url: "http://127.0.0.1:8000/manageraddmanager",
       timeout:10000,
       data: JSON.stringify(data),
       success: function(Data){
           var ret = Data.ret;
           if(ret === re_code.connect_error){
               swal("连接失败，请稍候再试","错误代码"+ret,'error');
           }
           else if(ret === re_code.verify_error){
               swal("对不起，您没有足够的权限","请确认登录帐号的权限后再操作","error")
           }
           else if(ret === re_code.username_exist){
               swal("注册用户名已存在","请修改用户名后再尝试注册","error")
           }
           else{
               swal("添加成功","","success");
           }
           switch_button_status($('#manager_info_sub'));
       },
       error: function (Data) {
            swal("连接失败","错误代码000001","error");
            switch_button_status($('#manager_info_sub'));
       }
   });
}

function switch_button_status(button_elem){
    var btn_elem = $(button_elem);
    var children_list = btn_elem.children();
    if(btn_elem.hasClass("btn-anim")){
        btn_elem.removeClass("btn-anim");
        btn_elem.addClass("disabled");
        $(children_list[0]).css("display","none");
        $(children_list[1]).html("提交中...");
        $(children_list[2]).css("display","inline-block");
    }
    else{
        btn_elem.addClass("btn-anim");
        btn_elem.removeClass("disabled");
        $(children_list[0]).css("display","inline-block");
        $(children_list[1]).html("提交");
        $(children_list[2]).css("display","none");
    }
}