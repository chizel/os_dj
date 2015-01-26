from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import BlogPost, BlogComment, Tag
from userprofile.models import UserProfile
from userprofile.tests import create_user


class BlogPostTest(TestCase):
    def create_user(self):
        # if user was logged in logout him and create new user
        self.client.logout()
        response = self.client.post(
            '/user/registration/',
            {'username': 'Greg',
             'email': 'greg@gmail.com',
             'password': 'hello'})
        self.assertEqual(response.status_code, 302)
        self.u = UserProfile.objects.get(pk=1)

    def test_bp_creation(self):
        BlogPost.objects.create(
            title='Hello',
            body='Blogpost\'s body',
            user=self.user)

        firts_bp = BlogPost.objects.get(pk=1)
        self.assertEqual(first_bp.title, 'Hello')
        self.assertEqual(first_bp.user, self.user)
