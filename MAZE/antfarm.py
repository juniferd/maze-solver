import draw
import image

import json
from random import randint, shuffle
from math import sqrt

CHEMICAL_STRENGTH = 25

class AntFarm(object):
    ANT_ID = 0

    def __init__(self):
        a_maze = draw.Maze(40)
        a_maze.draw_maze()

        self.a_maze_map = a_maze.get_maze_map()
        self.a_goal = [a_maze.get_goal()]
        self.a_solution = a_maze.get_solution()
        self.a_connections = a_maze.get_all_neighbors(self.a_maze_map)
        self.counter = 0
        self.a_maze = a_maze
        #for connection in self.a_connections:
        #    print 'connection: ',connection,
        #    print ', ',self.a_connections[connection]
        self.ants = []
        self.ant_positions = {}
        self.markers = {}
        self.visited_tiles = {}

        image.init(self.a_maze_map,self.a_goal,self.a_solution,False)

    def get_maze(self):
        return self.a_maze_map

    def get_goal(self):
        return self.a_goal

    def populate_farm(self):
        for x in range(0,10):
            ant = self.Ant()

    def run_farm(self):
        self.record_visited_tile()
        for ant in self.ants:
            try:
                current = self.ant_positions[ant]
                
            except KeyError:
                current = None
            self.ant_positions[ant] = ant.increment_ant(current)
        
        self.reduce_marker_strength()


    def Ant(self):
        a = Ant(self)
        self.ants.append(a)
        a.id = "ant" + str(AntFarm.ANT_ID)
        AntFarm.ANT_ID += 1

        return a
    def record_visited_tile(self):
        for ant in self.ant_positions:
            pos = self.ant_positions[ant]['pos']
            self.visited_tiles[str(pos)] = pos

    def reduce_marker_strength(self):
        del_keys = []
        for marker_pos in self.markers:
            for antid in self.markers[marker_pos]:
                if self.markers[marker_pos][antid]['strength'] > 0:
                    self.markers[marker_pos][antid]['strength'] -= 1
                else:
                    del_keys.append([marker_pos,antid])
        for del_key in del_keys:
            marker_pos = del_key[0]
            antid = del_key[1]
            del self.markers[marker_pos][antid]

    def leave_marker(self,ant,coord,chemical):
        '''
        {
            (x,y) : {
                'ant00' : {
                    'antid' : 'ant00',
                    'counter' : 0,
                    'chemical' : 'search',
                    'strength' : 50
                },
                'ant01' : {
                    'antid' : 'ant01',
                    'counter' : 1,
                    'chemical' : 'food',
                    'strength' : 50
                }
            }
            
        }
        '''
        str_coord = str(coord)
        if str_coord not in self.markers:
            self.markers[str_coord] = {}
        if self not in self.markers[str_coord]:
            self.markers[str_coord][ant.id] = {}

        self.markers[str_coord][ant.id]['antid'] = ant.id
        self.markers[str_coord][ant.id]['pos'] = coord
        self.markers[str_coord][ant.id]['counter'] = self.counter
        self.markers[str_coord][ant.id]['chemical'] = chemical
        self.markers[str_coord][ant.id]['strength'] = CHEMICAL_STRENGTH
        
    def get_markers(self,coord):
        
        str_coord = str(coord)
        try:
            markers = self.markers[str_coord]
        except KeyError,AttributeError:
            markers = None
        return markers

    def make_json(self):
        ants = []
        for ant in self.ant_positions:
            ants.append(self.ant_positions[ant])
        visited_tiles = []
        for tile in self.visited_tiles:
            visited_tiles.append(self.visited_tiles[tile])

        ret = {
            'ants' : ants,
            'markers' : self.markers,
            'visited' : visited_tiles,
            'food' : self.a_goal
        }
        
        return json.dumps(ret)

class Ant(object):
    def __init__(self,farm):
        print 'make an ant'
        self.farm = farm

    def increment_ant(self,previous):
        maze_map = self.farm.a_maze_map
        connections = self.farm.a_connections

        if previous:
            
            coord = previous['pos']
            ant_mode = previous['mode']

            # leave a chemical marker
            marker_pos = coord
            # is this coordinate where "food" is located?
            if marker_pos == self.farm.a_goal:
                marker_type = 'food'
            else:
                marker_type = 'search'
            
            previous_marker = self.farm.leave_marker(self,marker_pos,marker_type)            

            neighbors = connections[coord]
            #print ', neighbors: ',neighbors

            # need to figure out which of these coordinates to take
            # in order of preference:
            # 1. path to food (aka chemical marker)
            # 2. not a direction i've already been in
            options = list(neighbors)
            counter_dict = {}
            for neighbor in neighbors:
                # does the next room have food?
                #if neighbor == self.farm.a_goal:
                #    options = [neighbor]
                #    break
                try:
                    markers = self.farm.get_markers(neighbor)
                    if markers != None:
                        # loop through each of the markers
                        for antid in markers:
                            # is it food?
                            if markers[antid]['chemical'] == 'food':
                            #    options = [neighbor]
                            #    break
                                print 'found food path'
                            
                            else:
                                try:
                                    options.remove(neighbor)
                                except ValueError:
                                    pass
                                # is it this ant's marker?
                                if antid == self.id:
                                    this_counter = markers[antid]['counter']
                                    counter_dict[this_counter] = neighbor
                except AttributeError:
                    print 'PASS'
                    pass
            #print 'possible options: ',options
            
            l = len(options)
            if l > 0:
                r = randint(0,l-1)
                new_position = options[r]
            else:
            # has ant already tried all options? pick option with lowest counter
                new_position = counter_dict[min(counter_dict)]
        else:
            # spawn the ants randomly on the maze
            maze_len = len(maze_map)
            n = sqrt(maze_len) - 1
            x = randint(0,n)
            y = randint(0,n)
            new_position = (x,y)
            ant_mode = 'searching'

        ant = {
            'antid' : self.id,
            'mode' : ant_mode,
            'pos' : new_position
        }

        return ant
    
