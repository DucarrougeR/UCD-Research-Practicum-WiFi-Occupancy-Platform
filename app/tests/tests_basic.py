import unittest, sys, os, tempfile, sqlite3
from app.mod_db.QueryBuilder import QueryBuilder
from app.mod_db import theApp
import pandas as pd

class DataIntegrityTests(unittest.TestCase):
    # Creates a SQL connection to our SQLite database.
    con = sqlite3.connect("../mod_db/database.db")

    df = pd.read_sql_query("SELECT * from counts", con)

    # Manually tests the correctness of some rows in the log and ground truth data.
    def test_counts_integrity(self):
        df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Fri Nov 13 12:25:21' AND counts_room_number == 'B003'", con)    
        self.assertEqual(df["counts_associated"], 27.0)
        self.assertEqual(df["counts_truth"], 22.5)
        
        df = pd.read_sql_query("SELECT * from counts WHERE counts_time =='Tue Nov 03 11:50:25' AND counts_room_number == 'B003'", con)    
        self.assertEqual(df["counts_associated"], 71.0)
        self.assertEqual(df["counts_truth"], 67.5)

    # Manually tests the correctness of some rows in the timetable data.
    def test_timetable_integrity(self):
        #df = pd.read_sql_query("SELECT * from classes WHERE classes_time =='Tue Nov 03 14:00:00' AND classes_room =='B004'", con)  
        pass

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
