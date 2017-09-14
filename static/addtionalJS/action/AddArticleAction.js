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
    swal({
        title: '确定提交？',
        text: '提交后，可在文章列表查看',
        type: 'info',
        showCancelButton: true,
        confirmButtonColor: "#566FC9",
        confirmButtonText: "确定",
        cancelButtonText:"取消",
        closeOnConfirm: false
    },function () {
        switch_button_status($('#article_info_sub'));
        do_ajax(data);
    })
});

function do_ajax(data){
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
               switch_button_status($('#article_info_sub'));
           }
           else{
               swal("添加成功","","success");
               switch_button_status($('#article_info_sub'));
           }
       },
       error: function (Data) {
            swal("连接失败","错误代码000001","error");
            switch_button_status($('#article_info_sub'));
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