from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.exceptions import BadRequest

URL = reverse('cats_list')


class Tests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        with connection.cursor() as cursor:
            with open('api/testing/wg_forge_init.sql') as sql:
                cursor.execute(sql.read())

    def test_data_return(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 27)

    def test_asc_ordering(self):
        response = self.client.get(URL, {'order_by': 'name'})
        self.assertEqual(response.data[0]['name'], 'Amur')
        self.assertEqual(response.data[-1]['name'], 'Yasha')

    def test_desc_ordering(self):
        response = self.client.get(URL, {'order_by': '-tail_length'})
        self.assertEqual(response.data[0]['name'], 'Kelly')
        self.assertEqual(response.data[-1]['name'], 'Asya')

    def test_ordering_by_wrong_column(self):
        self.client.get(URL, {'order_by': 'wrong_column'})
        self.assertRaises(BadRequest)

    def test_limit(self):
        response = self.client.get(URL, {'limit': 10})
        self.assertEqual(len(response.data), 10)

    def test_invalid_limit(self):
        self.client.get(URL, {'limit': 'string'})
        self.assertRaisesMessage(BadRequest, 'invalid')

    def test_negative_limit(self):
        self.client.get(URL, {'limit': -10})
        self.assertRaisesMessage(BadRequest, 'negative')

    def test_offset(self):
        response = self.client.get(
            URL, {'order_by': 'color', 'limit': 1, 'offset': 10},
        )
        self.assertEqual(response.data[0]['name'], 'Amur')

    def test_large_offset(self):
        response = self.client.get(URL, {'offset': 30},
        )
        self.assertEqual(response.data, [])

    def test_invalid_offset(self):
        self.client.get(URL, {'offset': 'string'})
        self.assertRaisesMessage(BadRequest, 'invalid')

    def test_negative_offset(self):
        self.client.get(URL, {'offset': -10})
        self.assertRaisesMessage(BadRequest, 'negative')
