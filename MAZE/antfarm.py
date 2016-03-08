import draw
import image
from random import randint

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

class AntFarm(object):
    def __init__(self):
        a_maze = draw.Maze(40)
        a_maze.draw_maze()

        self.a_maze_map = a_maze.get_maze_map()
        self.a_goal = a_maze.get_goal()
        self.a_solution = a_maze.get_solution()

        self.a_maze = a_maze

        self.ants = []

        image.init(self.a_maze_map,self.a_goal,self.a_solution,False)

    def get_maze(self):
        return self.a_maze_map

    def get_goal(self):
        return self.a_goal

    def Ant(self):
        a = Ant(self)
        self.ants.append(a)

        return a

class Ant(object):
    def __init__(self,farm):
        print 'make an ant'
        self.farm = farm

    def move_ant(self,previous):
        maze_map = self.farm.a_maze_map
        if previous:

            coord = previous['pos']
            symbol = maze_map[coord]
            options = SYMBOL_MAP[symbol]
            next_coords = []
            for direction in options:
                next_coord = self.farm.a_maze.get_next_coord(maze_map,coord,direction)
                if next_coord:
                    next_coords.append(next_coord)
            l = len(next_coords)
            r = randint(0,l-1)

            new_position = next_coords[r]
        else:
            new_position = (0,0)


        ant = {
            'mode' : 'search',
            'pos' : new_position
        }

        return ant

