var panel = d3.select('#stats-panel > .panel-container');

function setText(dataText, totalRooms, dataCopyAnts){
    var textVisited = panel.selectAll('p.text-visited')
        .data(dataText);

    textVisited.enter()
        .append('p')
        .attr('class','text-visited clearfix')

    textVisited.html(function(d){
        var percentage = parseInt(parseInt(d) / parseInt(totalRooms) * 100)
        return '<span>explored:</span>'
        +'<span class = "align-right">'+percentage+'%</span>'
    });
    textVisited.exit().remove();
    
    var antText = panel.selectAll('p.side')
        .data(dataCopyAnts)
    
    antText.enter()
        .append('p')
        .attr('class','side clearfix')
        .attr('style',function(d){
            return 'color:'+antColors[d.antid]+';'
        })

    antText.html(function(d){
            var antName = antIds[d.antid]
            var antMode = d.mode
            var hasFood = ''
            if (d.has_food){
                hasFood = ' \u2605'
            }
            return '<span>'+antName+':</span>'
            +'<span class="align-right">'+antMode+hasFood+'</span>'
        });
    antText.exit().remove(); 

}

function setFoodTextGathered(data){
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
    var foodText = panel.selectAll('p.food-gathered')
        .data(food)

    foodText.enter()
        .append('p')
        .attr('class','food-gathered clearfix')

    foodText.html(function(d){
        return '<span>food gathered:</span>'
        +'<span class="align-right">'+d+'</span>'
    });
    
    foodText.exit().remove();

}

function setTurnText(data){
    var turn = [data]

    var turnText = d3.select('.panel-container > .turn-container').selectAll('span.turn')
        .data(turn)

    turnText.enter()
        .append('span')
        .attr('class','turn float-left')
        
    
    turnText.html(function(d){
        return 'turn: &nbsp;'+d
    });

    turnText.exit().remove()
}

