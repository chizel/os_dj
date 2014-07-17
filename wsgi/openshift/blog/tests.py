from django.test import TestCase

from blog.models import BlogPost, BlogComment, Tag
from userprofile.models import UserProfile
from django.contrib.auth.models import User


class BlogPostTest(TestCase):
    user = User()
    user.name = 'Greg'
    user.set_password('hello'),
    user.save()
    user = UserProfile.objects.create(

    def setUp(self):
        BlogPost.objects.create(
                title='Hello',
                body='Blogpost\'s body',
                user=1)
 
    def test_blogpost(self):
        firts_bp = BlogPost.objects.get(pk=1)
        self.assertEqual(first_bp.title, 'Hello')
        self.assertEqual(first_bp., 'Hello')
