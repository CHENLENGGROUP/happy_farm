//初始化时间插件
$('.input-limit-datepicker').daterangepicker({
		locale:{
			format: 'YYYY-MM-DD'
		},
		minDate: '06/01/2015',
		buttonClasses: ['btn', 'btn-sm'],
		applyClass: 'btn-info',
		cancelClass: 'btn-default',
		dateLimit: {
			days: 6
		}
	});
//商品分类
$(document).ready(function(){
    $(".cate_select").change(function(){
        var select_ob = $(this);

        while (true){
            var c_id = select_ob.find("option:selected").attr("c_id");
            var cate_id = select_ob.attr("id");
            var str_list = cate_id.split('_');
            var next_cate_id = str_list[0]+"_"+str_list[1]+"_"+(parseInt(str_list[2])+1).toString();
            var op_list = $("#"+next_cate_id +" option");
            if (op_list.length>0){
                var count = 0;
                op_list.each(function(){
                    var p_id = $(this).attr("p_id");
                    console.log($(this));
                    if(p_id!==c_id){
                        $(this).attr("disabled","disabled");
                    }
                    else{
                        $(this).removeAttr("disabled");
                        if(count === 0){
                            $(this).attr("selected", true);
                        }
                        console.log(count);
                        count++;
                    }
                });
                $('.cate_select').selectpicker('refresh');
            }
            else{
                break;
            }
            select_ob = $("#"+next_cate_id);
        }
    });
});
//商品类型
$(document).ready(function(){
    $("#product_type_select").change(function(){
        var product_type = $(this).find("option:selected").attr("product_type");
        product_type = parseInt(product_type);
        if(product_type===1){
            $("#normal_product_add_info").css("display","none");
            $("#sub_product_add_info").css("display","block")
        }
        else{
            $("#normal_product_add_info").css("display","block");
            $("#sub_product_add_info").css("display","none")
        }
    })
})