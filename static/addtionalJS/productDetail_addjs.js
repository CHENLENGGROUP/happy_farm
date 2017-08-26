/**
 * Created by Administrator on 2017/8/24 0024.
 */
//监听div大小变化
(function($, h, c) {
	var a = $([]),
	e = $.resize = $.extend($.resize, {}),
	i,
	k = "setTimeout",
	j = "resize",
	d = j + "-special-event",
	b = "delay",
	f = "throttleWindow";
	e[b] = 250;
	e[f] = true;
	$.event.special[j] = {
		setup: function() {
			if (!e[f] && this[k]) {
				return false;
			}
			var l = $(this);
			a = a.add(l);
			$.data(this, d, {
				w: l.width(),
				h: l.height()
			});
			if (a.length === 1) {
				g();
			}
		},
		teardown: function() {
			if (!e[f] && this[k]) {
				return false;
			}
			var l = $(this);
			a = a.not(l);
			l.removeData(d);
			if (!a.length) {
				clearTimeout(i);
			}
		},
		add: function(l) {
			if (!e[f] && this[k]) {
				return false;
			}
			var n;
			function m(s, o, p) {
				var q = $(this),
				r = $.data(this, d);
				r.w = o !== c ? o: q.width();
				r.h = p !== c ? p: q.height();
				n.apply(this, arguments);
			}
			if ($.isFunction(l)) {
				n = l;
				return m;
			} else {
				n = l.handler;
				l.handler = m;
			}
		}
	};
	function g() {
		i = h[k](function() {
			a.each(function() {
				var n = $(this),
				m = n.width(),
				l = n.height(),
				o = $.data(this, d);
				if (m !== o.w || l !== o.h) {
					n.trigger(j, [o.w = m, o.h = l]);
				}
			});
			g();
		},
		e[b]);
	}
})(jQuery, this);

$(document).ready(function () {
    resize_data_box();
	resize_bar_chart();

    $("#bar-chart2").resize(function (){
        resize_data_box()
    })

	$("#bar-chart2").resize(function (){
        resize_bar_chart()
    })

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

function resize_data_box(){
    var height = $("#bar-chart2").height();

    var cal_height = (height)/2;
    $(".sm-data-box .col-xs-5").height(cal_height);
}

function resize_bar_chart(){

	var height = $("#sale_line_chart").height();
	var width = $("#sale_line_chart").width();
	console.log(height);
	console.log(width);
	var cal_height = height-30-10-30;
	$("#chart_2").height(cal_height);
}