import json
from unittest import TestCase

from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)

from ..views import TicketCreateView

client = APIClient()
factory = APIRequestFactory()
user = User.objects.get(username="Doncic123")
view = TicketCreateView.as_view()


class BaseViewTestCase(TestCase):
    def setUp(self) -> None:
        self.email = "testexample@gmail.com"
        self.username = "example_one"
        self.password = "12345"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )

        self.url = reverse("token_obtain_pair")


class TestTicketList(BaseViewTestCase):

    def setUp(self):
        super(TestTicketList, self).setUp()

        self.valid_ticket = {
            "category": "Account",
            "title": "I have a problem",
            "description": "Description of the problem"
        }

        self.invalid_ticket = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_create_ticket(self):

        resp = self.client.post(self.url, {'username': self.username, 'password': self.password},
                                format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        token = resp.data['access']
        self.client.post()
        client.credentials(Authorization="Bearer " + token)
        resp = client.get("api/v1/support/tickets")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)



