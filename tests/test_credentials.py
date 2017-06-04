# run instructions: pip install nosetests
# cd /restful_api_with_mongo_db
# nosetests tests/

from app import app
import unittest
import base64
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


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_db.create_test_users_to_test_db()
        test_db.tasks.insert(task1)
        test_db.tasks.insert(task2)

    @classmethod
    def tearDownClass(cls):
        test_db.remove_test_users_from_db()
        test_db.tasks.remove({})

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.valid_credentials = base64.b64encode(b'mojo:python').decode('utf-8')
        self.invalid_password = base64.b64encode(b'fake:python').decode('utf-8')
        self.invalid_username = base64.b64encode(b'mojo:fake').decode('utf-8')
        self.new_task = '{"title":"Read a book"}'

    def test_task_2_can_be_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/2', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')

    def test_when_invalid_password_is_entered_task_2_is_not_retrieved(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/2', headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status, '403 FORBIDDEN')

    def test_when_invalid_username_is_entered_task_2_is_not_retrieved(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/2', headers={'Authorization': 'Basic ' + self.invalid_username})
        self.assertEqual(response.status, '403 FORBIDDEN')

    def test_all_tasks_are_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            'todo/api/v1.0/tasks', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')

    def test_when_invalid_password_is_entered_tasks_are_not_retrieved(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks', headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status, '403 FORBIDDEN')

    def test_when_invalid_username_is_entered_tasks_are_not_retrieved(self):
        response = self.app.get(
            '/todo/api/v1.0/tasks/2', headers={'Authorization': 'Basic ' + self.invalid_username})
        self.assertEqual(response.status, '403 FORBIDDEN')

    def test_when_new_task_is_created_without_credentials_status_code_is_403(self):
        response = self.app.post('todo/api/v1.0/tasks',
                                 data=self.new_task,
                                 content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_when_new_task_is_created_with_wrong_credentials_status_code_is_403(self):
        response = self.app.post('todo/api/v1.0/tasks',
                                 data=self.new_task,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status_code, 403)

    def test_when_task_is_updated_with_wrong_password_status_code_is_403(self):
        update = '{"done":true}'
        response = self.app.put('todo/api/v1.0/tasks/2',
                                data=update,
                                content_type='application/json',
                                headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status_code, 403)

    def test_when_task_is_deleted_with_invalid_credentials_status_code_is_403(self):
        response = self.app.delete('todo/api/v1.0/tasks/2',
                                   content_type='application/json',
                                   headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status_code, 403)