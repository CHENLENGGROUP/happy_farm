$('#manager_info_form').submit(function(){
    var username = $('#username').val();
    var real_name = $('#real_name').val();
    var telephone = $('#telephone').val();
    var password = $('#password').val();
    var confirmpassword = $('#confirmPassword').val();
    var authority = $('#authority').find("option:selected").attr("db_id")
    alert(authority)

    var data = {
        "username":username,
        "real_name":real_name,
        "telephone":telephone,
        "password":password,
        "password_com":confirmpassword,
        "authority":authority
    };
    $.ajax({
       type: "post",
       dataType: "json",
       url: "http://127.0.0.1:8000/manageraddmanager",
       timeout:10000,
       data: JSON.stringify(data),
       success: function(Data){
           var ret = Data.ret;
           if(ret !== re_code.success){
               swal("连接失败，请稍候再试","错误代码"+ret,'error');
           }
           swal("添加成功","","success");
       },
       error: function (Data) {
            swal("连接失败","错误代码000001","error");
            sweet_alert("连接失败，请稍候再试","错误代码000001");
       }
   });
});
