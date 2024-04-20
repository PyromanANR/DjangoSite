from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class LoginUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

class LogoutUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_logout_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

class RegisterUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_user(self):
        test_username = 'newuser'
        test_password = 'newpassword1'
        response = self.client.post(reverse('register'), {
            'username': test_username,
            'password1': test_password,
            'password2': test_password
        })
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(get_user_model().objects.filter(username=test_username).exists())