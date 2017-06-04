from pymongo import MongoClient
from pymongo import errors
import app


class DatabaseHelper(object):
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.production
            self.tasks = self.db.tasks
            self.users = self.db.users
            self.bcrypt = app.bcrypt
        except errors.ServerSelectionTimeoutError as err:
            print(err)

    def retrieve_tasks(self):
        return self.tasks.find({}, {'_id': 0})

    def retrieve_task_with_title(self, title):
        return self.tasks.find_one({'title': title}, {'_id': 0})

    def retrieve_task_with_id(self, id_):
        return self.tasks.find_one({'id': id_}, {'_id': 0})

    def find_and_update_task(self, task):
        id_ = task['id']
        tasks = self.retrieve_tasks()
        try:
            task_to_change = next(task for task in tasks if task['id'] == id_)
            self._update_task(id_, task, task_to_change)
        except:
            raise ValueError("Task was not updated")

    def _update_task(self, id_, task, task_to_change):
        for key, value in task_to_change.items():
            for k, new_value in task.items():
                if key == k and value != new_value:
                    self.tasks.update({'id': id_}, {'$set': {key: new_value}})

    def remove_task(self, task):
        id_ = task['id']
        task_to_remove = self.retrieve_task_with_id(id_)
        if task_to_remove == task:
            self.tasks.remove({'id': id_})
        else:
            raise ValueError("Task was not found!")

    def remove_task_by_id(self, id_):
        self.tasks.remove({'id': id_})

    def add_task_to_db(self, task):
        self.tasks.insert_one(task)

    def insert_user_to_db(self, user_info):
        self.users.insert_one(user_info)

    def retrieve_users(self):
        return self.users.find({}, {'_id': 0})

    def retrieve_user_by_username(self, username):
        return self.users.find_one({'username': username}, {'_id': 0})

    def create_non_existing_user_to_database(self, username, password):
        hash_ = self.bcrypt.generate_password_hash(password, 12).decode('utf-8')
        user_info = {'username': username, 'hash': hash_}
        user = self.retrieve_user_by_username(username)
        if not user:
            self.insert_user_to_db(user_info)

    def check_password_hash_for_user(self, username, password):
        try:
            user = next(user for user in self.users.find({}) if user['username'] == username)
            return self.bcrypt.check_password_hash(user['hash'], password)
        except StopIteration:
            return False


class TestDB(DatabaseHelper):
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.test
            self.tasks = self.db.tasks
            self.users = self.db.users
            self.bcrypt = app.bcrypt
        except errors.ServerSelectionTimeoutError as err:
            print(err)

    def create_test_users_to_test_db(self):
        self.create_non_existing_user_to_database('mojo', 'python')
        self.create_non_existing_user_to_database('kojo', 'python')

    def remove_test_users_from_db(self):
        self.users.remove({})


if __name__ == "__main__":
    database = DatabaseHelper()
