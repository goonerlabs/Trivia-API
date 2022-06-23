import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true

from flaskr import create_app
from models import setup_db, Question, Category




class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:@{}/{}".format('postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question' : 'Who scored the last goal in the 2011 champions league final?',
            'answer' : 'David Villa',
            'difficulty' : 2,
            'category' : 6
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_405_delete_all_categories_not_allowed(self):
        res = self.client().delete('/api/v1.0/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_paginated_questions(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/api/v1.0/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # def test_delete_question(self):
    #     res = self.client().delete('/api/v1.0/questions/2')
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertEqual(question, None)

    def test_404_question_to_delete_does_not_exist(self):
        res = self.client().delete('/api/v1.0/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_new_question(self):
        res = self.client().post('/api/v1.0/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_bad_request_creating_question(self):
        res = self.client().post('/api/v1.0/questions/10', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_get_question_search_with_results(self):
        res = self.client().post('/api/v1.0/questions', json={'searchTerm' : 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))

    def test_get_question_search_with_no_results(self):
        res = self.client().post('/api/v1.0/questions', json={'searchTerm' : 'xhdbhjbeddvbqvbhbwd'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['totalQuestions'], 0)

    def test_get_questions_by_category(self):
        res = self.client().get('/api/v1.0/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_category_id_does_not_exist(self):
        res = self.client().get('/api/v1.0/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_question(self):
        res = self.client().post('/api/v1.0/quizzes', json={
            'previous_questions' : [],
            'quiz_category' : {'id': '6', 'type' : 'Sports'}
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_not_enough_info_to_process(self):
        res = self.client().post('/api/v1.0/quizzes', json={'previous_questions' : []})

        data= json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()