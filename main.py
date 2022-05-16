from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash

import os

from replit import db

app = Flask(__name__)


# if "items" not in db:
db["items"] = {"0": {"id": "0", "name": "default item 1", "quantity": 5}, "1": {"id": "1", "name": "default item 2", "quantity": 5}, "2":{"id": "2", "name": "default item 3", "quantity": 5}}
db["locations"] = {"0": {"id": "0", "name": "default location", "address": "301 Warehouse Rd, Oregon, USA"}}


@app.route('/')
def index():
    return render_template('inventory.html', items=db["items"].values(), locations=db["locations"].values())


@app.route('/item', methods=['POST'])
def postItem():
  # if no id, assign a random one
  id = os.urandom(10).hex()
  
  if id in request.form:
    id = request.form['id']

  name = request.form['name']
  quantity = request.form['quantity']

  item = {"id": id, "name": name, "quantity": quantity}

  db["items"][id] = item

  return redirect('/')


# post location, for adding or editing a post
@app.route('/location', methods=['POST'])
def postLocation():
  # if no id, assign a random one
  id = os.urandom(10).hex()
  
  if "id" in request.form:
    id = request.form['id']

  name = request.form['name']
  address = request.form['address']

  item = {"id": id, "name": name, "address": address}

  db["locations"][id] = item

  return redirect('/')

# new location page
@app.route('/newLocation', methods=['GET'])
def addLocation():
  return render_template('location.html')

# edit location page
@app.route('/editLocation', methods=['POST'])
def editLocation():
  id = request.args.get("id")
  loc = db["locations"][id]
  
  return render_template('location.html', location=loc)


# delete location
@app.route('/removeLocation', methods=['POST'])
def removeLocation():
  id = request.args.get("id")
  if id != None:
    del db["locations"][id]
    
  return redirect('/')

  

app.run(host='0.0.0.0', port=81)