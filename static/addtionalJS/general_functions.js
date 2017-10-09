/**
 * Created by Administrator on 2017/9/29 0029.
 */
function eval_str(input_str){
    var re = new RegExp("&#39;","g");
    var re_u = new RegExp("u'","g");
    input_str = input_str.replace(re,"'");
    input_str = input_str.replace(re_u, "'")
    var input = eval(input_str)
    return input
}

function draw_pie_chart(lable, data, ele_id){
    var ctx6 = document.getElementById(ele_id).getContext("2d");
    var data6 = {
        labels: lable,
        datasets: [
            {
                data: data,
                backgroundColor: [
                    "rgba(234,101,162,.8)",
                    "rgba(241,91,38,.8)",
                    "rgba(252,176,59,.8)",
                    "rgba(50,205,50,.8)",
                    "rgba(86, 111, 201,.8)",
                    "rgba(255,228,225,.8)",
                    "rgba(127,216,207,.8)",
                ],
                hoverBackgroundColor: [
                    "rgba(234,101,162,.8)",
                    "rgba(241,91,38,.8)",
                    "rgba(252,176,59,.8)",
                    "rgba(50,205,50,.8)",
                    "rgba(86, 111, 201,.8)",
                    "rgba(255,228,225,.8)",
                    "rgba(127,216,207,.8)",
                ],
            }
        ]
    };

    var pieChart  = new Chart(ctx6,{
        type: 'pie',
        data: data6,
        options: {
            animation: {
                duration:	3000
            },
            responsive: true,
            maintainAspectRatio:false,
            legend: {
                labels: {
                fontFamily: "Varela Round",
                fontColor:"#2f2c2c"
                }
            },
            tooltips: {
                backgroundColor:'rgba(47,44,44,.9)',
                cornerRadius:0,
                footerFontFamily:"'Varela Round'"
            }
        }
    });
}

function draw_linechart(element, data, xkey, ykeys, lable){
    var chart = Morris.Area({
        element: element,
        data: data,
        xkey: xkey,
        ykeys: ykeys,
        labels: lable,
        pointSize: 2,
        fillOpacity: 0,
        lineWidth:2,
        pointStrokeColors:['#fcb03b', '#ea65a2', '#566FC9'],
        behaveLikeLine: true,
        gridLineColor: '#eee',
        hideHover: 'auto',
        lineColors: ['#fcb03b', '#ea65a2', '#566FC9'],
        resize: true,
        gridTextColor:'#2f2c2c',
        gridTextFamily:"Varela Round"
    })
    return chart;
}

function draw_barchart(element, data, xkey, ykeys, lable){
    var chart = Morris.Bar({
        element: element,
        data: data,
        xkey: xkey,
        ykeys: ykeys,
        labels: lable,
        barColors:['#fcb03b', '#ea65a2', '#566FC9'],
        hideHover: 'auto',
        gridLineColor: '#eee',
        resize: true,
        gridTextColor:'#2f2c2c',
        gridTextFamily:"Varela Round"
    });
    return chart;
}
// [
//                 "rgba(234,101,162,.8)",
//                 "rgba(241,91,38,.8)",
//                 "rgba(252,176,59,.8)"
//             ]