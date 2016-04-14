var TURN_SPEED = 1000

var svg = d3.select('#antfarm').insert('svg');

var pageCounter = setInterval(incrementWorld, TURN_SPEED);
var maxCounter = setInterval(refreshMaxCounter, TURN_SPEED * 30)

counter = 0;
maxCounterNum = 0;

var antColors = {}

var antNames = ['picard','riker','la forge','worf','crusher','troi','data','wesley','o\'brien','guinan','q','ro']
var antIds = { }



function setAntName(antid){
    if (!(antid in antIds)){
        var thisName = antNames[0]
        antIds[antid] = thisName
        antNames.shift()
    }
}
function setAnts(data){
    var ant = svg.selectAll('g.ant')
        .data(data)

    var antGroup = ant.enter().append('g')
    
    antGroup
        .attr('class','ant')
        .attr('fill', function(d){
            var r = parseInt(Math.random() * 255),
                g = parseInt(Math.random() * 255),
                b = parseInt(Math.random() * 255),
                rgb = 'rgb('+r+','+g+','+b+')';

            antColors[d.antid] = rgb;
            return rgb;
        })
        .attr('fill-opacity',0)
        .attr('transform',function(d){ 
            x = (d.pos[0] * 20) + 10
            y = (d.pos[1] * 20) + 10
            return 'translate('+x+','+y+')'
        })
            .append('circle')
            .attr('class','_ant')
            .attr('id', function(d){
                id = d.antid
                return id
            })
            .attr('r',3)
    
    antGroup.append('text')
        .text('test')
        .attr('class','text-food')
        .attr('font-size','12')

    ant.transition()
        .duration(TURN_SPEED)
        .ease('linear')
        .attr('transform',function(d){ 
            
            x = (d.pos[0] * 20) + 10
            y = (d.pos[1] * 20) + 10
            return 'translate('+x+','+y+')'
        })
        .attr('fill-opacity',1)
        .select('text.text-food')
            .text(function(d) {
                var star = '\u2605'
                setAntName(d.antid)
                var name = antIds[d.antid]
                if (d.has_food){
                    return name+' '+star
                } else {
                    return name
                }
                
            })


    ant.exit().remove();
}
function setMarkers(markers,visited){
    
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
                if (d.c == 'food'){
                    return 'red'
                } else if (d.c == 'exit') {
                    return '#333333'
                } else {
                    return antColors[d.antid]
                }
                
            }
        }).attr('fill-opacity',0.5)
        .on('mouseover', function(d){
            console.log(d.pos+', '+d.antid+', '+d.s+', '+d.c)
        });

    marker.exit().remove();

    var permanentMarkers = svg.selectAll('.perma-marker')
        .data(visited);
    
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
}
/*function setText(dataText, totalRooms, dataCopyAnts){
    
    var textVisited = d3.select('g.panel').selectAll('text.text-visited')
        .data(dataText);

    textVisited.enter()
        .append('text')
        .attr('class','text-visited')
        .attr('dy','240')

    textVisited
        .html(function(d){
            var percentage = parseInt(parseInt(d) / parseInt(totalRooms) * 100)
            return '<tspan>explored:</tspan>'
            +'<tspan text-anchor="end" x="140px">'+percentage+'%</tspan>'
        });
    textVisited.exit().remove();

    var antText = d3.select('g.panel').selectAll('text.side')
        .data(dataCopyAnts)
    
    antText.enter()
        .append('text')
        .attr('class','side')
        .attr('transform', function(d,i){
            num = 20 + (20 * i)
            return 'translate(0,'+ num +')'
        }).attr('font-size','12')
        .attr('fill',function(d){
            return antColors[d.antid]
        })

    antText.html(function(d){
            var antName = antIds[d.antid]
            var antMode = d.mode
            var hasFood = ''
            if (d.has_food){
                hasFood = ' \u2605'
            }
            return '<tspan>'+antName+':</tspan>'
            +'<tspan text-anchor="end" x="140px">'+antMode+hasFood+'</tspan>'
        });
    antText.exit().remove();   
}*/
function setFood(data){
    var food = svg.selectAll('.food')
        .data(data);

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

    food.transition()
        .duration(TURN_SPEED)
        .attr('fill-opacity',0)
        .attr('x', function(d){
            if (d != null){
                return (d[0] * 20) + 5
            }
        }).attr('y', function(d){
            if (d != null){
                return (d[1] * 20) + 5
            }
        }).attr('fill-opacity',0.25)

    food.exit().remove();
}
function setFoodGathered(data){
    var food = [0]
    var foodArr = []
    for (var key in data){
        var obj = {}
        count = data[key]['count']
        food[0] = food[0] + count
        obj['count'] = count
        obj['pos'] = data[key]['coord']
        foodArr.push(obj)
    }
    var foodContainer = svg.selectAll('.food-container')
        .data(foodArr)

    foodContainer.enter().append('circle')
        .attr('class','food-container')
        .attr('fill','blue')
        .attr('fill-opacity',0.25)
        .attr('transform',function(d){
            x = (d.pos[0] * 20) + 10
            y = (d.pos[1] * 20) + 10
            return 'translate('+x+','+y+')' 
        })
        .attr('r',5)

    foodContainer.transition()
        .attr('transform',function(d){
            x = (d.pos[0] * 20) + 10
            y = (d.pos[1] * 20) + 10
            return 'translate('+x+','+y+')' 
        })

    foodContainer.exit().remove();
}

function antsort(a,b) {
    return a.antid < b.antid;
}
function incrementWorld() {
    var url = '/ant/api/v1.0/actions/'+MAZEID+'/' + counter;
    var result = d3.json(url, function(error,data){
        if (error){
            console.log('error getting ant action')
        } else {
            //console.log('data: '+JSON.stringify(data))
            if (counter == 0){
                maxCounterNum = refreshMaxCounter();
            }
            
            data.ants.sort(antsort)

            var dataCopyAnts = JSON.parse(JSON.stringify(data.ants))

            setAnts(data.ants)
            var markers = []
            
            for (var key in data.markers){
                if (data.markers.hasOwnProperty(key)){
                    var ants = data.markers[key]
                    for (var key in ants){
                        markerObj = {}
                        thisPos = ants[key]['pos']
                        thisAntId = ants[key]['antid']
                        thisChemical = ants[key]['c']
                        thisStrength = ants[key]['s']

                        markerObj['pos'] = thisPos
                        markerObj['antid'] = thisAntId
                        markerObj['c'] = thisChemical
                        markerObj['s'] = thisStrength

                        markers.push(markerObj)
                    }
                }
            }
            
            setMarkers(markers, data.visited)

            var dataText = [Object.keys(data.visited).length]
            var totalRooms = document.querySelectorAll('rect.bg').length
            
            setTurnText(data.counter)

            setFoodTextGathered(data.food_gathered)
            
            setText(dataText, totalRooms, dataCopyAnts)
            
            setFood(data.food)
            
            setFoodGathered(data.food_gathered)

            counter ++;
        } 
    });
}

function refreshMaxCounter(){
    var result = d3.json('/ant/api/v1.0/'+MAZEID+'/max-counter', function(error,data){
        if (error){
            console.log('error getting max counter')
        } else {
            
            var maxArr = [data.max]

            var maxTurnText = d3.select('.panel-container > .turn-container').selectAll('span.max-turn')
                .data(maxArr)

            maxTurnText.enter()
                .append('span')
                .attr('class','max-turn float-right')

            maxTurnText.text(function(d){
                return '/ '+d
            })

            maxTurnText.exit().remove()

            maxCounterNum = maxArr[0]
        }
    });
}

