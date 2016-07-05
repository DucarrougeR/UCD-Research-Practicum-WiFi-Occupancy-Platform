import unittest, sys, os, tempfile
from app.mod_db.QueryBuilder import QueryBuilder

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

    def query_select_test(self):
        query = QueryBuilder().select('sample').get_query()
        assert query == 'SELECT * FROM sample'

    def query_select_test_with_params(self):
        query = QueryBuilder().select('sample', ['id']).get_query()
        assert query == 'SELECT id FROM sample'

    def query_join_test(self):
        query = QueryBuilder().select('sample').join('sample2', 'field1', '=', 'field2').get_query()
        assert query == 'SELECT * FROM sample JOIN sample2 ON field1 = field2'

    def query_where_test(self):
        query = QueryBuilder().select('sample', ['id']).where('id', '=', 1234).get_query()

        assert query == 'SELECT id FROM sample WHERE id = 1234'

if __name__ == "__main__":
    unittest.main()

