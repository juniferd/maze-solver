import draw
import image
import ant

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
        self.a_svg_maze = self.get_svg_attr()
        self.a_maze = {str(k) :[tuple(i) for i in v] for k,v in self.a_maze_map.items()}
        self.a_food_exits = {}
        self.a_food = FOOD
            
        self.ants = []
        self.ant_positions = {}
        self.markers = {}
        self.visited_tiles = {}

        image.init(self.a_maze_map,self.a_goal,self.a_solution,False)

    def get_svg_attr(self):
        svg_maze = []
        for tile in self.a_maze_map:
            temp = {}
            x = tile[0]
            y = tile[1]
            tile_type = self.a_maze_map[tile]

            # blank tile
            svg_maze.append({'x':20*x,'y':20*y,'width':20,'height':20,'fill':'#dddddd','class':'bg'})

            # left-right
            if (tile_type == '-'):
                svg_maze.append({'x':20*x,'y':(20*y)+5,'width':20,'height':10,'fill':'#ffffff'})
            # up-down
            elif (tile_type == '|'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':20,'fill':'#ffffff'})
            # up-right
            elif (tile_type == 'l'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':15,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+15,'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # up-left
            elif (tile_type == 'j'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':15,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # down-right
            elif (tile_type == 'r'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y)+5,'width':10,'height':15,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+15,'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # down-left
            elif (tile_type == '7'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y)+5,'width':10,'height':15,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # up-right-down
            elif (tile_type == '<'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':20,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+15,'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # up-left-down
            elif (tile_type == '>'):
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':20,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':5,'height':10,'fill':'#ffffff'})
            # up-left-right
            elif (tile_type == 'v'):
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':20,'height':10,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':5,'fill':'#ffffff'})
            # down-left-right
            elif (tile_type == '^'):
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':20,'height':10,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+5,'y':(20*y)+15,'width':10,'height':5,'fill':'#ffffff'})
            # cross
            elif (tile_type == '+'):
                svg_maze.append({'x':(20*x),'y':(20*y)+5,'width':20,'height':10,'fill':'#ffffff'})
                svg_maze.append({'x':(20*x)+5,'y':(20*y),'width':10,'height':20,'fill':'#ffffff'})

        return svg_maze

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
        a = ant.Ant(self)
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
        connections = self.a_connections[new_goal]
        if len(connections) > 0:
            print 'NEW GOAL: ',new_goal
            return new_goal
        else:
            self.create_new_goal()

    def reduce_food(self):
        if self.a_food > 0:
            self.a_food -= 1
            print 'FOOD STATUS: ',self.a_food
        else:
            self.drop_new_food()

    def record_food_gathered(self,coord):
        str_coord = str(coord)
        if str_coord in self.a_food_exits:
            self.a_food_exits[str_coord]['count'] += 1
        else:
            self.a_food_exits[str_coord] = {}
            self.a_food_exits[str_coord]['coord'] = coord
            self.a_food_exits[str_coord]['count'] = 1

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

    def leave_marker(self,ant,coord,chemical,dist,strength):
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
            'food_gathered' : self.a_food_exits,
            'counter' : self.counter
        }
        
        return json.dumps(ret)

