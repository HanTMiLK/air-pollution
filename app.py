from flask import Flask
from flask import render_template
from threading import Thread
import requests
import json
import os

     
app = Flask(__name__)
app.debug = True
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/update')
def update():
    os.popen(os.path.join(r'python /home/dmcl/python_web','test.py'))
    return "<h1>OK</h1>"

if __name__ == '__main__':
    app.run(host='10.133.199.50',port=5000)	
