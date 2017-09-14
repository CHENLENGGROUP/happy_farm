/**
 * Created by Administrator on 2017/9/13 0013.
 */
/**
 * Created by Administrator on 2017/8/21 0021.
 */
(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r !== null) return decodeURI(r[2]); return null;
    }
})(jQuery);

$(document).ready(function () {
    set_select_value("sort_select", "sort_rule");
    set_input_value();
    set_page_href();

    //点击搜索
    $("#search-tbn").click(function () {
        var href = get_href();
        href = href.substring(0,href.length-1);
        window.location.href=href;
    })
})

function set_select_value(op_classname, target_name){
    var op_list = $("."+op_classname).find("option");
    var target_value = $.getUrlParam(target_name);
    if(target_value!=null){
        var target_value_list = target_value.split('+');
        if (target_value_list.length===2){
            target_value = target_value_list[0] + " " + target_value_list[1];
        }
    }
    for(var i=0;i<op_list.length;i++){
        var op_value = $(op_list[i]).attr("value");
        if(op_value===target_value){
            $(op_list[i]).attr("selected", true);
            break;
        }
    }
    $('.'+op_classname).selectpicker('refresh');
}

function set_input_value(){
    var target_value = $.getUrlParam("search_item");
    if(target_value!=null){
        $("#example-input1-group21").val(target_value);
    }
}

function get_href(){

    var op_value_li = []
    $(".selectpicker").each(function () {
        var op_value = $(this).find("option:selected").attr("value");
        op_value_li.push(op_value)
    });
    var href="/managerarticlelist?";

    if(op_value_li[0]!=0){
        href = href + "sort_rule=" + op_value_li[0] + "&";
    }

    var search_item = $("#example-input1-group21").val()
    if(search_item!=""){
        href = href + "search_item="+search_item+"&";
    }
    href = encodeURI(href);
    return href
}

function set_page_href(){

    var page_number = $.getUrlParam("page_number");
    if(page_number == null){
        page_number = 1;
    }
    page_number = parseInt(page_number);

    var href = get_href();

    $(".pagination").find("li").each(function () {
        var href_1 = ""
        if($(this).hasClass("left-arrow")){
            href_1 = href + "page_number=" + (page_number-1)
        }
        else if($(this).hasClass("right-arrow")){
            href_1 = href + "page_number="+(page_number+1)
        }
        else {
            var page_number_1 = parseInt($(this).find("a").html());
            href_1 = href + "page_number=" + page_number_1;
        }
        if(!$(this).hasClass("disabled")){
            $(this).find("a").attr("href",href_1);
        }
    })

}