var Maze = {
    'init' : function(){
        var result = d3.json('/ant/api/v1.0/'+MAZEID+'/get-maze', function(error,data){
            if (error) {
                console.log('error getting maze')
            } else {
                d = data.maze
                n = d.length;
                for (i = 0; i < n; i++){
                    Maze.drawTile(d[i])    
                }
            }
        })
        
    },
    'test' : function(d){
        console.log(d)
    },
    'drawTile' : function(tile){
        svg.append('rect')
            .attr('x',tile.x)
            .attr('y',tile.y)
            .attr('width',tile.width)
            .attr('height',tile.height)
            .attr('fill',tile.fill)
            .attr('class',function(){
                if (tile.class){
                    return tile.class
                } else {
                    return 'path'
                }
            })
        
    
    }
}

Maze.init()