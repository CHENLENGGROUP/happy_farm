if($('#morris_extra_bar_chart').length > 0)
		// Morris bar chart
		Morris.Bar({
			element: 'morris_extra_bar_chart',
			data: [{
				y: '2006',
				a: 100,
				b: 90,
				c: 60
			}, {
				y: '2007',
				a: 75,
				b: 65,
				c: 40
			}, {
				y: '2008',
				a: 50,
				b: 40,
				c: 30
			}, {
				y: '2009',
				a: 75,
				b: 65,
				c: 40
			}, {
				y: '2010',
				a: 50,
				b: 40,
				c: 30
			}, {
				y: '2011',
				a: 75,
				b: 65,
				c: 40
			}, {
				y: '2012',
				a: 100,
				b: 90,
				c: 40
			},{
				y: '2013',
				a: 100,
				b: 90,
				c: 40
			}],
			xkey: 'y',
			ykeys: ['a', 'b'],
			labels: ['A', 'B'],
			barColors:['#fcb03b', '#ea65a2','black'],
			hideHover: 'auto',
			gridLineColor: '#eee',
			resize: true,
			gridTextColor:'#2f2c2c',
			gridTextFamily:"Varela Round"
		});
if($('#morris_bar_chart').length > 0)
    // Morris bar chart
    Morris.Bar({
        element: 'morris_bar_chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90,
            c: 60
        }, {
            y: '2007',
            a: 75,
            b: 65,
            c: 40
        }, {
            y: '2008',
            a: 50,
            b: 40,
            c: 30
        }, {
            y: '2009',
            a: 75,
            b: 65,
            c: 40
        }, {
            y: '2010',
            a: 50,
            b: 40,
            c: 30
        }, {
            y: '2011',
            a: 75,
            b: 65,
            c: 40
        }, {
            y: '2012',
            a: 100,
            b: 90,
            c: 40
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['A', 'B'],
        barColors:['#fcb03b', '#ea65a2'],
        hideHover: 'auto',
        gridLineColor: '#eee',
        resize: true,
        gridTextColor:'#2f2c2c',
        gridTextFamily:"Varela Round"
    });