var ele_val_arr = new Array();
var input = $('input');
var select = $('select');
var textarea = $('textarea');

$(document).ready(function () {
    change(input);
    change(select);
    change(textarea);
    /* Basic Init*/
	$('.dropify').dropify({
        messages:{
          'default': '编辑商品图片',
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
        var data = handle_json_data(ele_val_arr);
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
               swal("修改成功","","success");
           },
           error: function (Data) {
                swal("连接失败，请稍候再试","错误代码000001","error");
           }
        });
        input.attr("disabled",true);
        select.attr("disabled",true);
        select.selectpicker('refresh');
        textarea.attr("disabled",true);
        $('.btn-text').html("修改");
    }
});
function handle_json_data(eles) {
    var basic_info = {};
    var sub_info = {};
    var product_category_info = [];
    var product_property_info = [];

    for(var i=0;i<eles.length;i++){
        var eles_name = eles[i][0];
        if(eles_name==="product_name"||eles_name==="brief"||eles_name==="stock"||eles_name==="unit"
            ||eles_name==="attribute"||eles_name==="product_type"||eles_name==="is_hot"||eles_name==="description"){
                basic_info[eles_name] = eles[i][1];
        }
        else if(eles_name==="product_category"){
            product_category_info.push(eles[i][1]);
        }
        else if(eles_name==="product_property"){
            var property_str = eles[i][1];
            var property_list = property_str.split(",");
            for(var j=0;j<property_list.length;j++){
                var temp_str = property_list[j];
                var temp_list = temp_str.split("：");
                if(temp_list.length===2){
                    var temp_dict = {};
                    temp_dict[temp_list[0]] = temp_list[1];
                    product_property_info.push(temp_dict);
                }
            }
        }
        else if(eles_name==="promote_date"){
            var date_str = eles[i][1];
            var date_list = date_str.split(" ");
            sub_info["promote_start_date"] = date_list[0];
            sub_info["promote_end_date"] = date_list[2];
        }
        else{
            sub_info[eles_name] = eles[i][1];
        }
    }
    var json_dict = {
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
            for(var i=0;i<ele_val_arr.length;i++){
                var arr = new Array();
                var str = ele_val_arr[i].toString();
                var arr = str.split(",");
                if(arr[0] == $(this).attr("name")){
                    ele_val_arr.splice(i,1);
                }
            }
            ele_val_arr.push([$(this).attr("name"), $(this).val()]);
        })
    })
}