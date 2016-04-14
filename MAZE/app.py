import json

from threading import Thread,Timer
from operator import itemgetter
from flask import Flask,render_template,session,request
from collections import defaultdict
from flask.ext.compress import Compress

import antfarm
import db

app = Flask(__name__)
Compress(app)

@app.route('/')
@app.route('/<int:maze_id>')
def ant_maze(maze_id=0):
    world = db.get_world(maze_id)

    return render_template('maze.html', maze_id=maze_id)


@app.route('/ant/api/v1.0/actions/<int:maze_id>/<int:action_id>', methods=['GET'])
def get_action(maze_id,action_id):
    world = db.get_world(maze_id)

    if action_id > world.client_counter:
        world.client_counter = action_id
        db.save_world(maze_id, world)

    return world.info[action_id]

@app.route('/ant/api/v1.0/<int:maze_id>/max-counter', methods=['GET'])
def get_max_counter(maze_id):
    world = db.get_world(maze_id)
    ret = {
        "max": world.farm.counter
    }

    return json.dumps(ret)

@app.route('/ant/api/v1.0/<int:maze_id>/get-maze', methods=['GET'])
def get_maze(maze_id):
    world = db.get_world(maze_id)

    ret = {
        'maze' : world.farm.a_svg_maze
    }

    return json.dumps(ret)


def increment_world():
    for key in db.list_worlds():
        world = db.get_world(key)  
        # only do work on the server 10 moves ahead of client
        if world.farm.counter <= 10 + world.client_counter:
            world.farm.run_farm()
            world.info[world.farm.counter] = world.farm.make_json()

            world.farm.counter += 1

            print 'ANT FARM COUNTER: ', world.farm.counter
            db.save_world(key, world)

def threaded_function():   
    increment_world()

    t = Timer(0.5,threaded_function)
    t.start()

if __name__ == '__main__':
    threaded_function()
    
    app.run()