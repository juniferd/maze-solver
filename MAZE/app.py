import json

from threading import Thread,Timer
from flask import Flask,render_template,session

import antfarm

app = Flask(__name__)
COUNTER = 0
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

@app.route('/ant/api/v1.0/total-ants/', methods=['GET'])
def total_ants():
    num = len(ANT_FARM.ants)

    return json.dumps(num)

@app.route('/ant/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    global WORLD
    global CLIENT_COUNTER

    if action_id > CLIENT_COUNTER:
        CLIENT_COUNTER = action_id

    return WORLD[action_id]

def increment_world():
    global COUNTER
    global WORLD
    global ANT_FARM
    global CLIENT_COUNTER

    if not ANT_FARM:
        # populate ant farm
        ANT_FARM = antfarm.AntFarm()        
        ANT_FARM.populate_farm()
    
    # only do work on the server 10 moves ahead of client
    if COUNTER <= 10 + CLIENT_COUNTER:
        ANT_FARM.run_farm()
        WORLD[COUNTER] = ANT_FARM.make_json()

        ANT_FARM.counter += 1
        COUNTER += 1
    
def threaded_function():   
    increment_world()

    t = Timer(0.5,threaded_function)
    t.start()

if __name__ == '__main__':
    threaded_function()
    
    app.run()