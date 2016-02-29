## solve a given maze

# represent a maze as a series of connections
SYMBOL_MAP = {
    '-' : ['right', 'left'],
    '|' : ['up', 'down'],
    'l' : ['up','right'],
    'j' : ['up','left'],
    'r' : ['right','down'],
    '7' : ['down', 'left'],
    '<' : ['up', 'right', 'down'],
    '>' : ['up', 'down', 'left'],
    'v' : ['up', 'right', 'left'],
    '^' : ['right', 'down', 'left'],
    '+' : ['up','right','down','left']
}
# here is a maze represented as symbols
# it starts at the upper left and exits in the lower right
MAZE = [
    ['<','+','-','>'],
    ['|','l','r','7'],
    ['l','+','>','v'],
    ['<','v','v','7']
]
MAZE_MAP = {}

## FIX THIS LATER
for j,row in enumerate(MAZE):
    for i,symbol in enumerate(row):
        MAZE_MAP[(i,j)] = SYMBOL_MAP[symbol]


MAZE_CONN = {}



def get_all_neighbors(maze_map):
## this is faster
    connections = {}
    for tile in maze_map:
        next_coords = get_neighbors(tile)
        connections[tile] = next_coords
    return connections

def get_neighbors(coord):
    connections = MAZE_MAP[coord]
    next_coords = []

    for connection in connections:
        next_coord = get_next_coord(coord,connection)
        if next_coord is not None:
            next_coords.append(next_coord)

    return next_coords

def get_next_coord(coord,direction):
    start_x = coord[0]
    start_y = coord[1]
    if direction == 'up':
        next_x = start_x
        next_y = start_y - 1
    elif direction == 'right':
        next_x = start_x + 1
        next_y = start_y
    elif direction == 'down':
        next_x = start_x
        next_y = start_y + 1
    elif direction == 'left':
        next_x = start_x - 1
        next_y = start_y
    else:
        print "ERROR: not a valid direction"
        pass

    # only return valid coordinates
    if (next_x,next_y) in MAZE_MAP:
        return (next_x,next_y)

def visit_tiles(current_tile=(0,0),prev=None, path=None,complete_paths=None):
    start = (0,0)
    end = (3,3)
    if path is None:
        path = [start]
        complete_paths = []

    if current_tile != end:
        next_coords = MAZE_CONN[current_tile]
        if prev in next_coords or prev is None:
            # make sure this tile connects back to previous
            for coord in next_coords:
                if coord is not prev and coord not in path:
                    path.append(coord)
                    visit_tiles(coord,current_tile,path,complete_paths)
                    path.pop()
                
    elif current_tile == end:
        stringified_tuples = [ str(x) for x in path ]
        stringified_path = "|".join(stringified_tuples)
        complete_paths.append(stringified_path)
    
    return complete_paths


print "OK HERE WE GO"

MAZE_CONN = get_all_neighbors(MAZE_MAP)
print visit_tiles()
