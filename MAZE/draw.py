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
        solution_path = self.pick_path(solution_paths,board_size)
        #print 'solution path: ',solution_path
        # pick new tiles for this solution path
        solution_connections,new_tiles = self.generate_new_tiles(solution_path)
        #print 'connections: ',solution_connections
        for tile in new_tiles:
            maze_map[tile] = new_tiles[tile]

        # form minimum spanning tree that connects to solution path without any cycles
        other_connections = self.get_min_spanning_tree(solution_path,maze_map)
        
        other_paths_dict = {}
        for point in other_connections:
            if other_connections[point]:
                other_paths_dict[point] = other_connections[point]
            else:
                # special case where connecting back to solution path
                pass
        #print 'other_paths_dict: ',other_paths_dict
        other_tiles = self.generate_other_tiles(other_paths_dict,solution_connections)
        #print other_tiles        
        for tile in other_tiles:
            maze_map[tile] = other_tiles[tile]
        #print 'solution path: ',solution_path
        
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

        if  len(visited) > (n * n)/2:
            return solutions
        
        sol_len = len(solutions)
        if sol_len < 1:
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

                if len(visited) < (n * n)/2:
                    stringified_tuples = [ str(x) for x in visited ]
                    stringified_path = "|".join(stringified_tuples)
                    solutions.append(stringified_path)
                visited.pop()
        #print '-----------------'
        return solutions

    def pick_path(self,path,board_size):
        n = board_size
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
        #print 'connections: ',connections
        directions = {}
        tiles = {}

        for coord in connections:
            directions[coord] = self.get_directions(coord,connections[coord])
            # add on extra directions for start and end tiles
            if coord == path[0]:
                # start tile needs to connect to outside
                choices = ['up','left',['up','left']]
                r = randint(0,2)
                choice = choices[r]
                if type(choice) == list:
                    directions[coord].extend(choice)
                else:
                    directions[coord].append(choice)
            elif coord == path[-1]:
                # end tile needs to connect to outside
                choices = ['right','down',['right','down']]
                r = randint(0,2)
                choice = choices[r]
                if type(choice) == list:
                    directions[coord].extend(choice)
                else:
                    directions[coord].append(choice)
            
            # now get corresponding symbol
            tiles[coord] = self.get_symbol(directions, coord)
        #print 'directions: ',directions
        #print 'tiles: ',tiles
        return connections,tiles

    def get_symbol(self,directions,coord):
        sym = None
        for key in SYMBOL_MAP:
            directions[coord].sort()
            SYMBOL_MAP[key].sort()
            if directions[coord] == SYMBOL_MAP[key]:
                sym = key
        return sym

    def generate_other_tiles(self,connections=None,solution_connections=None):
        #TODO: probably just need to combine generate_new_tiles with this since it's doing the same thing
        directions = {}
        tiles = {}

        for coord in connections:
            if coord in solution_connections:
                # need to update solution connections to connect
                connections[coord].extend(solution_connections[coord])
                # TODO: need to have start and end tile exit to outside

            #print coord,": ",connections[coord],
            directions[coord] = self.get_directions(coord,connections[coord])
            if len(directions[coord]) < 2:
                # TODO: add more variance
                
                if directions[coord] == ['up']:
                    directions[coord].append('down')
                elif directions[coord] == ['down']:
                    directions[coord].append('up')
                elif directions[coord] == ['left']:
                    directions[coord].append('right')
                elif directions[coord] == ['right']:
                    directions[coord].append('left')
                else:
                    #print 'ERROR in generating other tiles directions',directions[coord]
                    pass
                
            # now get corresponding symbol
            tiles[coord] = self.get_symbol(directions, coord)

        #print 'directions: ',directions
        #print 'tiles: ',tiles
        return tiles        

    def get_min_spanning_tree(self,solution_path,maze_map):
        solution_set = set(solution_path)
        board_sets = {}
        connections = {}

        for coord in maze_map:
            connections[coord] = []
            if coord not in solution_set:
                arr_coord = [coord]
                board_sets[coord] = set(arr_coord)
                
            else:
                board_sets[coord] = solution_set

        #print 'solution set: ',solution_set
        for coord in board_sets:
            # pick a random neighbor up, right, down, left
            neighbor = self.pick_random_neighbor(coord)
            if neighbor in maze_map:
                # check to make sure this coordinate is on the board
                
                # check to see will union create a cycle/loop?
                if board_sets[neighbor] == board_sets[coord]:
                    is_valid = False
                    #print 'could not connect ',coord,' to ',neighbor
                else:
                    is_valid = True
                    #print 'connecting ',coord,' to ',neighbor
                    connections[coord].append(neighbor)
                    connections[neighbor].append(coord)
                
                if is_valid:
                    # do some work
                    board_sets[neighbor] = board_sets[neighbor] | board_sets[coord]
                    # for each coordinate in the unioned sets, do the same
                    for tile in board_sets[neighbor]:
                        board_sets[tile] = board_sets[neighbor]
                    #print 'new set: ',coord,': ',board_sets[coord]

        

        return connections
        

    def pick_random_neighbor(self,coord):
        direction = ['up','right','down','left']
        r = randint(0,3)
        neighbor = direction[r]
        #print 'coord: ',coord,
        if neighbor == 'up':
            next_tile = (coord[0],coord[1]-1)
            #print 'up: ',
        elif neighbor == 'right':
            next_tile = (coord[0]+1,coord[1])
            #print 'right: ',
        elif neighbor == 'down':
            next_tile = (coord[0],coord[1]+1)
            #print 'down: ',
        elif neighbor == 'left':
            next_tile = (coord[0]-1,coord[1])
            #print 'left: ',
        else:
            print 'ERROR getting random neighbor'
            return
        #print next_tile
        return next_tile

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

    def get_directions(self,start_coord,next_coords):
        directions = []
        start_x = start_coord[0]
        start_y = start_coord[1]

        for next_coord in next_coords:
            next_x = next_coord[0]
            next_y = next_coord[1]

            dx = next_x - start_x
            dy = next_y - start_y

            if dx == 0 and dy == 1:
                direction = 'down'
            elif dx == 0 and dy == -1:
                direction = 'up'
            elif dx == 1 and dy == 0:
                direction = 'right'
            elif dx == -1 and dy == 0:
                direction = 'left'
            else:
                print 'ERROR no direction found'
                pass

            directions.append(direction)

        return directions

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

        
        for y in range(0,n):
            for x in range(0,n):
                print viz[(x,y)],
            print '\n'