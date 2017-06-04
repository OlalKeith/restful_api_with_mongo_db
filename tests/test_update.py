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
        self.db = test_db
        self.db.tasks.insert(task1)
        self.db.tasks.insert(task2)

    def tearDown(self):
        self.db.tasks.remove({})

    def test_when_task_is_updated_it_is_changed(self):
        update = '{"done":true}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                content_type='application/json',
                                headers={'Authorization': 'Basic ' + self.valid_credentials})
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_resp['task']['done'])
        task_in_db = self.db.retrieve_task_with_title('Learn Python')
        self.assertTrue(task_in_db['done'])

    def test_when_task_update_is_not_in_json_error_code_400_is_retrieved(self):
        update = '{"done": true}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 400)

    def test_when_task_update_title_is_not_string_code_error_code_400_is_retrieved(self):
        update = '{"title": 1}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                content_type='application/json',
                                headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 400)

    def test_when_task_update_description_is_not_string_code_error_code_400_is_retrieved(self):
        update = '{"description": 1}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                content_type='application/json',
                                headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 400)

    def test_when_task_update_done_is_not_bool_code_error_code_400_is_retrieved(self):
        update = '{"done": 1}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                content_type='application/json',
                                headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 400)
