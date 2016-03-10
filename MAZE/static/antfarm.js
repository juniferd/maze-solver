
var svg = d3.select('#antfarm').insert('svg',':first-child');

var pageCounter = setInterval(getAntBehavior, 1100);
counter = 0;

function getAntBehavior() {
    var url = '/ant/api/v1.0/actions/' + counter;
    var result = d3.json(url, function(error,data){
        if (error){
            console.log('error')
        } else {

            var ant = svg.selectAll('.ant')
                .data(data)

            ant.enter()
                .append('circle')
                .attr('class','ant')
                .attr('r',3)
                .attr('fill', function(){
                    var r = parseInt(Math.random() * 255),
                        g = parseInt(Math.random() * 255),
                        b = parseInt(Math.random() * 255);
                    return 'rgb('+r+','+g+','+b+')'
                })

            ant.transition()
                .duration(1100)
                .ease('linear')
                .attr('cx',function(d){ return (d.pos[0] * 20) + 10})
                .attr('cy',function(d){ return (d.pos[1] * 20) + 10});

            ant.exit().remove();
            
            var marker = svg.selectAll('.nomarker')
                .data(data);

            marker.enter()
                .append('circle')
                .attr('class','marker')
                .attr('r',1)
                .attr('fill','#666666');
            
            marker.attr('cx',function(d){ 
                    console.log('marker position: '+d.marker.pos)
                    if (d.marker.pos != null){
                        return (d.marker.pos[0] * 20) + 10    
                    }
                    
                }).attr('cy',function(d){ 
                    if (d.marker.pos != null){
                        return (d.marker.pos[1] * 20) + 10
                    }
                });

            counter ++;
        } 
    });
}


