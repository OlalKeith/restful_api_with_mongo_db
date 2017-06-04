# run instructions: pip install nosetests
# cd /restful_api_with_mongo_db
# nosetests tests/

import unittest
import base64
import json

from app import app
from database import TestDB

task1 = {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    }
task2 = {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }

test_db = TestDB()


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_db.create_test_users_to_test_db()

    @classmethod
    def tearDownClass(cls):
        test_db.remove_test_users_from_db()

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.valid_credentials = base64.b64encode(b'mojo:python').decode('utf-8')
        self.invalid_credentials = base64.b64encode(b'hopo:python').decode('utf-8')  #invalid username
        self.new_task = '{"title":"Read a book"}'
        self.db = test_db
        self.db.tasks.insert(task1)
        self.db.tasks.insert(task2)

    def tearDown(self):
        self.db.tasks.remove({})

    def test_check_task_2_is_not_done(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/2', headers={'Authorization': 'Basic ' + self.valid_credentials})
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertFalse(json_resp['task']['done'])

    def test_when_new_task_is_created_status_code_is_201(self):
        response = self.app.post('/todo/api/v1.0/tasks',
                                 data=self.new_task,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.db.tasks.count(), 3)

    def test_when_new_task_is_created_it_can_be_retrieved(self):
        response = self.app.post('/todo/api/v1.0/tasks',
                                 data=self.new_task,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.valid_credentials})
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_resp['task']['title'], 'Read a book')
        self.assertEqual(self.db.tasks.count(), 3)

    def test_when_non_existing_task_is_requested_status_code_is_404(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/5', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 404)

    def test_when_task_is_deleted_it_cannot_be_found(self):
        self.app.delete(
            '/todo/api/v1.0/tasks/1', headers={'Authorization': 'Basic ' + self.valid_credentials})
        response = self.app.get(
            '/todo/api/v1.0/tasks/1', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.db.retrieve_task_with_id(1), None)
        self.assertEqual(self.db.tasks.count(), 1)

    def test_when_new_task_is_created_without_title_status_code_is_400(self):
        task = '{"description":"fake_news"}'
        response = self.app.post('/todo/api/v1.0/tasks',
                                 data=task,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.db.tasks.count(), 2)

if __name__ == '__main__':
    unittest.main()
