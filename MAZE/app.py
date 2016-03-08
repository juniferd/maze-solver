import json

from threading import Thread,Timer
from flask import Flask,render_template,session

import antfarm

app = Flask(__name__)
COUNTER = 0
ANT_FARM = None
DIRS = {}

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



@app.route('/ant/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    global DIRS

    for ant in ANT_FARM.ants:

        try:
            a_val = DIRS[ant][action_id]
        except KeyError:
            a_val = None
            pass

    return json.dumps(a_val)

@app.route('/turn/')
@app.route('/turn/<num>')
def turn(num=None):
    
    ret = {'turn' : COUNTER}


    return json.dumps(ret)

def increment_world():
    global COUNTER
    global DIRS
    global ANT_FARM

    if not ANT_FARM:
        ANT_FARM = antfarm.AntFarm()
        ant = ANT_FARM.Ant()
        DIRS[ant] = {}
    
    for ant in ANT_FARM.ants:
        try:
            previous = DIRS[ant][COUNTER - 1]
        except KeyError:
            previous = None
        DIRS[ant][COUNTER] = ant.move_ant(previous)
    
    COUNTER += 1
    
def threaded_function():   
    increment_world()

    t = Timer(1.0,threaded_function)
    t.start()

if __name__ == '__main__':
    threaded_function()
    
    app.run()