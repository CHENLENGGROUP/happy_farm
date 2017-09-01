/**
 * Created by Administrator on 2017/8/14 0014.
 */
var re_code = {
    'connect_error':'000001',
    'session_error':'000002',
    'passwd_incorrect':'000003',
    'username_exist':'000004',
    'telephon_exist':'000005',
    'verify_error':'000006',
    'parameter_error':'000007',
    'limit_exceeded':'000008',
    'success':'000000'
};

$(document).ready(function () {
   $("#product_info_sub").click(function () {
       if($(this).hasClass("disabled")){
           return;
       }
       switch_button_status(this);
       var ele_result = getElementsValue("product_info_from");
       var eles = ele_result[0];
       var notnull_eles = ele_result[1];
       eles = handle_input(eles);
       var is_ligal = is_input_empty(eles, notnull_eles);
       if(!is_ligal){
           sweet_alert("请完善必填信息","未满足要求的信息已用红框表示");
           switch_button_status(this);
           return false;
       }
       var json_data = handle_json_data(eles);
       ajax_request(json_data, this);
   })
});

function getElementsValue(formId) {
    var eles_value_arr = new Array();
    var eles_notNull_arr = new Array();
    var form = $("#"+formId);
    var element_in = form.find("input");
    var element_se = form.find("select");
    var element_te = form.find("textarea");

    for(var i_1=0;i_1<element_in.length;i_1++){
        var result = get_value(element_in[i_1]);
        if($(element_in[i_1]).attr("required")==="required"){
            eles_notNull_arr.push($(element_in[i_1]));
        }
        if(result.length !== 0){
            eles_value_arr.push(result);
        }
    }
    for(var i_2=0;i_2<element_se.length;i_2++){
        var result_1 = get_select_value(element_se[i_2]);
        if(result_1.length !== 0){
            eles_value_arr.push(result_1);
        }
    }
    for(var i_3=0;i_3<element_te.length;i_3++){
        var result_2 = get_value(element_te[i_3]);
        if(result_2.length !== 0){
            eles_value_arr.push(result_2);
        }
    }
    return [eles_value_arr,eles_notNull_arr];
}

function get_value(input_elem){
    var ele = $(input_elem);
    var ele_name = ele.attr("name");
    if(typeof(ele_name)==="undefined"){
        return [];
    }
    return [ele.attr("name"), ele.val()];
}

function get_select_value(select_elem){
    var ele = $(select_elem);
    var value_id = parseInt(ele.find("option:selected").attr("db_id"));
    return [ele.attr("name"), value_id]
}

function is_input_empty(eles, notnull_eles){
    var is_ligal = true;
    for(var i=0;i<eles.length;i++){
        for(var j=0;j<notnull_eles.length;j++){
            var notnull_name = notnull_eles[j].attr("name");
            if(eles[i][0]===notnull_name&&eles[i][1]===""){
                var parent_node = $(notnull_eles[j].context.parentElement);
                parent_node.addClass("has-error");
                parent_node.addClass("has-danger")
                is_ligal = false
            }
        }
    }
    return is_ligal
}

function handle_input(eles){
    for(var i=0;i<eles.length;i++){
        if(eles[i][0]==="product_type"){
            var product_type = eles[i][1];
        }
    }
    var result_fin = new Array();
    if(parseInt(product_type)===1){
        for(var i1=0;i1<eles.length;i1++){
            var ele_name = eles[i1][0];
            if(ele_name!=="market_price"&&ele_name!=="shop_price"
                &&ele_name!=="promote_price"&&ele_name!=="promote_date"){
                result_fin.push(eles[i1]);
            }
        }
    }
    else{
        for(var i1=0;i1<eles.length;i1++){
            var ele_name = eles[i1][0];
            if(ele_name!=="first_pay"&&ele_name!=="each_month_pay"
                &&ele_name!=="need_to_pay_month"){
                result_fin.push(eles[i1]);
            }
        }
    }
    return result_fin;
}

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

function sweet_alert(title, text){
    swal({
        title: title,
        text:text,
        type:"error",
        confirmButtonColor: "#566FC9",
        confirmButtonText:"确定",
        closeOnConfirm:true
    });
}

function sweet_alert_success(title, text, modi_url){
    swal({
        title: title,
        text: text,
        type: "success",
        showCancelButton: true,
        confirmButtonColor: "#566FC9",
        confirmButtonText: "确定",
        cancelButtonText:"取消",
        closeOnConfirm: false
    },function () {
        window.location.href=modi_url;
    })
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

function ajax_request(json_data, btn_obj){
    $.ajax({
       type: "post",
       dataType: "json",
       url: "http://127.0.0.1:8000/manageraddproduct",
       timeout:10000,
       data: json_data,
       success: function(Data){
           var ret = Data.ret;
           if(ret !== re_code.success){
               sweet_alert("连接失败，请稍候再试","错误代码"+ret);
           }
           var modi_url = "/managermodiproduct?product_id="+Data.product_id
           sweet_alert_success("添加成功","是否立即去给商品添加图片",modi_url);
           switch_button_status(btn_obj);
       },
       error: function (Data) {
            sweet_alert("连接失败，请稍候再试","错误代码000001");
            switch_button_status(btn_obj);
       }
   });
}