import unittest, sys, os, tempfile

class DataTests(unittest.TestCase):
    """ Data cleaning and formatting """    
    # Manually tests the correctness of some rows in the master log data.
    def test_log_data_correctness(self):
        self.assertEqual(foo, bar)

    # Manually tests the correctness of some rows in the ground truth data.
    def test_ground_truth_data_correctness(self):
        pass

    # Manually tests the correctness of some rows in the timetable data. 
    def test_timetable_data_correctness(self):
        pass

class DataBaseTests(unittest.TestCase):
    """ Database """
    def SetUp(selfself):
        self.db_fd, theApp.app.config['DATABASE'] = tempfile.msktemp()
        theApp.app.config['TESTING'] = True
        self.app = theApp.app.test_client()
        with theApp.app.app_context():
            theApp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(theApp.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data


if __name__ == "__main__":
    unittest.main()

