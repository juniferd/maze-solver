import shelve
import antfarm

class World(object):

    def __init__(self):
        self.farm = antfarm.AntFarm()
        self.farm.populate_farm()
        self.info = {}
        self.client_counter = 0


persisted = shelve.open("antfarm")

def list_worlds():
    if not persisted.has_key('worlds'):
        return [0]

    return persisted['worlds']

def get_world(maze_id):
    world_key = "world/%s" % maze_id

    if not persisted.has_key('worlds'):
        persisted['worlds'] = set()

    world_list = persisted['worlds']
    world_list.add(maze_id)
    persisted['worlds'] = world_list

    if not persisted.has_key(world_key):
        world = World()
        persisted[world_key] = world

    return persisted[world_key]


def save_world(maze_id, world):
    world_key = "world/%s" % maze_id
    persisted[world_key] = world
    persisted.sync()

def sync():
    persisted.sync()