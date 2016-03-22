var TURN_SPEED = 1100

var svg = d3.select('#antfarm').insert('svg',':first-child');

var pageCounter = setInterval(incrementWorld, TURN_SPEED);
counter = 0;
var antColors = {}

function incrementWorld() {
    var url = '/ant/api/v1.0/actions/' + counter;
    var result = d3.json(url, function(error,data){
        if (error){
            console.log('error')
        } else {
            //console.log('data: '+JSON.stringify(data))
            console.log(JSON.stringify(data.markers))

            var ant = svg.selectAll('.ant')
                .data(data.ants)

            ant.enter()
                .append('circle')
                .attr('class','ant')
                .attr('id', function(d){
                    id = d.antid
                    return id
                })
                .attr('r',3)
                .attr('fill', function(d){
                    var r = parseInt(Math.random() * 255),
                        g = parseInt(Math.random() * 255),
                        b = parseInt(Math.random() * 255),
                        rgb = 'rgb('+r+','+g+','+b+')';

                    antColors[d.antid] = rgb;
                    return rgb;
                });
            
            ant.transition()
                .duration(TURN_SPEED)
                .ease('linear')
                .attr('cx',function(d){ return (d.pos[0] * 20) + 10})
                .attr('cy',function(d){ return (d.pos[1] * 20) + 10})
                .attr('r',3)
                /*.each('end',pulse);*/

            ant.exit().remove();
            
            function pulse() {
                ant.attr('r',4)
            }

            var markers = []
            
            for (var key in data.markers){
                if (data.markers.hasOwnProperty(key)){
                    var ants = data.markers[key]
                    for (var key in ants){
                        markerObj = {}
                        thisPos = ants[key]['pos']
                        thisAntId = ants[key]['antid']
                        thisCounter = ants[key]['counter']
                        thisChemical = ants[key]['chemical']
                        thisStrength = ants[key]['strength']

                        markerObj['pos'] = thisPos
                        markerObj['antid'] = thisAntId
                        markerObj['counter'] = thisCounter
                        markerObj['chemical'] = thisChemical
                        markerObj['strength'] = thisStrength

                        markers.push(markerObj)
                    }
                }
            }

            var marker = svg.selectAll('.marker')
                .data(markers);
            
            marker.enter()
                .append('circle')
                .attr('class','marker')
                .attr('r',2);

            marker.attr('cx',function(d){ 
                    if (d != null){
                        return (d.pos[0] * 20) + 10    
                    }
                    
                }).attr('cy',function(d){ 
                    if (d != null){
                        return (d.pos[1] * 20) + 10
                    }
                }).attr('fill',function(d){
                    if (d != null){
                        if (d.chemical == 'food'){
                            return 'red'
                        } else if (d.chemical == 'exit') {
                            return '#333333'
                        } else {
                            return antColors[d.antid]
                        }
                        
                    }
                }).attr('fill-opacity',0.5);

            marker.exit().remove();

            var permanentMarkers = svg.selectAll('.perma-marker')
                .data(data.visited);
            
            permanentMarkers.enter()
                .append('circle')
                .attr('class','perma-marker')
                .attr('r',1)
                .attr('fill','#333333');

            permanentMarkers.attr('cx',function(d){
                    if (d != null){

                        return (d[0] * 20) + 10
                    }
                }).attr('cy',function(d){
                    if (d != null){
                        return (d[1] * 20) + 10
                    }
                });

            var dataText = [Object.keys(data.visited).length]
            var totalRooms = Object.keys(data.maze).length

            var textVisited = svg.selectAll('text')
                .data(dataText);

            textVisited.enter()
                .append('text')
                .attr('x',820)
                .attr('y',20)

            textVisited.text(function(d){
                var percentage = parseInt(parseInt(d) / parseInt(totalRooms) * 100)
                return 'explored: '+percentage+'%'
            });

            textVisited.exit().remove();

            var antText = svg.selectAll('g.ant-container')
                .data(data.ants)

            antText.enter()
                .append('g')
                .attr('class','ant-container')
                .attr('transform', function(d,i){
                    num = 40 + (20 * i)
                    return 'translate(820,'+ num +')'
                }).attr('font-size','12');
            antText.append('text')
                .text(function(d){
                    var antName = d.antid
                    var antMode = d.mode
                    var hasFood = ''
                    if (d.has_food){
                        hasFood = ' (has food)'
                    }
                    return antName+': '+antMode+hasFood
                }).attr('fill',function(d){
                    return antColors[d.antid]
                });

            var food = svg.selectAll('.food')
                .data(data.food);

            food.enter()
                .append('rect')
                .attr('class','food')
                .attr('x', function(d){
                    if (d != null){
                        return (d[0] * 20) + 5
                    }
                }).attr('y', function(d){
                    if (d != null){
                        return (d[1] * 20) + 5
                    }
                }).attr('width',10)
                .attr('height',10)
                .attr('fill','red')
                .attr('fill-opacity',0.25)
            counter ++;
        } 
    });
}


