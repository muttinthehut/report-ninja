// charting.js
// jpb, 2014-02-07
//  this script provides the info for chart in the base template client.html
//





        // RECALL THIS:
        // 1. Code here runs first, before the download starts.

        //     d3.tsv("data.tsv", function(error, data) {
        // 3. Code here runs last, after the download finishes.
        //       });

        // 2. Code here runs second, while the file is downloading.
        
        // START OF BAR CHART CODE - UPPER LEFT
        
        var valueLabelWidth = 40;   // space reserved for value labels (right)
        var barHeight = 20;         // height of one bar
        var barLabelWidth = 100;    // space reserved for bar labels
        var barLabelPadding = 5;    // padding between bar and bar labels (left)
        var gridLabelHeight = 18;   // space reserved for gridline labels
        var gridChartOffset = 3;    // space between start of grid and first bar
        var maxBarWidth = 420;      // width of the bar with the max value
        
        // accessor functions to return data
        var barLabel = function(d) { return d['makemodel']; };
        var barValue = function(d) { return parseFloat(d['shops']); };
        
        
        
        
     
        // function to return data...see note above
        d3.csv("/static/data/crossshop.csv",function(d) {
            
            console.log('Finished data load');
            return {
                clientid: d.ClientID,
                model: d.Model,
                makemodel: d.MakeModel,
                shops: +d.Shops
            };
        }, function(error,data) {
            
            // NOTE THE DATA IS FULLY LOADED HERE.  NOT ABOVE.
            // 
            
            console.log('Loading data');
            console.log(data);
            console.log(data.length);
        
          
            
        
            // scales here
        
            var yScale = d3.scale.ordinal().domain(d3.range(0,data.length)).rangeBands([0,data.length * barHeight]);
            var y = function(d,i) { return yScale(i); };
            
            var yText = function(d,i) { return y(d,i) + yScale.rangeBand() / 2; };
            var x = d3.scale.linear().domain([0, d3.max(data,barValue)]).range([0,maxBarWidth]);
            
            // svg container element
        
            var chart = d3.select('#chartrow1').append("svg")
                .attr('width', maxBarWidth + barLabelWidth + valueLabelWidth)
                .attr('height', gridLabelHeight + gridChartOffset + data.length * barHeight);
            
            // grid line labels
            var gridContainer = chart.append('g')
                .attr('transform','translate(' + barLabelWidth + ',' + gridLabelHeight + ')');
            gridContainer.selectAll("text").data(x.ticks(10)).enter().append("text")
                .attr("x",x)
                .attr("dy",-3)
                .attr("text-anchor","middle")
                .text(String);
            
            // vertical grid lines
            
            gridContainer.selectAll("line").data(x.ticks(10)).enter().append("line")
                .attr("x1", x)
                .attr("x2", x)
                .attr("y1", 0)
                .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
                .style("stroke", "#ccc");

            // bar labels
            var labelsContainer = chart.append('g')
                .attr('transform', 'translate(' + (barLabelWidth - barLabelPadding) + ',' + (gridLabelHeight + gridChartOffset) + ')'); 
            labelsContainer.selectAll('text').data(data).enter().append('text')
                .attr('y', yText)
                .attr('stroke', 'none')
                .attr('fill', 'black')
                .attr("dy", ".35em") // vertical-align: middle
                .attr('text-anchor', 'end')
                .text(barLabel);

            // bars
            var barsContainer = chart.append('g')
                .attr('transform', 'translate(' + barLabelWidth + ',' + (gridLabelHeight + gridChartOffset) + ')'); 
            barsContainer.selectAll("rect").data(data).enter().append("rect")
                .attr('y', y)
                .attr('height', yScale.rangeBand())
                .attr('width', function(d) { return x(barValue(d)); })
                .attr('stroke', 'white')
                .attr('fill', 'steelblue');
            
            // bar value labels
            barsContainer.selectAll("text").data(data).enter().append("text")
                .attr("x", function(d) { return x(barValue(d)); })
                .attr("y", yText)
                .attr("dx", 3) // padding-left
                .attr("dy", ".35em") // vertical-align: middle
                .attr("text-anchor", "start") // text-align: right
                .attr("fill", "black")
                .attr("stroke", "none")
                .text(function(d) { return d3.round(barValue(d), 2); });

            // start line
            barsContainer.append("line")
                .attr("y1", -gridChartOffset)
                .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
                .style("stroke", "#000");

        }   // END OF CALLBACK FUNCTION
        
        
        );
        
        
        
        
        // END OF BAR CHART CODE - UPPER LEFT
        
// START OF BAR CHART CODE LOWER





// END OF BAR CHART CODE LOWER


        // start of row 1 script

        var margin = {top: 20, right: 40, bottom: 20, left: 40},
        width = 550- margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

        // parse the date and time
        var parseDate = d3.time.format("%d-%b-%y").parse;

        // set the ranges
        var x = d3.time.scale().range([0, width]);
        var y = d3.scale.linear().range([height, 0]);


        // define the axes
        var xAxis = d3.svg.axis().scale(x)
            .orient("bottom").ticks(5);

        var yAxis = d3.svg.axis().scale(y)
            .orient("left").ticks(5);

        // define the line
        var valueline = d3.svg.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.close); });

// Adds the chart in the upper left on row 1
    
        var chart1 = d3.select("#chartrow1")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Get the data
        d3.tsv("/static/data/data.tsv", function(error, data) {
            data.forEach(function(d) {
            d.date = parseDate(d.date);
            d.close = +d.close;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.close; })]);

        chart1.append("path")      // Add the valueline path.
            .attr("d", valueline(data));

        chart1.append("g")         // Add the X Axis
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        chart1.append("g")         // Add the Y Axis
            .attr("class", "y axis")
            .call(yAxis);
});




// Adds the svg canvas
var	chart2 = d3.select("#chartrow2")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
// Get the data
d3.tsv("/static/data/data.tsv", function(error, data) {
	data.forEach(function(d) {
		d.date = parseDate(d.date);
		d.close = +d.close;
	});

	// Scale the range of the data
	x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain([0, d3.max(data, function(d) { return d.close; })]);

	// Add the valueline path.
	chart2.append("path")
		.attr("class", "line")
		.attr("d", valueline(data));

	// Add the X Axis
	chart2.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	// Add the Y Axis
	chart2.append("g")
		.attr("class", "y axis")
		.call(yAxis);

});