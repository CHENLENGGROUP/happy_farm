/**
 * Created by franksmac on 10/18/17.
 */
$(document).ready(function () {
    $("#confirm_btn").click(function () {
		var order_id = $(this).attr("data-content");
		console.log(order_id)
    })
});

function do_ajax(order_id) {

}