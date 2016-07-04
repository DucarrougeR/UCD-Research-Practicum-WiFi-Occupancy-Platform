import os
# import theApp
import unittest
import tempfile

class AppTest(unittest.TestCase):

    def SetUp(selfself):
        self.db_fd, theApp.app.config['DATABASE'] = tempfile.msktemp()
        theApp.app.config['TESTING'] = True
        self.app = theApp.app.test_client()
        with theApp.app.app_context():
            theApp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(theApp.app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()