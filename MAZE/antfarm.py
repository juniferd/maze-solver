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

    # TODO: BREAK THIS DOWN!!!

    def explore(self,previous):
        connections = self.farm.a_connections
        coord = previous['pos']
        neighbors = connections[coord]
        new_position = coord
        ant_mode = 'explore'
        has_food = False
        exits = self.farm.a_exits

        self.leave_chemical(coord,'search')
        
        # need to figure out which of these coordinates to take
        # in order of preference:
        # 1. path to food (aka chemical marker)
        # 2. not a direction any ant has already been in
        options = list(neighbors)
        counter_dict = {}
        for neighbor in neighbors:
            # does the next room have food?
            if neighbor == self.farm.a_goal[0]:
                options = [neighbor]
                print 'found food source'
                ant_mode = 'find exit'
                has_food = True
                break
            # is the next room an exit?
            elif neighbor in exits:
                options = [neighbor]
                print 'found an exit'
                ant_mode = 'find food'
                break
            
            try:
                markers = self.farm.get_markers(neighbor)
                if markers != None:
                    # loop through each of the markers
                    for antid in markers:
                        # is it food?
                        if markers[antid]['chemical'] == 'food':
                            options = [neighbor]
                            print 'found food path'
                            ant_mode = 'retrieve food'
                            break
                        else:
                            try:
                                options.remove(neighbor)
                            except ValueError:
                                pass
                            this_counter = markers[antid]['strength']
                            counter_dict[this_counter] = neighbor
            except AttributeError:
                print 'PASS: no markers'
                pass
            

        #print 'possible options: ',options
        
        l = len(options)
        if l > 0:
            r = randint(0,l-1)
            new_position = options[r]
        else:
        # has ant already tried all options? pick option with lowest counter
            new_position = counter_dict[min(counter_dict)]

        return new_position, ant_mode, has_food

    def find_food(self,previous):
        # this should only happen if an ant finds an exit before it finds food
        connections = self.farm.a_connections
        coord = previous['pos']
        neighbors = connections[coord]
        dist_exit = self.get_min_dist(neighbors,'exit')
        new_position = coord
        ant_mode = 'find food'
        has_food = previous['has_food']
        exits = self.farm.a_exits
        
        if coord in exits:
            self.leave_chemical(coord,'exit',0)
            has_food = False
        else:
            self.leave_chemical(coord,'exit',dist_exit)

        options = list(neighbors)
        counter_dict = {}
        for neighbor in neighbors:
            # does the next room have food?
            if neighbor == self.farm.a_goal[0]:
                options = [neighbor]
                print 'found food'
                ant_mode = 'retrieve food'
                has_food = True
                
                break
            try:
                markers = self.farm.get_markers(neighbor)
                
                if markers != None:
                    # loop through each of the markers
                    for antid in markers:
                        # is it food?
                        if markers[antid]['chemical'] == 'food':
                            options = [neighbor]
                            print 'found food path'
                            ant_mode = 'retrieve food'
                            has_food = False
                            
                            break

                        try:
                            options.remove(neighbor)
                        except ValueError:
                            pass

                        this_counter = markers[antid]['strength']
                        counter_dict[this_counter] = neighbor

            except AttributeError:
                print 'PASS: no markers'
                pass
        
        #print 'possible options: ',options
        
        l = len(options)
        if l > 0:
            print 'find food random options'
            r = randint(0,l-1)
            new_position = options[r]
        else:
            print 'find food min counter'
        # has ant already tried all options? pick option with lowest counter
            new_position = counter_dict[min(counter_dict)]

        return new_position,ant_mode,has_food

    def find_exit(self,previous):
        # 'find exit' behavior is like 'explore'
        # this should only happen if an ant finds food before it finds an exit

        connections = self.farm.a_connections
        coord = previous['pos']
        neighbors = connections[coord]

        dist_food = self.get_min_dist(neighbors,'food')

        new_position = coord
        ant_mode = 'find exit'
        has_food = previous['has_food']
        
        exits = self.farm.a_exits
        
        if coord == self.farm.a_goal[0]:
            self.leave_chemical(coord,'food',0)
            has_food = True
        else:
            self.leave_chemical(coord,'food',dist_food)
        
        options = list(neighbors)
        counter_dict = {}
        for neighbor in neighbors:
            # first see if any of these are exits
            if neighbor in exits:
                options = [neighbor]
                print 'found exit'
                ant_mode = 'retrieve food'
                has_food = False
                
                break
            try:
                markers = self.farm.get_markers(neighbor)
                
                if markers != None:

                    # loop through each of the markers
                    for antid in markers:
                        # is it exit?
                        if markers[antid]['chemical'] == 'exit':
                            options = [neighbor]
                            print 'found exit path'
                            ant_mode = 'retrieve food'
                            has_food = True
                            
                            break
                        # is it this ant's marker?
                        if antid == self.id:
                            try:
                                options.remove(neighbor)
                            except ValueError:
                                pass
                        this_counter = markers[antid]['strength']
                        counter_dict[this_counter] = neighbor

            except AttributeError:
                print 'PASS: no markers'
                pass
        
        #print 'possible options: ',options
        
        l = len(options)
        if l > 0:
            r = randint(0,l-1)
            new_position = options[r]
        else:
        # has ant already tried all options? pick option with lowest counter
            new_position = counter_dict[min(counter_dict)]


        return new_position, ant_mode, has_food

    def retrieve_food(self,previous):
        connections = self.farm.a_connections
        coord = previous['pos']
        neighbors = connections[coord]
        new_position = coord
        ant_mode = 'retrieve food'
        has_food = previous['has_food']
        dist_food = self.get_min_dist(neighbors,'food')
        dist_exit = self.get_min_dist(neighbors,'exit')
        exits = self.farm.a_exits

        exit_dict = {}
        food_dict = {}
        counter_dict = {}
        next_exit = None
        next_food = None
        options = list(neighbors)
        exits_count = defaultdict(int)
        foods_count = defaultdict(int)
        for neighbor in neighbors:
            # is neighbor food?
            
            if neighbor == self.farm.a_goal[0]:
                print 'neighbor is food!'
                next_food = neighbor
                dist_food = 0
            # is neighbor exit?
            if neighbor in exits:
                print 'neighbor is exit!'
                next_exit = neighbor
                dist_exit = 0
            try:
                markers = self.farm.get_markers(neighbor)
                
                if markers != None:
                    # loop through each of the markers
                    
                    for antid in markers:
                        # does one of these have an 'exit' marker?
                        if markers[antid]['chemical'] == 'exit':
                            this_dist = markers[antid]['dist']
                            exit_dict[this_dist] = neighbor
                            exits_count[neighbor] += 1
                        if markers[antid]['chemical'] == 'food':
                            this_dist = markers[antid]['dist']
                            food_dict[this_dist] = neighbor
                            foods_count[neighbor] += 1
                        if antid == self.id:
                            try:
                                options.remove(neighbor)
                            except ValueError:
                                pass
                        this_counter = markers[antid]['strength']
                        counter_dict[this_counter] = neighbor

            except AttributeError:
                print 'PASS: no markers'
                pass

        # if ant has food, go toward exit
        if has_food:
            if coord == self.farm.a_goal[0]:
                self.leave_chemical(coord,'food',0)
            else:
                self.leave_chemical(coord,'food',dist_food)
            print 'go to exit',
            # look for markers that point to exit
            # if no markers point to an exit, retrace 'food' path toward weakest 'food' marker
            # is the next square exit?
            if next_exit != None:
                print '... found exit!'
                new_position = next_exit
                has_food = False

            else:
                
                if not exit_dict:
                # ok there's no exit markers for some reason
                    print '... no exit markers',

                    if len(options) > 0:
                        print '... shuffle'
                        new_position = food_dict[max(food_dict)]
                        ant_mode = 'find exit'
                        #shuffle(options)
                        #new_position = options[0]
                    else:
                        print '... min counter'
                        new_position = counter_dict[min(counter_dict)]
                else:
                    print '... trace back to exit ',
                    
                    new_position = exit_dict[min(exit_dict)]


        # if ant does not have food, go toward food
        else:
            if coord in exits:
                self.leave_chemical(coord,'exit',0)
            else:
                self.leave_chemical(coord,'exit',dist_exit)
            print 'go to food',
            # is the next square food?
            if next_food != None:
                print '... found food!'
                new_position = next_food
                has_food = True
                
            else:
                
                if not food_dict:
                # ok there's no food markers for some reason
                    print '... no food markers',
                    if len(options) > 0:
                        print '... shuffle'
                        #shuffle(options)
                        #new_position = options[0]
                        new_position = exit_dict[max(exit_dict)]
                        ant_mode = 'find food'
                    else:
                        print '... min counter'
                        new_position = counter_dict[min(counter_dict)]
                else:
                    print '... trace back to food'
                    new_position = food_dict[min(food_dict)]

            
        return new_position, ant_mode, has_food


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
    
    def increment_ant(self,previous):
        '''
        ant modes include 'explore','find food','find exit','retrieve food'
        ant chemicals include 'search','exit','food'
        '''
        maze_map = self.farm.a_maze_map

        if previous:
            
            ant_mode = previous['mode']

            if ant_mode == 'explore':
                new_position, ant_mode, has_food = self.explore(previous)
            elif ant_mode == 'find exit':
                new_position, ant_mode, has_food = self.find_exit(previous)
            elif ant_mode == 'find food':
                new_position, ant_mode, has_food = self.find_food(previous)
            elif ant_mode == 'retrieve food':
                new_position, ant_mode, has_food = self.retrieve_food(previous)

            print 'ant mode ',self.id,': ',ant_mode, ', ',new_position
        else:
            # spawn the ants randomly on the maze
            maze_len = len(maze_map)
            n = sqrt(maze_len) - 1
            x = randint(0,n)
            y = randint(0,n)
            new_position = (x,y)
            ant_mode = 'explore'
            has_food = False

        ant = {
            'antid' : self.id,
            'mode' : ant_mode,
            'pos' : new_position,
            'has_food' : has_food
        }

        return ant
    
