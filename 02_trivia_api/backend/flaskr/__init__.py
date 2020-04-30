import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

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

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()

    cat_list = {cat.id: cat.type for cat in categories}

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': cat_list
    })

  @app.route('/questions', methods=['GET'])
  def get_questions():
    q_list = Question.query.order_by(Question.id).all()
    paginated_questions = paginate_questions(request, q_list)

    categories = {c.id: c.type for c in Category.query.all()}

    if len(paginated_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(q_list),
      'categories': categories
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    delete_me = Question.query.get(question_id)

    if delete_me is None:
      abort(422)
    delete_me.delete()

    # Make sure it was deleted by checking if it is still there.
    delete_me_again = Question.query.get(question_id)
    if delete_me_again is not None:
      abort(422)

    return jsonify({
      'success': True
    })

  @app.route('/questions', methods=['POST'])
  def submit_question():

    data = request.get_json()
    print('Category: {}'.format(data['category']))
    try:
      Question(
        question = data['question'],
        answer = data['answer'],
        category = data['category'],
        difficulty = data['difficulty']
      ).insert()
    except:
      abort(422)

    return jsonify({
      'success': True
    })
  
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    term = request.get_json().get('searchTerm', None)
    try: 
      q_list = Question.query.filter(Question.question.ilike('%{}%'.format(term))).all()
      paginated_questions = paginate_questions(request, q_list)

      categories = {c.id: c.type for c in Category.query.all()}

      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(q_list),
        'categories': categories
      })
    except:
      abort(404)
    

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      q_list = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
      paginated_questions = paginate_questions(request, q_list)

      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(q_list),
        'current_category': category_id
      })
    except:
      abort(404)

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    category = request.get_json().get('quiz_category', 0)
    prev_qs = request.get_json().get('previous_questions', [])

    try:
      if category['id'] == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == category['id']).all()
        
      pick_from_questions = []
      for q in questions:
        q_format = q.format()
        if q_format['id'] not in prev_qs:
          pick_from_questions.append(q_format)

      if len(pick_from_questions) == 0:
        cur_question = False
      else:
        cur_question = random.choice(pick_from_questions)
        prev_qs.append(cur_question)

      return jsonify({
        "success": True,
        "question": cur_question
      })
    except:
      abort(404)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Cannot find resource"
    }), 404
  
  return app

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Cannot process"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed"
    }), 405
  
  return app

    