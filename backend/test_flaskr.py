import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://localhost:5432/{}".format(self.database_name)

        self.new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 1,
        }

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_categories(self):
        """GET categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertIsInstance(data['categories'], dict)

    def test_retrieve_questions(self):
        """GET questions """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)

    def test_create_question(self):
        """POST question """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_question(self):
        """DELETE question """
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_search_questions(self):
        """POST search """
        res = self.client().post('/questions/search', json={'searchTerm': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)

    def test_get_questions_by_category(self):
        """GET questions by category """
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)

    def test_play_quiz(self):
        """POST play quiz """
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

    