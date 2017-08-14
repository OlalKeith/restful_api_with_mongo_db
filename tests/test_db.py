# run instructions: pip install nosetests
# cd /restful_api_with_mongo_db
# nosetests tests/

import unittest

from app import app
from database import TestDB

TEST_PASSWORD = "test_password123"
TEST_USER = "test_user"

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
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.db = test_db
        self.db.tasks.insert(task1)
        self.db.tasks.insert(task2)

    def tearDown(self):
        self.db.tasks.remove({})
        self.db.users.remove({})

    def test_when_task_is_updated_it_is_changed_in_db(self):
        old_task = self.db.retrieve_task_with_title('Learn Python')
        task = {'id': 2, 'done': True, 'title': 'Learn Python', 'description': 'Need to find a good Python tutorial on the web'}
        self.db.find_and_update_task(task)
        updated_task = self.db.retrieve_task_with_title('Learn Python')
        self.assertEqual(updated_task['done'], True)
        self.assertNotEqual(updated_task['done'], old_task['done'])

    def test_when_task_to_update_is_not_different_it_is_not_updated(self):
        old_task = self.db.retrieve_task_with_title('Learn Python')
        task = {'id': 2, 'done': False, 'title': 'Learn Python',
                'description': 'Need to find a good Python tutorial on the web'}
        self.db.find_and_update_task(task)
        updated_task = self.db.retrieve_task_with_id(2)
        self.assertEqual(updated_task['done'], False)
        self.assertEqual(updated_task['done'], old_task['done'])

    def test_when_many_fields_of_task_are_updated_all_fields_are_updated(self):
        task = {'id': 2, 'done': True, 'title': 'I am awesome',
                'description': 'Me hungry'}
        self.db.find_and_update_task(task)
        updated_task = self.db.retrieve_task_with_id(2)
        self.assertEqual(updated_task['done'], True)
        self.assertEqual(updated_task['title'], 'I am awesome')
        self.assertEqual(updated_task['description'], 'Me hungry')

    def test_when_task_with_invalid_id_is_tried_to_be_updated_error_is_raised(self):
        task = {'id': 6, 'done': True, 'title': 'I dont exist',
                'description': 'Oh my gosh'}
        self.assertRaises(ValueError, self.db.find_and_update_task, task)

    def test_when_task_is_deleted_it_cannot_be_found(self):
        task = {'id': 2, 'done': False, 'title': 'Learn Python',
                'description': 'Need to find a good Python tutorial on the web'}
        self.db.remove_task(task)
        self.assertEqual(self.db.tasks.count(), 1)
        self.assertEqual(self.db.retrieve_task_with_id(2), None)

    def test_when_non_existing_task_is_tried_to_be_removed_error_is_risen(self):
        task = {'id': 6, 'done': True, 'title': 'I dont exist',
                'description': 'Oh my gosh'}
        self.assertRaises(ValueError, self.db.remove_task, task)

    def test_task_is_removed_with_correct_id(self):
        self.db.remove_task_by_id(1)
        self.assertEqual(self.db.retrieve_task_with_id(1), None)
        self.assertEqual(self.db.tasks.count(), 1)

    def test_matching_hash_is_found_from_db(self):
        self.db.create_non_existing_user_to_database(TEST_USER, TEST_PASSWORD)
        self.assertTrue(self.db.check_password_hash_for_user(TEST_USER, TEST_PASSWORD))

    def test_password_does_not_match_to_hash_in_db(self):
        self.db.create_non_existing_user_to_database(TEST_USER, TEST_PASSWORD)
        self.assertFalse(self.db.check_password_hash_for_user(TEST_USER, "incorrect_password"))

    def test_single_user_is_retrieved_from_db(self):
        self.db.create_non_existing_user_to_database(TEST_USER, TEST_PASSWORD)
        user = self.db.retrieve_user_by_username(TEST_USER)
        self.assertEqual(user['username'], TEST_USER)

    def test_when_user_exists_already_it_is_not_created(self):
        self.db.create_non_existing_user_to_database(TEST_USER, TEST_PASSWORD)
        self.db.create_non_existing_user_to_database(TEST_USER, TEST_PASSWORD)
        self.assertEqual(self.db.users.count(), 1)







