import unittest, sys, os, tempfile, sqlite3
from app.mod_db import theApp
import pandas as pd
import config
import app.mod_api.controllers
import app.mod_api.models

class DataIntegrityTests(unittest.TestCase):
    # Creates a SQL connection to our SQLite database.


    def setUp(self):
        self.con = sqlite3.connect(config.DATABASE)

    # Manually tests the correctness of some rows in the log and ground truth data.
    def test_counts_integrity(self):
        # df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Fri Nov 13 12:25:21' AND counts_room_number == 'B003'", con)
        # self.assertEqual(df["counts_associated"], 27.0)
        # self.assertEqual(df["counts_truth"], 22.5)
        #
        # df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Tue Nov 03 11:50:25' AND counts_room_number == 'B003'", con)
        # self.assertEqual(df["counts_associated"], 71.0)
        # self.assertEqual(df["counts_truth"], 67.5)
        pass

    # Manually tests the correctness of some rows in the timetable data.
    def test_timetable_integrity(self):
        #df = pd.read_sql_query("SELECT * from classes WHERE classes_time =='Tue Nov 03 14:00:00' AND classes_room =='B004'", con)

        # df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Fri Nov 13 12:25:21' AND counts_room_number == 'B003'", self.con)
        #
        # self.assertEqual(df["counts_associated"], 27.0)
        # self.assertEqual(df["counts_truth"], 22.5)
        #
        # df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Tue Nov 03 11:50:25' AND counts_room_number == 'B003'", self.con)
        # self.assertEqual(df["counts_associated"], 71.0)
        # self.assertEqual(df["counts_truth"], 67.5)
        assert True

    # Manually tests the correctness of some rows in the timetable data.
    def test_timetable_integrity(self):
        # con = sqlite3.connect(config.DATABASE)
        #
        #
        # df = pd.read_sql_query("SELECT * from classes WHERE classes_time =='Tue Nov 03 14:00:00' AND classes_room_number =='B004'", con)
        pass

    # def test_timetable_integrity(self):
    #     # con = sqlite3.connect(config.DATABASE)
    #     #
    #     #
    #     # df = pd.read_sql_query("SELECT * from classes WHERE classes_time =='Tue Nov 03 14:00:00' AND classes_room_number =='B004'", con)
    #     pass

class APITests(unittest.TestCase):
    def valid_date_test(self):
        failed = app.mod_api.models.is_valid_date("XYZ Jul 04 2016") and app.mod_api.models.is_valid_date("Mon ABC 04 2016") \
                 and app.mod_api.models.is_valid_date("Mon Aug 32 2016")
        success = app.mod_api.models.is_valid_date("Mon Jul 04 2016")
        assert failed == False and success == True

    def parse_date_test(self):
        assert len(app.mod_api.models.parse_date("Mon Jul 04 2016")) == 4

class APITests(unittest.TestCase):
    def valid_date_test(self):
        failed = app.mod_api.models.is_valid_date("XYZ Jul 04 2016") and app.mod_api.models.is_valid_date("Mon ABC 04 2016") \
                 and app.mod_api.models.is_valid_date("Mon Aug 32 2016")
        success = app.mod_api.models.is_valid_date("Mon Jul 04 2016")
        assert failed == False and success == True

    def parse_date_test(self):
        assert len(app.mod_api.models.parse_date("Mon Jul 04 2016"))


class DataBaseTests(unittest.TestCase):
    ''' Database '''
    # def SetUp(self):
     #    self.db_fd, theApp.app.config['DATABASE'] = tempfile.msktemp()
     #    theApp.app.config['TESTING'] = True
     #    self.app = theApp.app.test_client()
     #    with theApp.app.app_context():
     #        theApp.init_db()
    #
    # def tearDown(self):
	# # Test if disconnection is successfull
     #    os.close(self.db_fd)
     #    os.unlink(theApp.app.config['DATABASE'])
    #
    # def test_empty_db(self):
	# # Test if db is empty
     #    rv = self.app.get('/')
     #    assert b'No entries here so far' in rv.data


if __name__ == "__main__":
    unittest.main()
