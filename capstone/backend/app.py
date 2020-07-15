import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()

@app.route('/')
def index():
  return render_template('pages/index.html', data=[{
    'name': 'MTC Marathon', 'distance_name': 'Marathon', 'date': '5 Oct 2020'
  }, {
    'name': 'Riverbank Run', 'distance_name': '25K', 'date': '20 Oct 2020'
  }, {
    'name': 'Bloomsday', 'distance_name': '12K', 'date': '20 Sept 2020' 
  }])


## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)