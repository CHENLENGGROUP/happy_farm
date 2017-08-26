$('#article_info_form').submit(function(){
    var title = $('#title').val();
    var subtitle = $('#subtitle').val();
    var brief = $('#brief').val();
    var content = $($(".wysihtml5-sandbox")[0]).contents().find("body")[0].innerHTML;
    var data = {
        "title":title,
        "subtitle":subtitle,
        "brief":brief,
        "content":content,
    };
    $.ajax({
       type: "post",
       dataType: "json",
       url: "http://127.0.0.1:8000/manageraddarticle",
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
