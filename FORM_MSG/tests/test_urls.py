from django.test import TestCase
from django.urls import reverse

from FORM_MSG.tests.tests_views import MessageTestBase


class SwaggerTest(TestCase):
    def test_get_page(self):
        r = self.client.get(reverse('api:openapi-schema'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('api:swagger-ui'))
        self.assertEqual(r.status_code, 200)


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
        # self.assertEqual(response.url, '/accounts/login/?next=/msg1/send/')

    def test_get_msg_404(self):
        response = self.authorized_client.get(reverse('form_msg:show_msg', kwargs={'pk': 9999}), {})
        self.assertEqual(response.status_code, 404)

    def test_edit_msg_guest(self):
        """redirect to login"""
        response = self.client.get(reverse('form_msg:edit_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))
        # self.assertEqual(response.url, '/accounts/login/?next=/msg1/edit/1/')

    def test_edit_msg_other_user(self):
        """redirect to login"""
        response = self.authorized_client2.get(reverse('form_msg:edit_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_delete_msg_guest(self):
        response = self.client.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))
        # self.assertEqual(response.url, '/accounts/login/?next=/msg1/edit/1/')

    def test_delete_msg_other_user(self):
        response = self.authorized_client2.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    def test_delete_msg_by_creator(self):
        response = self.authorized_client.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)


class LikeMessageTestURLS(MessageTestBase):
    def test_like_msg_auth(self):
        # MessageTestURLS.test_create_msg_auth()

        response = self.authorized_client.post(reverse('form_msg:like', kwargs={'pk': 1}), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('form_msg:msg_list'))

    def test_like_msg_guest(self):
        response = self.client.post(reverse('form_msg:like', kwargs={'pk': 1}), {})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/?next=/'))

    def test_like_msg_404(self):
        response = self.authorized_client.post(reverse('form_msg:like', kwargs={'pk': 9999}), {})
        self.assertEqual(response.status_code, 404)
