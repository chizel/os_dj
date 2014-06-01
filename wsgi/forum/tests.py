from django.test import TestCase

from forum.models import Branch, Theme, Post

class ThemeTest(TestCase):
    def test_add_post(self):
        new_post = Post(id=1, theme_id=1, post='hi', user_id=1)
        self.assertEqual(new_post.id, 1)
        self.assertEqual(new_post.theme_id, 1)
        self.assertEqual(new_post.user_id, 1)
        self.assertEqual(new_post.post, 'hi')

        #UserProfile.objects.filter(pk=request.user.id).update(count_messages=F('count_messages')+1)
        #theme.increment_count_posts()
