
var svg = d3.select('#antfarm').insert('svg',':first-child');

/*svg.attr('height',800)
    .attr('width',800)
    .append('defs')
    .append('pattern')
    .attr('height',800)
    .attr('width',800)
    .attr('id','bgmaze')
    .attr('patternUnits','userSpaceOnUse')
    .append('image')
    .attr('xlink:href','/static/img/output.jpg')
    .attr('x',0)
    .attr('y',0)
    .attr('width',800)
    .attr('height',800);

svg.append('svg:rect')
    .attr('x',0)
    .attr('y',0)
    .attr('width',800)
    .attr('height',800)
    .attr('fill','url(#bgmaze)');*/



var pageCounter = setInterval(getAntBehavior, 1500);
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
                    .attr('r',2)
                    .attr('fill','red')

                ant.transition()
                    .attr('cx',function(d){ return (d.pos[0] * 20) + 10})
                    .attr('cy',function(d){ return (d.pos[1] * 20) + 10});

                ant.exit().remove();
            
            counter ++;
        } 
    });
}


