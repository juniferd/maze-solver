import sys,os
from PIL import Image, ImageDraw
from math import sqrt


def init(maze,end,solution,show_path=True,start=(0,0)):
    #print 'a maze: ',maze
    ext = os.path.dirname(os.path.realpath(sys.argv[0]))

    tiles = {
        '-' : get_tile_01,
        '|' : get_tile_02,
        'l' : get_tile_08,
        'j' : get_tile_09,
        'r' : get_tile_10,
        '7' : get_tile_11,
        '<' : get_tile_05,
        '>' : get_tile_04,
        'v' : get_tile_06,
        '^' : get_tile_07,
        '+' : get_tile_03,
    }

    tile_size = 20

    board_size = int(sqrt(len(maze)))
    img_size = board_size * tile_size
    size = (img_size,img_size)

    img = Image.new('RGB',size,'#ffffff')
    draw = ImageDraw.Draw(img)
    
    #draw the maze tiles
    for coord in maze:
        #print coord,': ',maze[coord]
        coord_x = coord[0] * 20
        coord_y = coord[1] * 20
        this_symbol = maze[coord]

        this_tile = tiles[this_symbol](coord_x,coord_y,draw)
        #img.paste(this_tile,(coord_x,coord_y))
    
    if show_path:
        #draw the solution path
        solution_path = []
        for vertex in solution:
            coord_x = (vertex[0] * 20) + 10
            coord_y = (vertex[1] * 20) + 10
            solution_path.append((coord_x,coord_y))

        draw_solution_path(solution_path,draw)

        #draw the start and finish
        draw_goal(start,draw)
        draw_goal(end,draw,'end')

    img_path = ext + '/static/img/output.jpg'
    img.save(img_path)
    
    #img.show()
    return img

def draw_solution_path(solution_path,draw):
    draw.line(solution_path,'#544eff',2)

def draw_goal(coord,draw,goal='start'):
    x0 = (coord[0] * 20) + 5
    y0 = (coord[1] * 20) + 5

    x1 = x0 + 10
    y1 = y0 + 10
    draw.ellipse([(x0,y0),(x1,y1)],None,'#ff00ff')
    draw.text((x1+2,y0),goal,'#ff00ff')

def get_tile_01(start_x,start_y,draw):
    # draw '-'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 20
    y1 = start_y + 5

    x2 = start_x
    y2 = start_y + 15

    x3 = x1
    y3 = start_y + 20

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')

    pass

def get_tile_02(start_x,start_y,draw):
    # draw '|'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 20

    x2 = start_x + 15
    y2 = start_y

    x3 = start_x + 20
    y3 = start_y + 20

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')

    pass

def get_tile_03(start_x,start_y,draw):
    # draw '+'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 5

    x2 = start_x + 15
    y2 = start_y

    x3 = start_x + 20
    y3 = y1

    x4 = start_x
    y4 = start_y + 15

    x5 = x1
    y5 = start_y + 20

    x6 = x2
    y6 = y4

    x7 = x3
    y7 = y5

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')
    draw.rectangle([(x6,y6),(x7,y7)],'#cccccc')

    pass

def get_tile_04(start_x,start_y,draw):
    # draw '>'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 5

    x2 = x0
    y2 = start_y + 15

    x3 = x1
    y3 = start_y + 20

    x4 = start_x + 15
    y4 = y0

    x5 = start_x + 20
    y5 = y3

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_05(start_x,start_y,draw):
    # draw '<'
    
    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 20

    x2 = start_x + 15
    y2 = y0

    x3 = start_x + 20
    y3 = start_y + 5

    x4 = x2
    y4 = start_y + 15

    x5 = start_x + 20
    y5 = y1

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_06(start_x,start_y,draw):
    # draw 'v'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 5

    x2 = start_x + 15
    y2 = y0

    x3 = start_x + 20
    y3 = y1

    x4 = x0
    y4 = start_y + 15

    x5 = x3
    y5 = start_y + 20

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_07(start_x,start_y,draw):
    # draw '^'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 20
    y1 = start_y + 5

    x2 = x0
    y2 = start_y + 15

    x3 = start_x + 5
    y3 = start_y + 20

    x4 = start_x + 15
    y4 = y2

    x5 = x1
    y5 = y3

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_08(start_x,start_y,draw):
    # draw 'l'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 20

    x2 = x1
    y2 = start_y + 15

    x3 = start_x + 20
    y3 = start_y + 20

    x4 = start_x + 15
    y4 = y0

    x5 = x3
    y5 = start_y + 5

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_09(start_x,start_y,draw):
    # draw 'j'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 5

    x2 = start_x + 15
    y2 = y0

    x3 = start_x + 20
    y3 = start_y + 20

    x4 = start_x
    y4 = start_y + 15

    x5 = x2
    y5 = y3

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_10(start_x,start_y,draw):
    # draw 'r'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 5
    y1 = start_y + 20

    x2 = x1
    y2 = y0

    x3 = start_x + 20
    y3 = start_y + 5

    x4 = start_x + 15
    y4 = start_y + 15

    x5 = x3
    y5 = y1

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass

def get_tile_11(start_x,start_y,draw):
    # draw '7'

    x0 = start_x
    y0 = start_y

    x1 = start_x + 20
    y1 = start_y + 5

    x2 = start_x + 15
    y2 = y1

    x3 = x1
    y3 = start_y + 20

    x4 = x0
    y4 = start_y + 15

    x5 = start_x + 5
    y5 = y3

    draw.rectangle([(x0,y0),(x1,y1)],'#cccccc')
    draw.rectangle([(x2,y2),(x3,y3)],'#cccccc')
    draw.rectangle([(x4,y4),(x5,y5)],'#cccccc')

    pass