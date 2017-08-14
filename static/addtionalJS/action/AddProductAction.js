/**
 * Created by Administrator on 2017/8/14 0014.
 */
$(document).ready(function () {
   $("#product_info_sub").click(function () {
       var eles = getElementsValue("product_info_from");
       console.log(eles);
   })
});

function getElementsValue(formId) {
    var eles_value_arr = new Array();
    var form = $("#"+formId);
    var element_in = form.find("input");
    var element_se = form.find("select");
    var element_te = form.find("textarea");

    for(var i_1=0;i_1<element_in.length;i_1++){
        eles_value_arr.push(get_value(element_in[i_1]));
    }
    for(var i_2=0;i_2<element_se.length;i_2++){
        eles_value_arr.push(get_value(element_se[i_2]));
    }
    for(var i_3=0;i_3<element_te.length;i_3++){
        eles_value_arr.push(get_value(element_te[i_3]));
    }

    return eles_value_arr;
}

function get_value(input_elem){
    var ele = $(input_elem);
    return [ele.attr("name"), ele.val()];
}
