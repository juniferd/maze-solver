import draw
import image

import json
from random import randint, shuffle
from math import sqrt
from collections import defaultdict

CHEMICAL_STRENGTH = 25
FOOD = 25

class AntFarm(object):
    ANT_ID = 0

    def __init__(self):
        a_maze = draw.Maze(30)
        a_maze.draw_maze()

        self.a_maze_map = a_maze.get_maze_map()
        self.a_goal = [a_maze.get_goal()]
        self.a_solution = a_maze.get_solution()
        self.a_connections = a_maze.get_all_neighbors(self.a_maze_map)
        self.counter = 0
        self.a_exits = a_maze.get_exits()
        self.a_maze = {str(k) :[tuple(i) for i in v] for k,v in self.a_connections.items()}
        self.a_food_exits = {}
        self.a_food = FOOD
            
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

    def drop_new_food(self):
        # remove existing goal
        self.a_goal.pop(0)
        # create new goal
        new_goal = self.create_new_goal()
        self.a_goal.append(new_goal)
        # reset amount of food at goal
        self.a_food = FOOD

    def create_new_goal(self):
        dict_keys = list(self.a_maze_map.keys())
        r = randint(0,len(dict_keys)-1)
        new_goal = dict_keys[r]
        print 'NEW GOAL: ',new_goal
        return new_goal

    def reduce_food(self):
        if self.a_food > 0:
            self.a_food -= 1
        else:
            self.drop_new_food()

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

    def leave_marker(self,ant,coord,chemical,dist,strength=CHEMICAL_STRENGTH):
        '''
        {
            (x,y) : {
                'ant00' : {
                    'antid' : 'ant00',
                    
                    'chemical' : 'search',
                    'strength' : 50,
                    'dist' : None
                },
                'ant01' : {
                    'antid' : 'ant01',
                    
                    'chemical' : 'food',
                    'strength' : 50,
                    'dist' : 31
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
        
        self.markers[str_coord][ant.id]['chemical'] = chemical
        self.markers[str_coord][ant.id]['strength'] = strength
        self.markers[str_coord][ant.id]['dist'] = dist
        
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
            'food' : self.a_goal,
            'maze' : self.a_maze
        }
        
        return json.dumps(ret)

class Ant(object):
    def __init__(self,farm):
        print 'make an ant'
        self.farm = farm

    def get_min_dist(self,neighbors,chemical):
        dists = []

        for neighbor in neighbors:
            
            markers = self.farm.get_markers(neighbor)
            if markers != None:
                for antid in markers:
                    if markers[antid]['chemical'] == chemical:
                        dist = markers[antid]['dist']
                        if dist != None:
                            dists.append(dist)
       
        try:
            min_dist = min(dists) + 1
        except ValueError:
            min_dist = None

        return min_dist

    def get_popular_coord(self,dist_dict,counts_dict):
        combo = {}
        min_dist = {}
        
        # first get minimum distance for each coordinate
        for dist in dist_dict:
            if dist != None:
                coord = dist_dict[dist]
                if coord in min_dist:
                    if dist < min_dist[coord]:
                        min_dist[coord] = float(dist)
                else:
                    min_dist[coord] = float(dist)
        # now get combination value distance * num of ants
        for coord in min_dist:
            dist = min_dist[coord]
            inv_count = float(1 / float(counts_dict[coord]))
            combo[coord] = float(inv_count * dist)

        sorted_keys = sorted(combo, key=combo.get)
        print 'sorted keys: ',sorted_keys
        try:
            best_position = sorted_keys[0]
        except IndexError:
            best_position = dist_dict[min(dist_dict)]

        return best_position

    def leave_chemical(self,coord,chemical,dist=None):
        # leave a chemical marker
        marker_pos = coord
        marker_type = chemical
        marker_strength = CHEMICAL_STRENGTH
        
        if marker_type == 'exit':
            marker_strength = CHEMICAL_STRENGTH * 5
        elif marker_type == 'food':
            marker_strength = CHEMICAL_STRENGTH * 10
        
        self.farm.leave_marker(self,marker_pos,marker_type,dist,marker_strength)
    
    def spawn_ant(self):

        maze_len = len(self.farm.a_maze_map)
        n = sqrt(maze_len) - 1
        x = randint(0,n)
        y = randint(0,n)
        new_position = (x,y)
        ant_mode = 'explore'
        has_food = False
        
        return new_position, ant_mode, has_food

    

    def state_machine(self,ant_mode,neighbor,has_food,marker=None):

        def found_food(ant, **kwargs):
            print "ANT FOUND FOOD"
            ant_mode = 'find exit'

            return True,ant_mode,True

        def found_exit(ant, **kwargs):
            print "ANT FOUND EXIT"
            ant_mode = 'find food'

            return True,ant_mode,False
        
        def retrieve_found_exit(ant, **kwargs):
            ant_mode = 'retrieve food'
            if has_food:
                print "ANT FOUND EXIT - RETRIEVING FOOD"
                return True,ant_mode,False
            else:
                return False,ant_mode,has_food

        def retrieve_found_food(ant, **kwargs):
            ant_mode = 'retrieve food'
            if not has_food:
                print "ANT FOUND FOOD - RETRIEVING FOOD"
                return True,ant_mode,True
            else:
                return False,ant_mode,has_food

        def retrieve_found_path(ant, **kwargs):
            print "ANT FOUND FOOD PATH - RETRIEVING FOOD"
            ant_mode = 'retrieve food'
            return True,ant_mode,has_food

        def do_nothing(ant, **kwargs):   
            return False,ant_mode,has_food

        exits = self.farm.a_exits

        HANDLERS = {
            'explore:food' : found_food,
            'explore:exit' : found_exit,
            'explore:foodmarker' : retrieve_found_path,
            'find food:food' : retrieve_found_food,
            'find food:exit' : do_nothing,
            'find food:foodmarker' : retrieve_found_path,
            'find exit:food' : do_nothing,
            'find exit:exit' : retrieve_found_exit,
            'find exit:exitmarker' : retrieve_found_path,
            'retrieve food:food' : retrieve_found_food,
            'retrieve food:exit' : retrieve_found_exit
        }
        
        key = ""
        if neighbor in exits:
            key = "%s:%s" % (ant_mode, "exit")
        if neighbor == self.farm.a_goal[0]:
            key = "%s:%s" % (ant_mode, "food")
        if marker == 'food':
            key = "%s:%s" % (ant_mode, "foodmarker")
        if marker == 'exit':
            key = "%s:%s" % (ant_mode, "exitmarker")



        if key in HANDLERS:
            return HANDLERS[key](self)
        else:
            return False,ant_mode,has_food


    def prep_chemical_coord(self,ant_mode,coord,has_food):
        connections = self.farm.a_connections
        exits = self.farm.a_exits
        neighbors = connections[coord]
        goal = self.farm.a_goal[0]

        dist_exit = self.get_min_dist(neighbors,'exit')
        dist_food = self.get_min_dist(neighbors,'food')

        if ant_mode == 'explore':
            self.leave_chemical(coord,'search')

        elif ant_mode == 'find food':
            if coord in exits:
                self.leave_chemical(coord,'exit',0)
            else:
                self.leave_chemical(coord,'exit',dist_exit)

        elif ant_mode == 'find exit':
            if coord == goal:
                self.leave_chemical(coord,'food',0)
            else:
                self.leave_chemical(coord,'food',dist_food)

        elif ant_mode == 'retrieve food':
            if has_food:
                if coord == goal:
                    self.leave_chemical(coord,'food',0)
                else:
                    self.leave_chemical(coord,'food',dist_food)
            else:
                if coord in exits:
                    self.leave_chemical(coord,'exit',0)
                else:
                    self.leave_chemical(coord,'exit',dist_exit)


    def prep_neighbors(self, ant_mode, coord, has_food):
        connections = self.farm.a_connections
        exits = self.farm.a_exits
        neighbors = connections[coord]

        options = list(neighbors)
        strength_dict = {}
        exit_dict = {}
        food_dict = {}

        exits_count = defaultdict(int)
        foods_count = defaultdict(int)

        for neighbor in neighbors:

            # do mode-specific checks on neighboring square
            breakout,ant_mode,has_food = self.state_machine(ant_mode,neighbor,has_food)
            
            if breakout:
                options = [neighbor]
                break

            try:
                # get markers for neighbor
                markers = self.farm.get_markers(neighbor)

                if markers != None:
                    # loop through each of the markers
                    for antid in markers:
                        breakout,ant_mode,has_food = self.state_machine(ant_mode,neighbor,has_food,markers[antid]['chemical'])
            
                        if breakout:
                            options = [neighbor]
                            break

                        # does one of these have an 'exit' marker?
                        if markers[antid]['chemical'] == 'exit':

                            this_dist = markers[antid]['dist']
                            exit_dict[this_dist] = neighbor
                            exits_count[neighbor] += 1
                            
                        if markers[antid]['chemical'] == 'food':
                            this_dist = markers[antid]['dist']
                            food_dict[this_dist] = neighbor
                            foods_count[neighbor] += 1

                        this_strength = markers[antid]['strength']
                        strength_dict[this_strength] = neighbor

                        if ant_mode == 'retrieve food' or ant_mode == 'find exit':
                            if antid == self.id:
                                try:
                                    options.remove(neighbor)
                                except ValueError:
                                    pass
                        else:
                            try:
                                options.remove(neighbor)
                            except ValueError:
                                pass


            except AttributeError:
                print 'PASS: no markers'
                pass

        return options, strength_dict, food_dict, foods_count, exit_dict, exits_count, ant_mode, has_food, breakout

    def get_next_ant_move(self,previous):
        ant_mode = previous['mode']
        coord = previous['pos']
        has_food = previous['has_food']
        new_position = None

        options, strength_dict, food_dict, foods_count, exit_dict, exits_count, new_ant_mode, new_has_food, breakout = self.prep_neighbors(ant_mode,coord,has_food)
        if ant_mode == 'explore' or ant_mode == 'find food' or ant_mode == 'find exit':
            if len(options) > 0:
                shuffle(options)
                new_position = options[0]
            else:
                new_position = strength_dict[min(strength_dict)]
        elif ant_mode == 'retrieve food':
            if breakout:
                new_position = options[0]
            else:
                if has_food:
                    if not exit_dict:
                        print '... no exit markers',
                        if len(food_dict) > 0:
                            print '... max food dict'
                            new_position = food_dict[max(food_dict)]
                            new_ant_mode = 'find exit'
                        else:
                            print '... min strength'
                            new_position = strength_dict[min(strength_dict)]
                    else:
                        print 'trace back to exit'
                        new_position = self.get_popular_coord(exit_dict,exits_count)
                else:    
                    if not food_dict:
                        print '... no food markers',
                        if len(exit_dict) > 0:
                            print '... max exit dict'
                            new_position = exit_dict[max(exit_dict)]
                            new_ant_mode = 'find food'
                        else:
                            print '... min strength'
                            new_position = strength_dict[min(strength_dict)]
                    else:
                        print 'trace back to food'
                        new_position = self.get_popular_coord(food_dict,foods_count)
        return new_position, new_ant_mode, new_has_food

    def increment_ant(self,previous):
        '''
        ant modes include 'explore','find food','find exit','retrieve food'
        ant chemicals include 'search','exit','food'
        '''
        maze_map = self.farm.a_maze_map

        if previous:
            
            ant_mode = previous['mode']
            coord = previous['pos']
            has_food = previous['has_food']
            
            self.prep_chemical_coord(ant_mode,coord,has_food)

            
            new_position, ant_mode, has_food = self.get_next_ant_move(previous)
            

            print self.id,': ',ant_mode, ', ',new_position
        else:
            # spawn the ants randomly on the maze
            new_position, ant_mode, has_food = self.spawn_ant()

        ant = {
            'antid' : self.id,
            'mode' : ant_mode,
            'pos' : new_position,
            'has_food' : has_food
        }

        return ant
    
