import json

from threading import Thread,Timer
from flask import Flask,render_template,session

import antfarm

app = Flask(__name__)
COUNTER = 0
ANT_FARM = None
WORLD = {}

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/hello/')
@app.route('/hello/<num>')
def hello(num=None):
    global ANT_FARM

    if not ANT_FARM:
        ANT_FARM = antfarm.AntFarm()

    return render_template('hello.html', num=num)

@app.route('/ant/api/v1.0/total-ants/', methods=['GET'])
def total_ants():
    num = len(ANT_FARM.ants)

    return json.dumps(num)

@app.route('/ant/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    global WORLD    
    return WORLD[action_id]


def increment_world():
    global COUNTER
    global WORLD
    global ANT_FARM

    if not ANT_FARM:
        # populate ant farm
        ANT_FARM = antfarm.AntFarm()        
        ANT_FARM.populate_farm()
        
    ANT_FARM.run_farm()
    WORLD[COUNTER] = ANT_FARM.make_json()

    ANT_FARM.counter += 1
    COUNTER += 1
    
def threaded_function():   
    increment_world()

    t = Timer(1.0,threaded_function)
    t.start()

if __name__ == '__main__':
    threaded_function()
    
    app.run()