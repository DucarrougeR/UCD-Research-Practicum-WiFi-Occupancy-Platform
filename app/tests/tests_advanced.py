import unittest, sys, os, tempfile, sqlite3
from app import app as flask_app
import json
import json

class FlaskAdvancedTests(unittest.TestCase):
    def check_room_route_api_test(self):
        # @mod_api.route('/room/occupancy/<room>/<time>/<type>')
        """ will check if an api route is working correctly """
        tester = flask_app.test_client(self)
        response = tester.get('/api/room/occupancy/B003/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        for result in data["results"]:
            self.assertEqual(result["counts_room_number"], "B003")

    def check_room_time_route_api_test(self):
        # @mod_api.route('/room/occupancy/<room>/<time>/<type>')
        """ will check if an api route is working correctly """
        tester = flask_app.test_client(self)
        response = tester.get('/api/room/occupancy/B003/Tue%20Nov%2003%202015/continuous')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        for result in data["results"]:
            self.assertEqual(result["counts_time"][4:10], "Nov 03")
            self.assertEqual(result["counts_room_number"], "B003")

    def check_home_route_test(self):
        tester = flask_app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def check_static_css_route_test(self):
        tester = flask_app.test_client(self)
        # check for scss file because css file won't be compiled on the server
        response = tester.get('/static/scss/main.scss')
        self.assertEqual(response.status_code, 200)



    # login helpers
    def login(self, username, password, tester):

        return tester.post('/api/auth/login', data=json.dumps(dict(
            email=username,
            password=password
        )), follow_redirects=True)

    def logout(self, tester):
        tester = flask_app.test_client(self)
        return tester.get('/api/auth/logout', follow_redirects=True)

    def check_login_logout_test(self):
        tester = flask_app.test_client(self)
        rv = self.login('admin@admin.com', 'password', tester)
        self.assertEqual(rv.status_code, 200)

    def check_rooms_list_route_test(self):
        tester = flask_app.test_client(self)
        response = tester.get('/api/rooms/list')
        self.assertEqual(response.status_code, 200)

