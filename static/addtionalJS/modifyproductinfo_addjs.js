var ele_val_arr = {};
var input = $('input');
var select = $('select');
var textarea = $('textarea');

(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r !== null) return unescape(r[2]); return null;
    }
})(jQuery);

$(document).ready(function () {
    change(input);
    change(select);
    change(textarea);
    /* Basic Init*/
	$('.dropify').dropify({
        messages:{
          'default': '点击上传图片',
          'replace': '',
          'remove':  '移除',
          'error':   '商品图片上传失败'
        },
        error:{
          'fileSize': '图片文件大于500KB，上传失败',
        },
        tpl: {
                wrap:            '<div class="dropify-wrapper"></div>',
                loader:          '<div class="dropify-loader"></div>',
                message:         '<div class="dropify-message"><p id = "edit-message" style="color: #eee; display:none;">{{ default }}</p></div>',
                preview:         '<div class="dropify-preview"><span class="dropify-render"></span><div class="dropify-infos"><div class="dropify-infos-inner"><p class="dropify-infos-message">{{ replace }}</p></div></div></div>',
                filename:        '<p class="dropify-filename"><span class="file-icon"></span> <span class="dropify-filename-inner"></span></p>',
                clearButton:     '<button type="button" class="dropify-clear">{{ remove }}</button>',
                errorLine:       '<p class="dropify-error">{{ error }}</p>',
                errorsContainer: '<div class="dropify-errors-container"><ul></ul></div>'
            }
      });

	$('#cancel_modify').click(function () {
        input.attr("disabled",true);
        select.attr("disabled",true);
        select.selectpicker('refresh');
        textarea.attr("disabled",true);
        $(".btn-text").html("修改");
    })
});
$('#product_info_modify').click(function(){
    if($('.btn-text').html() == "修改"){
        input.each(function(){
            if(this.name != "product_type"){
                $(this).removeAttr("disabled");
            }
        });
        textarea.removeAttr("disabled");
        select.removeAttr("disabled");
        select.selectpicker('refresh');
        $('.btn-text').html("保存");
    }else{
        // console.log(ele_val_arr)
        var data = handle_json_data(ele_val_arr);
        console.log(data)
        swal({
            title: "确认保存？",
            text: "是否确认保存做出的修改",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#566FC9",
            confirmButtonText: "确定",
            cancelButtonText:"取消",
            closeOnConfirm: false
        },function () {
            switch_button_status($("#product_info_modify"));
            modi_product_ajax(data);

        })
    }
});
function handle_json_data(eles) {
    var basic_info = {};
    var sub_info = {};
    var product_category_info = [];
    var product_property_info = {};
    var product_id = $.getUrlParam("product_id");
    var product_type = $("input[name='product_type']").attr("product_type");
    for(var key in eles){
        var eles_name = key;
        if(eles_name==="product_name"||eles_name==="brief"||eles_name==="stock"||eles_name==="unit"
            ||eles_name==="attribute"||eles_name==="product_type"||eles_name==="is_hot"||eles_name==="description"){
                basic_info[eles_name] = eles[key];
        }
        else if(eles_name==="product_category"){
            product_category_info.push(eles[key]);
        }
        else if(eles_name==="product_property"){
            product_property_info[key] = eles[key];
        }
        else{
            sub_info[eles_name] = eles[key];
        }
    }
    var json_dict = {
        "product_id":product_id,
        "product_type":product_type,
        "basic_info":basic_info,
        "sub_info":sub_info,
        "product_category_info":product_category_info,
        "product_property_info":product_property_info
    };
    return JSON.stringify(json_dict)
}

function change(tag){
    tag.each(function(){
        $(this).change(function(){
            var p_name = $(this).attr("name");
            var value = {}
            if(p_name=="product_property"){
                var old_value = handle_product_property_str(product_info["property_str"]);
                var new_value = handle_product_property_str($(this).val());
                value = {
                    'old_value':old_value,
                    'new_value':new_value
                }
                ele_val_arr[p_name] = value;
            }
            else if(p_name == "promote_date"){
                var date_str = $(this).val();
                var date_list = date_str.split(" ");
                var promote_start_date = date_list[0];
                var promote_end_date = date_list[2];
                var value_1 = {
                    'old_value':product_info['promote_start_date'],
                    'new_value': promote_start_date
                }
                var value_2 = {
                    'old_value':product_info['promote_end_date'],
                    'new_value':promote_end_date
                }
                ele_val_arr['promote_start_date'] = value_1;
                ele_val_arr['promote_end_date'] = value_2;
            }
            else{
                value = {
                    'old_value':product_info[p_name],
                    'new_value':$(this).val()
                };
                ele_val_arr[p_name] = value;
            }
        })
    })
}

function handle_product_property_str(property_str){
    var product_property = [];
    var property_list = property_str.split(",");
    for(var j=0;j<property_list.length;j++){
        var temp_str = property_list[j];
        var temp_list = temp_str.split("：");
        if(temp_list.length===2){
            var temp_dict = {};
            temp_dict[temp_list[0]] = temp_list[1];
            product_property.push(temp_dict);
        }
    }
    return product_property;
}

function modi_product_ajax(data){
    $.ajax({
        type: "post",
        dataType: "json",
        url: "http://127.0.0.1:8000/managermodiproduct",
        timeout:10000,
        data: data,
        success: function(Data){
           var ret = Data.ret;
           if(ret !== re_code.success){
               swal("连接失败，请稍候再试","错误代码"+ret,"error");
           }
           else{
               input.attr("disabled",true);
               select.attr("disabled",true);
               select.selectpicker('refresh');
               textarea.attr("disabled",true);
               switch_button_status($("#product_info_modify"));
               swal("修改成功","","success");
           }
        },
        error: function (Data) {
            swal("连接失败，请稍候再试","错误代码000001","error");
            $("#product_info_modify").addClass("btn-anim");
            $("#product_info_modify").removeClass("disabled");
            var children_list = $("#product_info_modify").children();
            $(children_list[0]).css("display","inline-block");
            $(children_list[1]).html("保存");
            $(children_list[2]).css("display","none");
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
        $(children_list[1]).html("保存中...");
        $(children_list[2]).css("display","inline-block");
    }
    else{
        btn_elem.addClass("btn-anim");
        btn_elem.removeClass("disabled");
        $(children_list[0]).css("display","inline-block");
        $(children_list[1]).html("修改");
        $(children_list[2]).css("display","none");
    }
}