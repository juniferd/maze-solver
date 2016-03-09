import draw
import image
from random import randint

class AntFarm(object):
    def __init__(self):
        a_maze = draw.Maze(40)
        a_maze.draw_maze()

        self.a_maze_map = a_maze.get_maze_map()
        self.a_goal = a_maze.get_goal()
        self.a_solution = a_maze.get_solution()
        self.a_connections = a_maze.get_all_neighbors(self.a_maze_map)

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
        connections = self.farm.a_connections
        if previous:

            coord = previous['pos']
            #print 'coord: ',coord,

            neighbors = connections[coord]
            #print ', neighbors: ',neighbors
                
            l = len(neighbors)
            r = randint(0,l-1)

            new_position = neighbors[r]
        else:
            new_position = (0,0)

        # leave a chemical marker


        ant = {
            'mode' : 'search',
            'pos' : new_position
        }

        return ant

