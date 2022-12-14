from django import forms
from django.test import TestCase, Client, override_settings
from django.core.cache import cache
from django.urls import reverse

from FORM_MSG.tests.tests_views import MessageTestBase


class MessageTestURLS(MessageTestBase):
    def test_create_msg_auth(self):
        response = self.authorized_client.post(reverse('form_msg:send_msg'), {
            'name': 123,
            'text': 321,
            'user': self.authorized_client
        })
        self.assertEqual(response.status_code, 200)

    def test_create_msg_guest(self):
        """redirect to login"""
        response = self.client.post(reverse('form_msg:send_msg'), {
            'name': 123,
            'text': 321,
            'user': self.client
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))

    def test_edit_msg_guest(self):
        """redirect to login"""
        response = self.client.get(reverse('form_msg:edit_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))

    def test_edit_msg_other_user(self):
        """redirect to login"""
        response = self.authorized_client2.get(reverse('form_msg:edit_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_delete_msg_guest(self):
        response = self.client.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))

    def test_delete_msg_other_user(self):
        response = self.authorized_client2.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_delete_msg_by_creator(self):
        response = self.authorized_client.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
