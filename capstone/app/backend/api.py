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

@app.route('/races', methods=['GET'])
def get_races():
  # join with distances to get distance name
  upcoming_races = Race.query.filter(Race.date >= datetime.datetime.today()).all()
  past_races = Race.query.filter(Race.date < datetime.datetime.today()).all()

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

@app.route('/distances', methods=['GET'])
def get_distances():
  distances = Distance.query.all()

  dists = {}
  for dist in distances:
    dists[dist.id] = {'name': dist.name, 'distance_km': dist.distance_km,
                      'distance_miles': dist.distance_mi}

  if len(dists) == 0:
    abort(404)

  return jsonify({
    'success': True,
    'distances': dists
  })

@app.route('/races-detail/<int:id>', methods=['GET'])
def get_race_detail(id):
  race = Race.query.filter(Race.id == id).\
    join(Distance, Race.distance_id == Distance.id).first() 

  if race is None:
    abort(404)

  race_deets = {'name': race.name, 'date': race.date,
                'city': race.city, 'state': race.state,
                'distance_name': race.distance.name,
                'distance_km': race.distance.distance_km,
                'distance_miles': race.distance.distance_mi,
                'website': race.website,
                'race_id': id, 'distance_id': race.distance.id}

  return jsonify({
    'success': True,
    'race': race_deets
  })

@app.route('/races/create', methods=['POST'])
def create_race():
  raise NotImplementedError

@app.route('/distances/create', methods=['POST'])
def create_distance():
  raise NotImplementedError

@app.route('/races/<int:id>', methods=['PATCH'])
def update_race(payload, id):
  raise NotImplementedError

@app.route('/distances/<int:id>', methods=['PATCH'])
def update_distance(payload, id):
  raise NotImplementedError

@app.route('/races/<int:id>', methods=['DELETE'])
def delete_race(payload, id):
  raise NotImplementedError

@app.route('/distances/<int:id>', methods=['DELETE'])
def delete_distance(payload, id):
  raise NotImplementedError


## Error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 40,
        "message": "Bad Request"
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
  return jsonify({
    "success": False,
    "error": 405,
    "message": "Method not allowed"
  }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
# @app.errorhandler(AuthError)
# def authentication_failed(AuthError):
#     return jsonify({
#         "success": False,
#         "error": AuthError.status_code,
#         "message": "Authentication failed: {}".format(AuthError)
#         }), 401

## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)