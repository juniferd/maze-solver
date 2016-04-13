import json

from threading import Thread,Timer
from operator import itemgetter
from flask import Flask,render_template,session,request

import antfarm

app = Flask(__name__)
#COUNTER = 0
ANT_FARM = None
WORLD = {}
CLIENT_COUNTER = 0

@app.route('/')
@app.route('/<num>')
def ant_maze(num=None):
    global ANT_FARM

    if not ANT_FARM:
        ANT_FARM = antfarm.AntFarm()

    return render_template('maze.html', num=num)


@app.route('/ant/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    global WORLD
    global CLIENT_COUNTER

    if action_id > CLIENT_COUNTER:
        CLIENT_COUNTER = action_id

    return WORLD[action_id]

@app.route('/ant/api/v1.0/max-counter', methods=['GET'])
def get_max_counter():
    global ANT_FARM
    
    ANT_FARM.counter
    ret = {
        "max": ANT_FARM.counter
    }

    return json.dumps(ret)

@app.route('/ant/api/v1.0/get-maze', methods=['GET'])
def get_maze():
    global ANT_FARM

    ANT_FARM.a_svg_maze
    ret = {
        'maze' : ANT_FARM.a_svg_maze
    }

    return json.dumps(ret)


def increment_world():
    #global COUNTER
    global WORLD
    global ANT_FARM
    global CLIENT_COUNTER

    if not ANT_FARM:
        # populate ant farm
        ANT_FARM = antfarm.AntFarm()        
        ANT_FARM.populate_farm()
    
    # only do work on the server 10 moves ahead of client
    if ANT_FARM.counter <= 10 + CLIENT_COUNTER:
        ANT_FARM.run_farm()
        WORLD[ANT_FARM.counter] = ANT_FARM.make_json()

        ANT_FARM.counter += 1

        print 'ANT FARM COUNTER: ',ANT_FARM.counter
        #COUNTER += 1
    
def threaded_function():   
    increment_world()

    t = Timer(0.5,threaded_function)
    t.start()

if __name__ == '__main__':
    threaded_function()
    
    app.run()