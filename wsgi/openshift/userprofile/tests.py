from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from userprofile.models import UserProfile, PrivateMessage


class UserProfileCreateTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        user = User.objects.create_user(
            username='Jimm',
            password='hello',
            email='jimm@gmail.com')
        UserProfile.objects.create(user=user)

    def test_user_register(self):
        # if user was logged in logout him and create new user
        self.client.logout()
        response = self.client.post(
            '/user/registration/',
            {'username': 'Greg',
             'email': 'greg@gmail.com',
             'password': 'hello'})
        self.assertEqual(response.status_code, 302)
        u = UserProfile.objects.get(pk=2)
        self.assertEqual(u.pk, u.user.pk)
        self.assertEqual(u.user.username, 'Greg')
        self.assertEqual(u.user.email, 'greg@gmail.com')

    def test_user_login(self):
        self.client.logout()
        response = self.client.post(
            '/user/login/',
            {'username': 'Jimm', 'password': 'hello', 'next': '/'})
        self.assertEqual(response.status_code, 302)

    def test_user_profile_edit(self):
        self.client.login(username='Jimm', password='hello')
        response = self.client.post(
            '/user/edit/',
            {'email': 'new@gmail.com',
             'about_me': 'hi',
             'website': 'http://www.linux.org/',
             'password': 'hello'})
        u = UserProfile.objects.get(pk=1)
        self.assertEqual(u.about_me, 'hi')
        self.assertEqual(u.website, 'http://www.linux.org/')
        self.assertEqual(u.user.email, 'new@gmail.com')
