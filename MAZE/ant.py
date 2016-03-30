import antfarm

from random import randint, shuffle
from math import sqrt
from collections import defaultdict

CHEMICAL_STRENGTH = 25

class Result(object):
    def __init__(self):
        pass


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

        sm_result = Result()

        def found_food(ant, **kwargs):
            print "ANT FOUND FOOD"
            ant_mode = 'find exit'
            sm_result.ant_mode = ant_mode
            sm_result.has_food = True
            sm_result.food_gathered = False
            sm_result.breakout = True
            
            # reduce food in antfarm
            self.farm.reduce_food()

        def found_exit(ant, **kwargs):
            print "ANT FOUND EXIT"
            ant_mode = 'find food'

            sm_result.ant_mode = ant_mode
            sm_result.has_food = has_food
            sm_result.food_gathered = False
            sm_result.breakout = True
        
        def retrieve_found_exit(ant, **kwargs):
            ant_mode = 'retrieve food'
            if has_food:
                print "ANT FOUND EXIT - RETRIEVING FOOD"

                sm_result.ant_mode = ant_mode
                sm_result.has_food = False
                # drop off food in antfarm
                sm_result.food_gathered = True
                sm_result.breakout = True
            else:

                sm_result.ant_mode = ant_mode
                sm_result.has_food = has_food
                sm_result.food_gathered = False
                sm_result.breakout = False

        def retrieve_found_food(ant, **kwargs):
            ant_mode = 'retrieve food'
            if not has_food:
                print "ANT FOUND FOOD - RETRIEVING FOOD"
                sm_result.ant_mode = ant_mode
                sm_result.has_food = True
                sm_result.food_gathered = False
                sm_result.breakout = True
                
                # reduce food in antfarm
                self.farm.reduce_food()
            else:

                sm_result.ant_mode = ant_mode
                sm_result.has_food = has_food
                sm_result.food_gathered = False
                sm_result.breakout = False


        def retrieve_follow_food(ant, **kwargs):
            print "ANT FOUND FOOD PATH - RETRIEVING FOOD - HAS FOOD? ",has_food
            ant_mode = 'retrieve food'

            sm_result.ant_mode = ant_mode
            sm_result.has_food = has_food
            sm_result.food_gathered = False
            sm_result.breakout = True

        def retrieve_follow_exit(ant, **kwargs):
            print "ANT FOUND EXIT PATH - RETRIEVING FOOD - HAS FOOD? ",has_food
            ant_mode = 'retrieve food'

            sm_result.ant_mode = ant_mode
            sm_result.has_food = has_food
            sm_result.food_gathered = False
            sm_result.breakout = True

        def do_nothing(ant, **kwargs):

            sm_result.ant_mode = ant_mode
            sm_result.has_food = has_food
            sm_result.food_gathered = False
            sm_result.breakout = False

        exits = self.farm.a_exits

        HANDLERS = {
            'explore:food' : found_food,
            'explore:exit' : found_exit,
            'explore:foodmarker' : retrieve_follow_food,
            'find food:food' : retrieve_found_food,
            'find food:exit' : do_nothing,
            'find food:foodmarker' : retrieve_follow_food,
            'find exit:food' : do_nothing,
            'find exit:exit' : retrieve_found_exit,
            'find exit:exitmarker' : retrieve_follow_exit,
            'retrieve food:food' : retrieve_found_food,
            'retrieve food:exit' : retrieve_found_exit,

        }
        
        key = ant_mode
        if neighbor in exits:
            key = "%s:%s" % (ant_mode, "exit")
        if neighbor == self.farm.a_goal[0]:
            key = "%s:%s" % (ant_mode, "food")
        if marker == 'food':
            key = "%s:%s" % (ant_mode, "foodmarker")
        if marker == 'exit':
            key = "%s:%s" % (ant_mode, "exitmarker")



        if key in HANDLERS:
            HANDLERS[key](self)
        else:
            sm_result.breakout = False
            sm_result.ant_mode = ant_mode
            sm_result.has_food = has_food
            sm_result.food_gathered = False
        return sm_result


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


    def prep_neighbors(self, ant_mode, coord, has_food, change_coord, mode_counter):
        connections = self.farm.a_connections
        exits = self.farm.a_exits
        neighbors = connections[coord]

        prep_result = Result()

        prep_result.options = list(neighbors)
        prep_result.strength_dict = {}
        prep_result.exit_dict = {}
        prep_result.food_dict = {}

        prep_result.exits_count = defaultdict(int)
        prep_result.foods_count = defaultdict(int)

        prep_result.ant_mode = ant_mode
        prep_result.has_food = has_food

        print 'INITIAL OPTIONS: ',prep_result.options
        for neighbor in neighbors:

            # do mode-specific checks on neighboring square
            sm_result = self.state_machine(ant_mode,neighbor,has_food)
            prep_result.breakout = sm_result.breakout

            if sm_result.breakout:
                print 'BREAK OUT NEIGHBOR LOOP'
                prep_result.options = [neighbor]
                prep_result.ant_mode = sm_result.ant_mode
                prep_result.has_food = sm_result.has_food

                if sm_result.food_gathered:
                    self.farm.record_food_gathered(neighbor)
                break

            try:
                # get markers for neighbor
                markers = self.farm.get_markers(neighbor)
                print 'INITIAL MARKERS: ',markers
                if markers != None:
                    # loop through each of the markers
                    for antid in markers:
                        sm_result_m = self.state_machine(ant_mode,neighbor,has_food,markers[antid]['chemical'])
                        prep_result.breakout = sm_result_m.breakout
                        
                        this_strength = markers[antid]['strength']
                        prep_result.strength_dict[this_strength] = neighbor

                        if ant_mode == 'retrieve food':
                            if markers[antid]['chemical'] == 'exit':

                                this_dist = markers[antid]['dist']
                                prep_result.exit_dict[this_dist] = neighbor
                                prep_result.exits_count[neighbor] += 1
                                
                            if markers[antid]['chemical'] == 'food':
                                this_dist = markers[antid]['dist']
                                prep_result.food_dict[this_dist] = neighbor
                                prep_result.foods_count[neighbor] += 1

                        if sm_result_m.breakout:
                            print 'BREAK OUT MARKER LOOP'
                            prep_result.options = [neighbor]
                            prep_result.ant_mode = sm_result_m.ant_mode
                            prep_result.has_food = sm_result_m.has_food
                            break

                        if ant_mode == 'explore' or ant_mode == 'find food':
                            try:
                                prep_result.options.remove(neighbor)
                            except ValueError:
                                pass
                        else:
                            if antid == self.id:
                                try:
                                    prep_result.options.remove(neighbor)
                                except ValueError:
                                    pass

            except AttributeError:
                print 'PASS: no markers'
                pass
        print 'OPTIONS AFTER LOOP: ',prep_result.options
        return prep_result

    def get_next_ant_move(self,previous):
        ant_mode = previous['mode']
        coord = previous['pos']
        has_food = previous['has_food']
        change_coord = previous['change_coord']
        mode_counter = previous['mode_counter']
        new_position = None
        prep = Result()

        prep_result = self.prep_neighbors(ant_mode,coord,has_food,change_coord,mode_counter)
        
        prep.change_coord = change_coord
        
        new_ant_mode = prep_result.ant_mode
        new_has_food = prep_result.has_food
        
        if prep_result.ant_mode != 'retrieve food' and prep_result.ant_mode != 'change':
            if len(prep_result.options) > 0:
                print 'SHUFFLE OPTIONS ',prep_result.options
                shuffle(prep_result.options)
                new_position = prep_result.options[0]
            else:
                print 'MIN STRENGTH DICT ', prep_result.strength_dict
                new_position = prep_result.strength_dict[min(prep_result.strength_dict)]
        
        elif prep_result.ant_mode == 'change':
            connections = self.farm.a_connections
            
            neighbors = list(connections[coord])
            print 'CHANGE ',neighbors
            
            if mode_counter < 6:
                print 'CHANGE MODE - NEIGHBORS: ',neighbors,', ',change_coord
                new_ant_mode = 'change'
            else:
                if prep_result.has_food :
                    new_ant_mode = 'find exit'
                else:
                    new_ant_mode = 'explore'

            if len(neighbors) > 1:
                try:
                    neighbors.remove(change_coord)
                    print 'REMOVE PREVIOUS COORD: ',neighbors
                except ValueError:
                    pass
                print 'OPTIONS: ',neighbors

            shuffle(neighbors)
            new_position = neighbors[0]
            prep.change_coord = coord
        
        elif prep_result.ant_mode == 'retrieve food':
            if prep_result.breakout:
                print 'BREAK OUT '
                new_position = prep_result.options[0]
            else:
                if prep_result.has_food:
                    if not prep_result.exit_dict:
                        print '... no exit markers',
                        if len(prep_result.options) > 0:
                            print '... shuffle'
                            shuffle(prep_result.options)
                            new_position = prep_result.options[0]
                            new_ant_mode = 'find exit'
                        else:
                            print '... min strength',prep_result.strength_dict
                            new_position = prep_result.strength_dict[min(prep_result.strength_dict)]
                    else:
                        print 'trace back to exit'
                        new_position = prep_result.exit_dict[min(prep_result.exit_dict)]
                        #new_position = self.get_popular_coord(prep_result.exit_dict,prep_result.exits_count)
                else:    
                    if not prep_result.food_dict:
                        print '... no food markers',
                        if len(prep_result.options) > 0:
                            print '... shuffle'
                            shuffle(prep_result.options)
                            new_position = prep_result.options[0]
                            new_ant_mode = 'find food'
                        else:
                            print '... min strength',prep_result.strength_dict
                            new_position = prep_result.strength_dict[min(prep_result.strength_dict)]
                    else:
                        print 'trace back to food',prep_result.food_dict
                        new_position = prep_result.food_dict[min(prep_result.food_dict)]
                        #new_position = self.get_popular_coord(prep_result.food_dict,prep_result.foods_count)

        prep.new_position = new_position
        prep.new_ant_mode = new_ant_mode
        prep.new_has_food = new_has_food
        return prep

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
            mode_counter = previous['mode_counter']
            change_coord = previous['change_coord']


            self.prep_chemical_coord(ant_mode,coord,has_food)
            prep = self.get_next_ant_move(previous)
            new_position = prep.new_position
            new_ant_mode = prep.new_ant_mode
            new_has_food = prep.new_has_food
            change_coord = prep.change_coord

            if new_ant_mode == ant_mode and new_has_food == has_food:
                mode_counter += 1
                if mode_counter > 100 and new_ant_mode != 'explore':
                    change_coord = coord
                    new_ant_mode = 'change'
                    mode_counter = 0
                    print 'CHANGE MODES ',change_coord
                    

            else:
                mode_counter = 0
                change_coord = False

            print self.id,': ',new_ant_mode, ' ',new_position,' mode counter: ',mode_counter,'change mode: ',change_coord
            print '---------------------'
        else:
            # spawn the ants randomly on the maze
            new_position, new_ant_mode, new_has_food = self.spawn_ant()
            change_coord = False
            mode_counter = 0

        ant = {
            'antid' : self.id,
            'mode' : new_ant_mode,
            'pos' : new_position,
            'has_food' : new_has_food,
            'mode_counter' : mode_counter,
            'change_coord' : change_coord
        }

        return ant
    
