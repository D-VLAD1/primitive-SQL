import unittest
import requests


BASE_URL = 'http://0.0.0.0:8000'
HEALTH = f'{BASE_URL}/health'
CREATE_DATABASE = f'{BASE_URL}/create-database'
CREATE_TABLE = f'{BASE_URL}/create-table'
CREATE_NOTE = f'{BASE_URL}/create-note'
DELETE_TABLE = f'{BASE_URL}/delete-table'
DELETE_NOTE = f'{BASE_URL}/delete-note'
SAVE_TREE = f'{BASE_URL}/save-tree-json'
UPLOAD_TREE = f'{BASE_URL}/upload-tree-json'



class TestDB(unittest.TestCase):
    def test_health(self):
        response = requests.get(HEALTH)
        response.raise_for_status()
        self.assertEqual(response.json(), {'status': 200})

    def test_flow(self):
        # test create database
        response = requests.post(CREATE_DATABASE, json={})
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {})

        # test create table
        response = requests.post(CREATE_TABLE, json={
            "database": db,
            "new_table_name": "notes",
            "attrs": ["name", "email"]
        })
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {'key': 'notes', 'value': {}, 'left': {}, 'right': {}, 'attrs': ['name', 'email']})


        # test create note
        response = requests.post(CREATE_NOTE, json={
            "database": db,
            "table_name": "notes",
            "new_note_name": "note1",
            "note_content": {"name": "Hello", "email": "World"}
        })
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {'key': 'notes', 'value': {'key': 'note1', 'value': {'name': 'Hello', 'email': 'World'}, 'left': {}, 'right': {}}, 'left': {}, 'right': {}, 'attrs': ['name', 'email']})


        # test delete note
        response = requests.post(DELETE_NOTE, json={
            "database": db,
            "table_name": "notes",
            "note_name": "note1",
        })
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {'key': 'notes', 'value': {}, 'left': {}, 'right': {}, 'attrs': ['name', 'email']})


        # test delete table
        response = requests.post(DELETE_TABLE, json={
            "database": db,
            "table_name": "notes"
        })
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {})

        # test save tree in json
        response = requests.post(SAVE_TREE, json={
            "database": db,
            "filename": "db.json"
        })
        response.raise_for_status()

        filename = response.json()
        self.assertEqual(filename, {'filename': 'db.json'})

        # test upload tree from json (filename="db.json")
        response = requests.post(UPLOAD_TREE, json=filename)
        response.raise_for_status()

        db = response.json()['database']
        self.assertEqual(db, {})


if __name__ == "__main__":
    unittest.main()