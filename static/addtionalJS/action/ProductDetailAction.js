/**
 * Created by Administrator on 2017/8/30 0030.
 */

$(document).ready(function () {

    $("#payment_log").click(function () {
        $(".modal-body").html('<div class="icon-container col-sm-6 col-md-4 col-lg-3"><i class="fa fa-spin fa-circle-o-notch"></i> 正在加载数据</div>');
        var order_id = $(this).parent().parent().attr("order_id");
        var json_data = {"order_id":parseInt(order_id)};
        JSON.stringify(json_data);
        var thead_list = ["支付账号","支付金额","支付时间"];
        var key_list = ["username","amount","payment_date"];
        ajax_get_info("/managerbrowsepaymentlog", json_data, '支付日志',thead_list, key_list);
    });

    $("#order_log").click(function () {
        $(".modal-body").html('<div class="icon-container col-sm-6 col-md-4 col-lg-3"><i class="fa fa-spin fa-circle-o-notch"></i> 正在加载数据</div>');
        var order_id = $(this).parent().parent().attr("order_id");
        var json_data = {"order_id":parseInt(order_id)};
        JSON.stringify(json_data);
        var thead_list = ["操作者","操作者类型","操作名字","操作时间"];
        var key_list = ["actor_name","actor_type", "act_name", "act_time"];
        ajax_get_info("/managerbrowseorderactlog", json_data, "操作日志", thead_list, key_list);
    })
})

function ajax_get_info(url, json_data, data_name,thead_list, key_list){
    $.ajax({
        url:url,
        type: "get",
        dataType: "json",
        timeout:10000,
        data: json_data,
        success:function (data) {
            if(data.ret!==re_code.success){
                $(".modal-body").html("<h4>连接出错,请稍后再试</h4>");
            }
            else{
                var h5_str = make_html_str(data.payment_log,data_name,thead_list,key_list);
                console.log(h5_str);
                $(".modal-body").html(h5_str);
            }
        },
        error:function () {
            $(".modal-body").html("<h4>连接出错,请稍后再试</h4>");
        }
    })
}

function make_html_str(data_list, data_name, thead_list, key_list){

    var h5_head = '';
    var h5_body = '';
    var h5_footer =                 '</tbody>' +
                                '</table>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
    h5_head = '<div class="hiddend_scroll_bar pull-right" style="background-color:white;width:17px;height:450px;position: relative; left: -17px;"></div>'
    h5_head = h5_head + '<div class="panel-wrapper collapse in">' +
                            '<div class="panel-body">' +
                                '<h4 class="text-muted">'+ data_name +'</h4>' +
                            '<div class="table-wrap mt-40">' +
                        '<div class="table-responsive" style="overflow-y:scroll; max-height: 453px;">' +
                            '<table class="table mb-0">'+
                                '<thead>' +
                                    '<tr>'
    for(var i=0;i<thead_list.length;i++){
        h5_head = h5_head+'<th>'+thead_list[i]+'</th>'
    }
    h5_head = h5_head + '</tr></thead><tbody>'

    return h5_head + h5_body + h5_footer
}