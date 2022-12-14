from django.db.models import Q
from django.urls import reverse

from FORM_MSG.models import Message
from FORM_MSG.tests.tests_views import MessageTestBase


class MessageFormTest(MessageTestBase):
    def test_create_form_msg(self):
        msg_count = Message.objects.count()
        self.assertEqual(msg_count, 1)

        form_data = {
            'name': 'username1',
            'text': 'text1',
            'accept_terms': True
        }

        response = self.authorized_client.post(path=reverse('form_msg:send_msg'),
                                               data=form_data)
        self.assertRedirects(response, expected_url=reverse('form_msg:send_msg'))

        self.assertEqual(Message.objects.count(), msg_count + 1)
        self.assertTrue(Message.objects.filter(Q(name='username1') & Q(text='text1')).exists())
