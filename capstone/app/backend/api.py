import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from models import db_drop_and_create_all, setup_db, Race, Distance
from auth.auth import AuthError, requires_auth

KM_2_MILE = 0.621371

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  #available to public
  @app.route('/races', methods=['GET'])
  def get_races():
    upcoming_races = Race.query.filter(Race.date >= datetime.today()).all()
    past_races = Race.query.filter(Race.date < datetime.today()).all()
    # TODO: join with distance to get better distance stuff

    def fill_details(raceq):
      return {r.id: {
        "name": r.name,
        "city": r.city,
        "state": r.state,
        "website": r.website,
        "distance_id": r.distance_id,
        "date": r.date
      } for r in raceq}

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
  @requires_auth('get:distance')
  def get_distances(payload):
    distances = Distance.query.all()

    dists = {}
    for dist in distances:
      dists[dist.id] = {'name': dist.name, 'distance_km': dist.distance_km,
                        'distance_mi': dist.distance_mi}

    if len(dists) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'distances': dists
    })

  @app.route('/races-detail/<int:id>', methods=['GET'])
  @requires_auth('get:race-details')
  def get_race_detail(payload, id):
    race = Race.query.filter(Race.id == id).\
      join(Distance, Race.distance_id == Distance.id).first() 

    if race is None:
      abort(404)

    race_deets = {'name': race.name, 'date': race.date,
                  'city': race.city, 'state': race.state,
                  'distance_name': race.distance.name,
                  'distance_km': race.distance.distance_km,
                  'distance_mi': race.distance.distance_mi,
                  'website': race.website,
                  'race_id': id, 'distance_id': race.distance.id}

    return jsonify({
      'success': True,
      'race': race_deets
    })

  @app.route('/races', methods=['POST'])
  @requires_auth('post:race')
  def submit_race(payload):
    data = request.get_json()

    #fail if distance id is bad
    if Distance.query.get(data['distance_id']) is None:
      abort(404)

    try:
      Race(
        name = data['name'],
        city = data['city'],
        state = data['state'],
        website = data['website'],
        distance_id = data['distance_id'],
        date = datetime.strptime(data['date'], '%Y-%m-%d')
      ).insert()
    except Exception as e:
      print(e)
      abort(400)

    return jsonify({
      'success': True
    })

  @app.route('/distances', methods=['POST'])
  @requires_auth('post:distance')
  def submit_distance(payload):
    data = request.get_json()
    try:
      #distance conversions
      if 'distance_km' in data:
        distance_km = data['distance_km']
      elif 'distance_mi' in data:
        distance_mi = data['distance_mi']
        distance_km = distance_mi / KM_2_MILE

      Distance(
        name = data['name'],
        distance_km = distance_km
      ).insert()
    except:
      abort(400)

    return jsonify({
      'success': True
    })

  @app.route('/races/<int:id>', methods=['PATCH'])
  @requires_auth('patch:race')
  def update_race(payload, id):
    # the only thing we should update for a race is the website,
    #  so that we can change the website to the results page
    data = request.get_json()
    if data is None:
      abort(422)

    old_race = Race.query.get(id)
    if old_race is None:
      abort(404)

    website = data.get('website', None)
    if website is not None:
      old_race.website = website
    else:
      abort(422)

    try:
      old_race.update()
      return jsonify({
        'success': True
      })
    except:
      abort(422)

  @app.route('/distances/<int:id>', methods=['PATCH'])
  @requires_auth('patch:distance')
  def update_distance(payload, id):
    data = request.get_json()
    if data is None:
      abort(422)
    name = data.get('name', None)
    distance_km = data.get('distance_km', None)
    distance_mi = data.get('distance_mi', None)
    if set([name, distance_km, distance_mi]) == {None}:
      abort(422)

    old_distance = Distance.query.get(id)
    if old_distance is None:
      abort(404)
    if name is not None:
      old_distance.name = name
    if distance_km is not None:
      old_distance.distance_km = distance_km
      old_distance.distance_mi = round(distance_km * KM_2_MILE, 2)
    elif distance_mi is not None:
      old_distance.distance_km = round(distance_mi / KM_2_MILE, 2)
      old_distance.distance_mi = distance_mi

    try:
      old_distance.update()
      return jsonify({
        'success': True
      })
    except:
      abort(422)

  @app.route('/races/<int:id>', methods=['DELETE'])
  @requires_auth('delete:race')
  def delete_race(payload, id):
    delete_me = Race.query.get(id)

    if delete_me is None:
      abort(422)
    delete_me.delete()

    # Make sure it was deleted by checking if it is still there.
    delete_me_again = Race.query.get(id)
    if delete_me_again is not None:
      abort(422)

    return jsonify({
      'success': True
    })

  @app.route('/distances/<int:id>', methods=['DELETE'])
  @requires_auth('delete:distance')
  def delete_distance(payload, id):
    delete_me = Distance.query.get(id)

    if delete_me is None:
      abort(422)
    delete_me.delete()

    # Make sure it was deleted by checking if it is still there.
    delete_me_again = Distance.query.get(id)
    if delete_me_again is not None:
      abort(422)

    return jsonify({
      'success': True
    })

  ## Error handling
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": "Unauthorized"
      }), 401


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

  return app

#app = create_app()

#db_drop_and_create_all()



## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)