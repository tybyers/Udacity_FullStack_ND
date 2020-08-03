import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models import setup_db, Race, Distance

# prior to running these tests, please `cp working/database_default.db test_database.db`
#  from the same directory as these tests. Otherwise, they may fail due to the
#  delete step
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

        # test failure behavior
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
        new_site = "http://www.newsite.com"
        race_id = 1
        # what's website for current race_id?
        cur_site = self.client().get('/races-detail/{}'.format(race_id))
        cur_site = cur_site.get_json()['race']['website']
        self.assertNotEqual(new_site, cur_site)
        # update the site
        upd_site = self.client().patch('/races/{}'.format(race_id), 
            json={'website': new_site})
        self.assertEqual(upd_site.status_code, 200)
        self.assertTrue(upd_site.get_json()['success'])
        # did we change it?
        changed_site = self.client().get('/races-detail/{}'.format(race_id)).get_json()['race']['website']
        self.assertEqual(new_site, changed_site)
        # change it back
        upd_site = self.client().patch('/races/{}'.format(race_id), 
            json={'website': cur_site})
        self.assertEqual(upd_site.status_code, 200)
        self.assertTrue(upd_site.get_json()['success'])
        # verify changed it back
        changed_back = self.client().get('/races-detail/{}'.format(race_id)).get_json()['race']['website']
        self.assertEqual(cur_site, changed_back)

        # check failure mode 1: no "website" in json
        no_web = self.client().patch('/races/1', json={'DWEEBSITE': 'type'})
        self.assertEqual(no_web.status_code, 422)
        self.assertFalse(no_web.get_json()['success'])

        # check failure mode 2: no race at ID
        norace = self.client().patch('/races/99999999', json={})
        self.assertEqual(norace.status_code, 404)
        self.assertFalse(norace.get_json()['success'])

    def test_update_distance(self):
        # get the maximum ID
        dist_id = str(max([int(id) for id in self.client().get('/distances').get_json()['distances'].keys()]))
        dist_km = 200
        new_dist = self.client().patch('/distances/{}'.format(dist_id), 
                    json={'name': 'Ultramarathon','distance_km': dist_km})
        self.assertEqual(new_dist.status_code, 200)
        self.assertTrue(new_dist.get_json()['success'])
        # get distances and see if has been changed
        dist_dict = self.client().get('/distances').get_json()['distances'][dist_id]
        self.assertEqual(dist_dict['name'], 'Ultramarathon')
        self.assertEqual(dist_dict['distance_km'], dist_km)
        # assure the distance param is nearly correct for km -> mi conversion
        self.assertLess(dist_dict['distance_km'] * 0.62 - dist_dict['distance_mi'] , 1)
        self.assertGreater(dist_dict['distance_km'] * 0.62 - dist_dict['distance_mi'] , -1)

        # check failure mode 1: no distance params sent
        no_dist = self.client().patch('/distances/1', json={'furlongs': 2})
        self.assertEqual(no_dist.status_code, 422)
        self.assertFalse(no_dist.get_json()['success'])

        # check failure mode 2: no distance at ID
        no_dist = self.client().patch('/distances/99999999', json={})
        self.assertEqual(no_dist.status_code, 422)
        self.assertFalse(no_dist.get_json()['success'])

    def test_delete_race(self):
        # get max race id and pop off the top of that (since we created a past race above)
        race_id = str(max([int(id) for id in self.client().get('/races').get_json()['races']['past'].keys()]))
        #print('max race_id: {}'.format(race_id))
        deleted = self.client().delete('/races/{}'.format(race_id))
        self.assertEqual(deleted.status_code, 200)
        self.assertTrue(deleted.get_json()['success'])
        
        # check to see if race_id still is there
        self.assertNotIn(race_id, self.client().get('/races').get_json()['races']['past'].keys())

        # check failure mode
        too_high = self.client().delete('/races/9999999999')
        self.assertEqual(too_high.status_code, 422)
        self.assertFalse(too_high.get_json()['success'])

    def test_delete_distance(self):
        # get max distance id and pop off the top of that (since we created a distance above)
        dist_id = str(max([int(id) for id in self.client().get('/distances').get_json()['distances'].keys()]))
        deleted = self.client().delete('/distances/{}'.format(dist_id))
        self.assertEqual(deleted.status_code, 200)
        self.assertTrue(deleted.get_json()['success'])

         # check to see if dist_id still is there
        self.assertNotIn(dist_id, self.client().get('/distances').get_json()['distances'].keys())
        
        # check failure mode
        too_high = self.client().delete('/distances/9999999999')
        self.assertEqual(too_high.status_code, 422)
        self.assertFalse(too_high.get_json()['success'])

    def test_auth(self):
        ## TODO!!!
        pass


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
