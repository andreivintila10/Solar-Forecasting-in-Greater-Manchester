from flask import Flask, render_template, Response,make_response
 
import redis
import random
import json
import numpy as np


app = Flask(__name__)

d = {'x' : [11, 28, 388, 400, 420], 'y' : [1, 2, 3, 4, 5]}


@app.route('/streamdata')
def event_stream():
    make_response(d.to_json())

@app.route('/stream')
def show_basic():
    x = random.randint(0,101)
    y = random.randint(0,101)
    print(json.dumps(d))
    return render_template("manchester_forecast.html",data=json.dumps(d))
 
 
 
if __name__ == '__main__':
    app.run(threaded=True,
    host='0.0.0.0'
)