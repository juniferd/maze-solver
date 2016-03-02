import sys,os
from PIL import Image
from math import sqrt


def init(maze):
    #print 'a maze: ',maze
    tile_ext = 'img/maze-pieces-'

    tiles = {
        '-' : ''.join([tile_ext,'01.jpg']),
        '|' : ''.join([tile_ext,'02.jpg']),
        'l' : ''.join([tile_ext,'08.jpg']),
        'j' : ''.join([tile_ext,'09.jpg']),
        'r' : ''.join([tile_ext,'11.jpg']),
        '7' : ''.join([tile_ext,'10.jpg']),
        '<' : ''.join([tile_ext,'05.jpg']),
        '>' : ''.join([tile_ext,'04.jpg']),
        'v' : ''.join([tile_ext,'06.jpg']),
        '^' : ''.join([tile_ext,'07.jpg']),
        '+' : ''.join([tile_ext,'03.jpg']),
    }

    for tile in tiles:
        tile_img = Image.open(tiles[tile])
        tiles[tile] = tile_img

    tile_size = tile_img.size[0]

    board_size = int(sqrt(len(maze)))
    img_size = board_size * tile_size
    size = (img_size,img_size)

    img = Image.new('RGB',size)

    for coord in maze:
        #print coord,': ',maze[coord]
        coord_x = coord[0] * 20
        coord_y = coord[1] * 20
        this_symbol = maze[coord]
        this_tile = tiles[this_symbol]
        img.paste(this_tile,(coord_x,coord_y))
    img.save('img/output.jpg')
    
    img.show()