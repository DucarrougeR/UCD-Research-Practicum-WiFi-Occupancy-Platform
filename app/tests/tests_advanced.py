import unittest, sys, os, tempfile, sqlite3
from app.mod_db import theApp
import pandas as pd
import config
import app.mod_api.controllers
import app.mod_api.models
from app import app as flask_app
import json
import json

class FlaskAdvancedTests(unittest.TestCase):
    def check_room_route_api_test(self):
        # @mod_api.route('/room/occupancy/<room>/<time>')
        """ will check if an api route is working correctly """
        tester = flask_app.test_client(self)
        response = tester.get('/api/room/occupancy/B003/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        for result in data["results"]:
            self.assertEqual(result["counts_room_number"], "B003")

    def check_room_time_route_api_test(self):
        # @mod_api.route('/room/occupancy/<room>/<time>')
        """ will check if an api route is working correctly """
        tester = flask_app.test_client(self)
        response = tester.get('/api/room/occupancy/B003/Tue%20Nov%2003%202015')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        for result in data["results"]:
            self.assertEqual(result["counts_time"][4:10], "Nov 03")
            self.assertEqual(result["counts_room_number"], "B003")