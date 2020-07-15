import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .models import db_drop_and_create_all, setup_db, Race, Distance

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

db_drop_and_create_all()

@app.route('/')
def index():
  return render_template('pages/index.html', data=[{
    'name': 'MTC Marathon', 'distance_name': 'Marathon', 'date': '5 Oct 2020',
    'website': 'https://www.tcmevents.org/'
  }, {
    'name': 'Riverbank Run', 'distance_name': '25K', 'date': '20 Oct 2020',
    'website': 'https://amwayriverbankrun.com/'
  }, {
    'name': 'Bloomsday', 'distance_name': '12K', 'date': '20 Sept 2020',
    'website': 'https://www.bloomsdayrun.org/'
  }])


## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)