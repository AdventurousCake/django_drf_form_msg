from django.core.cache import cache
from django.forms.models import model_to_dict
from django.test import TestCase, Client
from django.urls import reverse

from FORM_MSG.forms import MsgForm
from FORM_MSG.models import Message, Like
from core.models import User


# BASE CLASS
class MessageTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # cls.user = User.objects.get(username='admin')
        cls.user = User.objects.create_user(username='user1')
        cls.user2 = User.objects.create_user(username='user2')
        cls.message = Message.objects.create(author=cls.user,
                                             name='Name',
                                             text='123')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()

        """Создаем клиент зарегистрированного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
        cache.clear()


# TESTS START
class MessageViewTest(MessageTestBase):
    # Проверка используемых шаблонов
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары: имя шаблона:reverse(name)
        templates_page_names = {
            'form_msg/msg_list.html': reverse('form_msg:msg_list'),
            'form_msg/msg_BY_ID.html': reverse('form_msg:show_msg', kwargs={'pk': 1}),
            'form_msg/msg_send.html': reverse('form_msg:send_msg'),
            # 'form_msg/msg_send.html': reverse('form_msg:edit_msg'), # kwargs={'slug': 'test-slug'}
            'form_msg/signup.html': reverse('form_msg:signup'),
            'form_msg/USERPAGE.html': reverse('form_msg:users_details', kwargs={'pk': self.user.id}),
        }

        # проверяем что при обращении к name вызывается соотв. шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    # форма в forms
    # def test_home_page_show_correct_context(self):
    #     """Шаблон home сформирован с правильным контекстом."""
    #     response = self.guest_client.get(reverse('form_msg:send_msg'))
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Словарь ожидаемых типов полей формы:
    #     # указываем, объектами какого класса должны быть поля формы
    #     form_fields = {
    #         'title': forms.fields.CharField,
    #         # При создании формы поля модели типа TextField
    #         # преобразуются в CharField с виджетом forms.Textarea
    #         'text': forms.fields.CharField,
    #         'slug': forms.fields.SlugField,
    #         'image': forms.fields.ImageField,
    #     }
    #
    #     # Проверяем, что типы полей формы в словаре context
    #     # соответствуют ожиданиям
    #     for value, expected in form_fields.items():
    #         with self.subTest(value=value):
    #             form_field = response.context['form'].fields[value]
    #             # Проверяет, что поле формы является экземпляром
    #             # указанного класса
    #             self.assertIsInstance(form_field, expected)

    # БЕЗ PAGINATOR
    def test_msg_list_is_1(self):
        """тест контекста"""
        """проверка кол-ва объектов на странице"""
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        self.assertEqual(response.status_code, 200)
        # print(response.context['object_list'])

        self.assertEqual(response.context['object_list'].count(), 1)

    # БЕЗ PAGINATOR
    # Проверяем, что словарь context страницы /msg_list
    # в первом элементе списка object_list содержит ожидаемые значения
    def test_msg_list_page_show_correct_context(self):
        """Шаблон msg_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        self.assertEqual(response.status_code, 200)

        # взяли превый элемент из списка и проверили, что его содержание совпадает с ожидаемым
        first_object = model_to_dict(response.context['object_list'][0])
        print(first_object)

        message_id_0 = first_object.get('id')
        # message_author_0 = first_object.get('author__username')
        message_author_id_0 = first_object.get('author')
        message_text_0 = first_object.get('text')
        message_date_0 = first_object.get('date')

        # message_author_0 = first_object.get('author')
        # message_name_0 = first_object.get('name')
        # message_text_0 = first_object.get('text')

        self.assertEqual(message_id_0, 1)
        # self.assertEqual(message_author_0, self.user.username)
        self.assertEqual(message_author_id_0, 1)
        self.assertEqual(message_text_0, '123')
        # self.assertIsInstance(message_date_0, datetime.datetime)

    def test_msg_create_page_context(self):
        response = self.authorized_client.get(reverse('form_msg:send_msg'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], MsgForm)

    def test_initial_value(self):
        """Предустановленнное значение формы."""
        response = self.authorized_client.get(reverse('form_msg:send_msg'))
        self.assertEqual(response.status_code, 200)

        # print(response.context['form'])
        # print(response.context['form'].fields['text'])

        title_inital = response.context['form'].initial['text']
        self.assertEqual(title_inital, 'example')
        # self.assertEqual(title_inital, 'Значение по-умолчанию')

    # last
    def test_delete_msg(self):
        response = self.authorized_client.get(reverse('form_msg:delete_msg', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('form_msg:send_msg'))

        self.assertFalse(Message.objects.filter(id=1).exists())


class LikeMessageViewTest(MessageTestBase):
    def test_like_initial(self):
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['user_likes'])
        # print(response.context['object_list'])
        self.assertEqual(response.context['object_list'][0].likes_count(), 0)

    def test_like(self):
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'][0].likes_count(), 0)

        response2 = self.authorized_client.post(reverse('form_msg:like', kwargs={'pk': 1}), {})
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        self.assertEqual(response.context['object_list'][0].likes_count(), 1)

        self.assertTrue(Like.objects.filter(id=1).exists())

    # def test_like_unique(self):
    #     with self.assertRaises(IntegrityError):
    #         Like.objects.create(user=self.user, message=self.message)
    #         Like.objects.create(user=self.user, message=self.message)
