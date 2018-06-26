import json
import os
import uuid

import requests
import unittest2

import seatsio

BASE_URL = "https://api-staging.seatsio.net"


class SeatsioClientTest(unittest2.TestCase):

    def setUp(self):
        super(SeatsioClientTest, self).setUp()
        self.user = self.create_test_user()
        self.client = seatsio.Client(self.user["secretKey"], BASE_URL)

    def tearDown(self):
        super(SeatsioClientTest, self).tearDown()

    def newClient(self, secret_key):
        return seatsio.Client(secret_key, BASE_URL)

    def create_test_user(self):
        response = requests.post(
            BASE_URL + "/system/public/users",
            data=json.dumps({
                "email": "test" + str(uuid.uuid4()) + "@seats.io",
                "password": "12345678"
            })
        )
        if response.ok:
            return response.json()
        else:
            raise Exception("Failed to create a test user")

    def create_test_chart(self):
        return self.create_test_chart_from_file('sampleChart.json')

    def create_test_chart_with_sections(self):
        return self.create_test_chart_from_file('sampleChartWithSections.json')

    def create_test_chart_from_file(self, file):
        with open(os.path.join(os.path.dirname(__file__), file), 'r') as test_chart_json:
            data = test_chart_json.read().replace('\n', '')
            chart_key = str(uuid.uuid4())
            url = BASE_URL + "/system/public/" + self.user["designerKey"] + "/charts/" + chart_key
            response = requests.post(
                url=url,
                headers={"Accept": "application/json"},
                data=data
            )
            if response.status_code == 201:
                return chart_key
            else:
                raise Exception("Failed to create a test user")