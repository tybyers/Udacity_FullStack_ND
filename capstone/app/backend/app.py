import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

from .models import db_drop_and_create_all, setup_db, Race, Distance

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

#db_drop_and_create_all()

@app.route('/')
def index():
  # TODO: Replace this with a render of a more useful index page
  data = get_races().get_json()['race']
  print(data)
  return render_template('pages/index.html', data=data)

@app.route('/race', methods=['GET'])
def get_races():
  # join with distances to get distance name
  upcoming_races = Race.query.filter(Race.date >= datetime.datetime.today()).all()
  past_races = Race.query.filter(Race.date < datetime.datetime.today()).all()
  print(past_races)

  # TODO: build in something to differentiate current races from past races
  def fill_details(raceq):
    return [{
      "id": r.id,
      "name": r.name,
      "city": r.city,
      "state": r.state,
      "website": r.website,
      "distance_id": r.distance_id,
      "date": r.date
    } for r in raceq]

  race_details = {}
  race_details['upcoming'] = fill_details(upcoming_races)
  race_details['past'] = fill_details(past_races)

  if len(race_details['upcoming']) + len(race_details['past']) == 0:
    abort(404)

  return jsonify({
    'success': True,
    'races': race_details
  })

## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)