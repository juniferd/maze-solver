from random import randint, shuffle
from math import sqrt

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
UNICODE_MAP = {
    '-' : u'\u2501',
    '|' : u'\u2503',
    'l' : u'\u2517',
    'j' : u'\u251b',
    'r' : u'\u250f',
    '7' : u'\u2513',
    '<' : u'\u2523',
    '>' : u'\u252b',
    'v' : u'\u253b',
    '^' : u'\u2533',
    '+' : u'\u254b'
}
SYMBOL_KEY = []
for key in SYMBOL_MAP:
    SYMBOL_KEY.append(key)

class Maze(object):

    def __init__(self,board_size):
        self.__maze = self.generate_maze(board_size)

    ## generate a maze
    def generate_maze(self,board_size):
        maze_map = {}
        solution_path = []

        # first generate a maze that has all possible options
        maze_map = self.generate_init_board(board_size)
        
        # then generate a solution path
        solution_paths = self.generate_solution_paths(maze_map)
        # now pick just one path
        solution_path = self.pick_path(solution_paths)
        # pick new tiles for this solution path
        new_tiles = self.generate_new_tiles(solution_path)
        #for path in solution_paths:
        #    print 'possible path: ',path
        
        print 'solution path: ',solution_path
        print 'connections: ',new_tiles
        return maze_map

    ## generate the initial "maze"
    def generate_init_board(self,board_size):
        maze_map = {}
        for i in range(0,board_size):
            for j in range(0,board_size):
                #num = randint(0,10)
                #tile_key = SYMBOL_KEY[num]

                maze_map[(i,j)] = '+'
        return maze_map
    ## generate many solution paths
    def generate_solution_paths(self,maze_map,curr=(0,0),visited=None,solutions=None):
        start = (0,0)
        n = int(sqrt(len(maze_map)))
        end = (n-1,n-1)
        #print '-----------------'
        if visited == None:
            visited = []
            solutions = []

        sol_len = len(solutions)
        if sol_len < 100:
            if curr != end:
                next_coords = self.get_neighbors(maze_map,curr)
                for tile in visited:
                # remove any previously visited tiles
                    try:
                        next_coords.remove(tile)
                    except ValueError:
                        pass
                #print 'visited: ',visited
                #print 'current: ',curr
                #print 'next possible coords: ',next_coords
                if next_coords:
                    visited.append(curr)
                    shuffle(next_coords)
                    for coord in next_coords:
                        next_tile = coord
                        self.generate_solution_paths(maze_map,next_tile,visited,solutions)
                    
                    visited.pop()
                    
            elif curr == end:
                #print "we found the end"
                visited.append(end)
                stringified_tuples = [ str(x) for x in visited ]
                stringified_path = "|".join(stringified_tuples)
                solutions.append(stringified_path)
                visited.pop()
        #print '-----------------'
        return solutions

    def pick_path(self,path):
        arr_path = []
        for line in path:
            line = line.split('|')
            for i,entry in enumerate(line):
                line[i] = tuple(int(x) for x in entry[1:-1].split(","))
            # make sure each tile only one away
            check_path = self.check_path_distance(line)
            if check_path:
                arr_path.append(line)
            
        n = len(arr_path)
        r = randint(0,n-1)
        random_path = arr_path[r]
        return random_path

    def check_path_distance(self,path):
        is_valid = True
        for i,coord in enumerate(path):
            start_x = coord[0]
            start_y = coord[1]
            next_x = 0
            next_y = 0
            try:
                next_x = path[i+1][0]
                next_y = path[i+1][1]
            except IndexError:
                return is_valid
            dx = abs(next_x - start_x)
            dy = abs(next_y - start_y)
            #print 'coord: ',coord
            #print 'dx ',dx
            #print 'dy ',dy
            #print '---'
            if dx > 1 or dy > 1:
                is_valid = False
                return is_valid

            if dx == dy:
                is_valid = False
                return is_valid

        return is_valid

    def generate_new_tiles(self,path):
        connections = self.get_connections(path)


        return connections

    def get_connections(self,path):
        connections = {}
        for i,coord in enumerate(path):
            group = connections.setdefault(coord,[])
            try:
                left = path[i-1]
                if i-1 >= 0:
                    group.append(left)
            except IndexError:
                pass
            
            try:
                right = path[i+1]
                if i+1 < len(path):
                    group.append(right)
            except IndexError:
                pass


        return connections

    def get_all_neighbors(self,maze_map):
        connections = {}

        for tile in maze_map:
            next_coords = self.get_neighbors(maze_map,tile)
            connections[tile] = next_coords
        return connections

    def get_neighbors(self,maze_map,coord):
        maze_key = maze_map[coord]
        connections = SYMBOL_MAP[maze_key]
        next_coords = []

        for connection in connections:
            next_coord = self.get_next_coord(maze_map,coord,connection)
            if next_coord is not None:
                next_coords.append(next_coord)

        return next_coords

    def get_next_coord(self,maze_map,coord,direction):
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
            next_x = None
            next_y = None
            pass

        # only return valid coordinates
        if (next_x,next_y) in maze_map:
            return (next_x,next_y)

    ## convert to unicode visual
    def draw_unicode(self,maze_map):
        viz_map = {}

        for (x,y) in maze_map:
            v = maze_map[(x,y)]
            viz_map[(x,y)] = UNICODE_MAP[v]

        return viz_map 

    ## draw a maze
    def draw_maze(self):
        n = int(sqrt(len(self.__maze)))
        viz = self.draw_unicode(self.__maze)
        
        #for key in self.__maze:
        #    print key,": ",self.__maze[key], viz[key]

        print "--------"
        
        for y in range(0,n):
            for x in range(0,n):
                print viz[(x,y)],
            print '\n'