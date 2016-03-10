import draw
import image
from random import randint, shuffle
from math import sqrt

class AntFarm(object):
    def __init__(self):
        a_maze = draw.Maze(40)
        a_maze.draw_maze()

        self.a_maze_map = a_maze.get_maze_map()
        self.a_goal = a_maze.get_goal()
        self.a_solution = a_maze.get_solution()
        self.a_connections = a_maze.get_all_neighbors(self.a_maze_map)
        self.counter = 0
        self.a_maze = a_maze

        self.ants = []

        self.markers = {}

        image.init(self.a_maze_map,self.a_goal,self.a_solution,False)

    def get_maze(self):
        return self.a_maze_map

    def get_goal(self):
        return self.a_goal

    def Ant(self):
        a = Ant(self)
        self.ants.append(a)

        return a

    def leave_marker(self,ant,coord,chemical):
        '''
        {
            (x,y) : {
                'ant00' : {
                    'counter' : 0,
                    'marker' : 'search'
                },
                'ant01' : {
                    'counter' : 1,
                    'marker' : 'food'
                }
            }
            
        }
        '''

        if coord not in self.markers:
            self.markers[coord] = {}
        if self not in self.markers[coord]:
            self.markers[coord][ant] = {}

        self.markers[coord][ant]['counter'] = self.counter
        self.markers[coord][ant]['marker'] = chemical
        
        #print 'leave marker at ',coord,': ',self.markers[coord][ant]['counter']
        pass
    def get_markers(self,coord):
        #print 'get marker at ',coord
        
        try:
            markers = self.markers[coord]
        except KeyError,AttributeError:
            markers = None
        return markers

class Ant(object):
    def __init__(self,farm):
        print 'make an ant'
        self.farm = farm

    def move_ant(self,previous):
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
                        for ant in markers:
                            
                            # is it food?
                            if markers[ant]['marker'] == 'food':
                                options = [neighbor]
                                break
                            # is it this ant's marker?
                            elif ant == self:
                                options.remove(neighbor)
                                this_counter = markers[ant]['counter']
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
            marker_pos = None
            marker_type = 'search'
            ant_mode = 'searching'

        ant = {
            'marker' : {
                'pos' : marker_pos,
                'marker' : marker_type
            },
            'mode' : ant_mode,
            'pos' : new_position
        }

        return ant
    
