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
        # success behavior
        result = self.client().get('/distances')
        data = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['distances']), 1)

        # failure: cannot get distances/id
        result = self.client().get('distances/1')
        data = result.get_json()
        self.assertEqual(result.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_races(self):
        # success behavior
        result = self.client().get('/races')
        data = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('past', data['races'])
        self.assertGreaterEqual(len(data['races']['past']), 1)

        # failure: cannot get races/id
        result = self.client().get('races/1')
        data = result.get_json()
        self.assertEqual(result.status_code, 405)
        self.assertFalse(data['success'])

    def test_get_race_detail(self):
        # test success behavior
        result = self.client().get('/races-detail/1')
        data = result.get_json()
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('city', data['race'])
        self.assertGreaterEqual(len(data['race']), 1)

        # test error behavior
        result = self.client().get('/races-detail/99999999')
        data = result.get_json()
        self.assertEqual(result.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_race(self):
        # length of upcoming races should be one more than before
        new_race = {
            "name": "Boston Marathon", 
            "city": "Boston", 
            "state": "MA", 
            "website": "http://registration.baa.org/cfm_Archive/iframe_ArchiveSearch.cfm",
            "distance_id": 1, 
            "date": "2008-04-21"
        }
        # get the number of past races in there
        result1 = self.client().get('/races')
        data1 = result1.get_json()
        num_past1 = len(data1['races']['past'])
        # add new race
        result_post = self.client().post('/races', json=new_race)
        data_post = result_post.get_json()
        self.assertEqual(result_post.status_code, 200)
        self.assertTrue(data_post['success'])
        # check number of past races is +1
        result2 = self.client().get('/races')
        data2 = result2.get_json()
        num_past2 = len(data2['races']['past'])
        self.assertEqual(num_past1 + 1, num_past2)

        # check for failure behavior
        new_race_bad_distance = new_race
        new_race_bad_distance['distance_id'] = 99999999
        result_bad = self.client().post('/races', json=new_race_bad_distance)
        data_bad = result_bad.get_json()
        self.assertEqual(result_bad.status_code, 404)
        self.assertFalse(data_bad['success'])

    def test_add_distance(self):
        # distance with km specified
        dist_10k = {
            "name": "10K",
            "distance_km" : 10.0
        }
        # distance with mi specified
        dist_5mi = {
            "name": "5 Miler",
            "distance_mi": 5.0
        }
        # check how many distances are in database
        result1 = self.client().get('/distances')
        data1 = result1.get_json()
        num_dists = len(data1["distances"])
        # add 10k
        res10 = self.client().post('/distances', json=dist_10k)
        data10 = res10.get_json()
        self.assertEqual(res10.status_code, 200)
        self.assertTrue(data10['success'])
        # add 5-miler
        res5m = self.client().post('/distances', json=dist_5mi)
        data5m = res5m.get_json()
        self.assertEqual(res5m.status_code, 200)
        self.assertTrue(data5m['success'])
        # check if there are two more distances in db
        result2 = self.client().get('distances')
        data2 = result2.get_json()
        num_dists2 = len(data2['distances'])
        self.assertEqual(num_dists + 2, num_dists2)

        # check failure mode
        will_fail = {'bad_name': 'will_fail'}
        result_fail = self.client().post('/distances', json=will_fail)
        self.assertEqual(result_fail.status_code, 400)
        self.assertFalse(result_fail.get_json()['success'])

    def test_update_race(self):
        pass

    def test_update_distance(self):
        pass

    def test_delete_race(self):
        pass

    def test_delete_distance(self):
        pass











# Make the tests executable
if __name__ == "__main__":
    unittest.main()
