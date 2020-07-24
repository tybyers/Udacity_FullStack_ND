import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models import setup_db, Race, Distance

class RacesTestCase(unittest.TestCase):
    """This class tests the api for Distances and Races"""

    def setUp(self):
        """Initialize app and define the test variables"""
        self.app = create_app()
        self.client = self.app.test_client
        self.db_filename = "test_database.db"
        proj_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(proj_dir, self.db_filename))
        setup_db(self.app, self.database_path)

        # bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_distances(self):
        result = self.client().get('/distances')
        data = result.get_json()
        print('HEADS UP DATA: {}'.format(data))

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['distances']), 1)


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
