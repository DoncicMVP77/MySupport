from datetime import timedelta
from importlib import reload
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import (AccessToken, RefreshToken,
                                             SlidingToken)
from rest_framework_simplejwt.utils import (aware_utcnow, datetime_from_epoch,
                                            datetime_to_epoch)
from rest_framework_simplejwt.views import TokenViewBase

from .utils import APIViewTestCase, override_api_settings

User = get_user_model()


class BaseJWTTestCase(TestCase):
    def setUp(self) -> None:
        self.email = "testexample@gmail.com"
        self.username = "example_one"
        self.password = "12345"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )


class TestTokenObtainPairView(BaseJWTTestCase):
    def setUp(self) -> None:
        super(TestTokenObtainPairView, self).setUp()
        self.url =  reverse("token_obtain_pair")

    def test_user_inactive(self):

        self.user.is_active = False
        self.user.save()

        res = self.client.post(self.url,
            data={
                User.USERNAME_FIELD: self.username,
                "password": self.password,
            }
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("detail", res.data)

    def test_success(self):
        res = self.client.post(self.url,
            data={
                User.USERNAME_FIELD: self.username,
                "password": self.password,
            }
        )

        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_fields_missing(self):
        res = self.client.post(self.url, data={})
        self.assertEqual(res.status_code, 400)
        self.assertIn(User.USERNAME_FIELD, res.data)
        self.assertIn("password", res.data)

        res = self.client.post(self.url, data={User.USERNAME_FIELD: self.username})
        self.assertEqual(res.status_code, 400)
        self.assertIn("password", res.data)

        res = self.client.post(self.url, data={"password": self.password})
        self.assertEqual(res.status_code, 400)
        self.assertIn(User.USERNAME_FIELD, res.data)

    def test_credentials_wrong(self):
        res = self.client.post(self.url,
            data={
                User.USERNAME_FIELD: self.username,
                "password": "test_user",
            }
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn("detail", res.data)
