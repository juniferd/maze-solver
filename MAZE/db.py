import cPickle as pickle
import gzip
import antfarm
import copy
import os
import sys

import threading

db_lock = threading.Lock()

# this holds the farm and the max client counter for a world
class World(object):
    def __init__(self):
        self.farm = antfarm.AntFarm()
        self.farm.populate_farm()
        self.client_counter = 0


# this holds the saved JSON turns for a world 
class WorldInfo(object):
    def __init__(self):
        self.info = {}

# KEYS: 
#   worlds - set([1,2,3...])
#   world/:id/bucket/:bucket - WorldInfo
#   world/:id - World


# everywhere we are using persistence.get() change it to get_key()
# every where we are using persistence.set() change it to set_key()
def get_key(key_name, default_value=None):
    # check if file for key_name exists
    ext = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_path = ext+"/db/%s" % key_name
    if not os.path.exists(file_path):
        return default_value

    db_lock.acquire(True) # blocking
    # open file
    with open(file_path, "rb") as f:
        try:
            data = pickle.load(f)
        except EOFError:
            print ("EOF ERROR, RETURNING DEFAULT VALUE FOR %s" % key_name)
            data = default_value
    db_lock.release()
    # use pickle to read the data from file
    # return the object from pick
    if data:
        return data

    return default_value

def set_key(key_name, value):
    # pickle value
    print("PERSISTING KEY", key_name)
    db_lock.acquire(True)
    ext = os.path.dirname(os.path.realpath(sys.argv[0]))
    key_name = ext+"/db/%s" % (key_name)
    with open(key_name, "wb") as f:
        pickle.dump(value, f)
    db_lock.release()
    # open file
    # save value to file and close file

def list_worlds():
    return get_key('worlds', default_value=set([0]))

INFO_CHUNK_SIZE=50
# This function returns the saved 'turn' associated with the 
# given world  (maze_id) at the 'action_id'
def get_info(maze_id, action_id):
    bucket = int(action_id) / INFO_CHUNK_SIZE
    info_key = 'world.%s.bucket.%s' % (maze_id, bucket)
    print("INFO KEY", info_key, "ACTION ID", action_id)

    saved_info = get_key(info_key)
    if saved_info:
        return saved_info.info[action_id]

def save_info(info, maze_id, action_id):
    bucket = int(action_id) / INFO_CHUNK_SIZE

    info_key = 'world.%s.bucket.%s' % (maze_id, bucket)

    saved_info = get_key(info_key)
    if not saved_info:
        print("BUILDING NEW WORLD INFO", info_key)
        saved_info = WorldInfo()

    saved_info.info[action_id] = info

    set_key(info_key, saved_info)

def get_world(maze_id):
    world_key = "world.%s" % maze_id

    if not get_key('worlds'):
        set_key('worlds',set())

    world_list = list_worlds()
    world_list.add(maze_id)
    set_key('worlds',world_list)

    if not get_key(world_key):
        world = World()
        set_key(world_key,world)

    return get_key(world_key)

def save_world(maze_id, world):
    world_key = "world.%s" % maze_id
    set_key(world_key,world)
