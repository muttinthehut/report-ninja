// dmmcharts.js
// jpb, 2014-02-10
// rework to load single D3.js momentum chart on the page
//  used to generate static image for download

 console.log("dmmcharts.js loaded");

//  DMM DATA HERE

    // grab the dmm data
    var d3dmmdata = JSON.parse(dmmdata);
    // jpb, debug only below
     console.log(d3dmmdata);
   

//
// START OF DMM CHART - UPPER RIGHT

  
        var margin = {top: 20, right: 40, bottom: 40, left: 40},
        // width = 550- margin.left - margin.right,
        width = 202 - margin.left - margin.right,
        // height = 250 - margin.top - margin.bottom;
        height = 140 - margin.top - margin.bottom;
      
        var parseDate = d3.time.format("%Y-%m-%d").parse;
        // var formatDate = d3.time.format("%b").parse;
        
        // for color
        var color = d3.scale.category10();

        // set the ranges
        var x = d3.time.scale().range([0, width]);
        var y = d3.scale.linear().range([height, 0]);
        
                // define the axes
        var xAxis = d3.svg.axis().scale(x)
            .orient("bottom")
            .tickFormat(d3.time.format("%b"));

        var yAxis = d3.svg.axis().scale(y)
            .orient("left");

        // define the line
        var line = d3.svg.line()
           // .interpolate("basis")
            .x(function(d) { 
                    // jpb, debug below
                    // console.log(d.date); 
                    return x(d.date); })
            .y(function(d) { 
                    // jpb, debug below
                    // console.log(d.dmm); 
                    return y(d.dmm); });

// Adds the chart in the upper left on row 1
    
        var chart1 = d3.select("#dmmchart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        // add color
        color.domain(d3.keys(d3dmmdata[0].fields).filter (
               function(key) { return key == "clientmodel"; }
               ));
        
        // coerce data into the right formats
        
        d3dmmdata = d3dmmdata.map( function(d) {
            return {
                clientmodel: d.fields.clientmodel,
                date: parseDate(d.fields.yearmonth),
                dmm : +d.fields.dmm };
        });
        
        // nest the data on clientmodel since we want to draw one line per model
        
        d3dmmdata = d3.nest().key(function(d) {console.log(d.clientmodel); return d.clientmodel; }).entries(d3dmmdata);
        


      x.domain([d3.min(d3dmmdata,function(d) { return d3.min(d.values, function (d) { return d.date;});  }),
                d3.max(d3dmmdata,function(d) {return d3.max(d.values, function (d) {return d.date;}); })]);
                
        // y.domain([0,d3.max(d3dmmdata, function(d) { return d3.max(d.values, function (d) {return d.dmm; }); })]);
        y.domain([0,100]);
         
            

        chart1.append("g")         // Add the X Axis
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
                .selectAll("text")
                .style("text-anchor","end")
                .style("font-family","sans-serif")
                .style("font-size","10px")
                .style('fill','white')
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) { return "rotate(-75)"});
 

        chart1.append("g")         // Add the Y Axis
            .attr("class", "y axis")
            .style("font-family","sans-serif")
            .style("font-size","10px")
            .style("fill","white")
            .call(yAxis);
        
         
        var clientmodels = chart1.selectAll(".clientmodel").data(d3dmmdata,function(d) { return d.key })
                .enter().append("g")
                .attr("class", "clientmodel");
        
        clientmodels.append("path")
            .attr("class","line")
            .attr("fill","none")
            .attr("stroke","#ccc")
            .attr("d", function(d) {
                // jpb, debug only below
                // console.log(d); 
                return line(d.values); })
            .style("stroke", function(d) {return color(d.key); })
            .style("stroke-width",'5px');
            

    // jpb, added the legend
    var legend = clientmodels.selectAll('g')
        .data(d3dmmdata)
        .enter()
        .append('g')
            .attr('class','legend');
            
            console.log('at legend');
            
        legend.append('rect')
            .attr('x',width-20)
            .attr('y',function(d,i){return i * 20;})
            .attr('width',10)
            .attr('height',10)
            .style('fill', function(d) { console.log(d.key); return color(d.key);
            });
            
        legend.append('text')
            .attr('x',width-8)
            .attr('y',function(d,i){return(i*20) + 9;})
            .style("font-family","sans-serif")
            .style("font-size","10px")
            .style('fill','white')

            .text(function(d){ return d.key; });
   

console.log("end of dmmcharts.js");
