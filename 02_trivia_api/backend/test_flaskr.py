import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    new_question = {
            'question': 'What is the square root of 4?',
            'answer': '2',
            'category': 1,
            'difficulty': 1
    }

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_questions'], 0)
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(len(data['categories']), 0)

    def test_delete_question(self):

        # pop off the top question
        q_res = self.client().get('/questions')
        q_data = q_res.get_json()
        questions = q_data['questions']
        before_len = q_data['total_questions']
        delete_id = questions[0]['id']

        res = self.client().delete('/questions/{}'.format(delete_id))
        data = res.get_json()

        question = Question.query.filter(Question.id == delete_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

        # Is the length of questions really one less? Did we delete ok?
        q_res_after = self.client().get('/questions')
        q_data_after = q_res_after.get_json()
        
        self.assertEqual(before_len - 1, q_data_after['total_questions'])
        
    def test_submit_question(self):
        # get the *before* length
        before_res = self.client().get('/questions')
        before_data = before_res.get_json()
        before_len = before_data['total_questions']

        # add a new question
        res = self.client().post('/questions', json=self.new_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        # check the number of questions is one more than before
        after_res = self.client().get('/questions')
        after_data = after_res.get_json()
        after_len = after_data['total_questions']

        self.assertEqual(before_len + 1, after_len)

    def test_search_question(self):
        search_term = 'a'
        res = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'] > 0)

    def test_get_question_by_category(self):
        category_id = 1
        url = '/categories/{}/questions'.format(category_id)
        res = self.client().get(url)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'] > 0)
    
    def test_quiz(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 0, 'type': None}})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['question']), 5)

    # test error handlers
    def test_400_bad_page_request(self):
        bad_question = {'question': 'bad question', 'invalid': 'whaaaa'}
        res = self.client().post('/questions', json=bad_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=100000000')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Cannot find resource')

    def test_405_question_creation_unallowed(self):
        # attempt to add a new question
        res = self.client().post('/questions/1412531', json=self.new_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_422_bad_delete(self):
        res = self.client().delete('/questions/92450')
        data = res.get_json()  

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Cannot process')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()