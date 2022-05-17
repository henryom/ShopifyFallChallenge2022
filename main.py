from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import os

from replit import db

app = Flask(__name__)



@app.route('/')
def index():
    items = db["items"].values()
    # add location names if ids are valid
    for item in items:
      item["locationName"] = db["locations"][item["locationID"]]["name"] if item["locationID"] in db["locations"] else "-"
      
    return render_template('inventory.html', items=items, locations=db["locations"].values())

# Items

@app.route('/item', methods=['POST'])
def postItem():

  # if no id, assign a random one
  id = os.urandom(10).hex()
  
  if id in request.form:
    id = request.form['id']

  name = request.form['name']
  quantity = request.form['quantity']
  locationID = request.form['locationID']
  notes = request.form['notes']

  item = {"id": id, "name": name, "quantity": quantity, "locationID": locationID, "notes": notes}

  db["items"][id] = item

  return redirect('/')

# new item page
@app.route('/newItem', methods=['GET'])
def addItem():
  return render_template('item.html', locations=db["locations"].values())

# edit item page
@app.route('/editItem', methods=['POST'])
def editItem():
  id = request.args.get("id")
  item = db["items"][id]
  
  return render_template('item.html', item=item, locations=db["locations"].values())

# delete item
@app.route('/removeItem', methods=['POST'])
def removeItem():
  id = request.args.get("id")
  if id != None:
    del db["items"][id]
    # TODO: remove references
    
  return redirect('/')

# Locations

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
    # TODO: remove references
    
  return redirect('/')

  

app.run(host='0.0.0.0', port=81)