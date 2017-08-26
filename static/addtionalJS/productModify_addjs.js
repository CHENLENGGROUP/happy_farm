/**
 * Created by Administrator on 2017/8/26 0026.
 */
$(document).ready(function () {
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

    $("#product_info_sub").click(function () {
		$("#product_info_from").find("input").each(function () {
			console.log($(this).val())
        })
    })
})