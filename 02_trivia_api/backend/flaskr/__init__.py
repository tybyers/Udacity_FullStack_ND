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
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
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
      abort(404)

    delete_me.delete()

    #still there?
    delete_me_again = Question.query.get(question_id)
    if delete_me_again is not None:
      abort(404)

    return jsonify({
      'success': True
    })

  @app.route('/questions', methods=['POST'])
  def submit_question():#question, answer, difficulty, category):

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
      abort(404)

    return jsonify({
      'success': True
    })
  
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    term = request.get_json().get('searchTerm', None)
    q_list = Question.query.filter(Question.question.ilike('%{}%'.format(term))).all()
    paginated_questions = paginate_questions(request, q_list)

    categories = {c.id: c.type for c in Category.query.all()}

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(q_list),
      'categories': categories
    })
    

  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    q_list = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    paginated_questions = paginate_questions(request, q_list)

    #cat_name = Category.query.get(category_id).type

    if len(paginated_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(q_list),
      'currentCategory': category_id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    