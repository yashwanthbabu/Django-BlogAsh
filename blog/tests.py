import time

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Post, Comment


class BlogEntriesTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.author = User.objects.create(username="Yashwanth",
                                          email="yashwanth@agiliq.com",
                                          password="yashwanth")
        self.post = Post.objects.create(author=self.author, title='Test',
                                        body='Testcase1',
                                        created=time.localtime()[:2])
        self.comment = Comment.objects.create(post=self.post,
                                              name="Yashwanth",
                                              email="yashwanth@agiliq.com",
                                              body="testcase1",
                                              created=time.localtime()[:2])

    def test_blog_access(self):
        response = self.c.get(reverse('main'))
        self.assertEqual(200, response.status_code)

    def test_blog_post_access(self):
        response = self.c.get(reverse('post', args=[self.post.id]))
        self.assertEqual(200, response.status_code)

    def test_blog_post_add_comment_access(self):
        response = self.c.get(reverse('add_comment', args=[self.post.id]))
        self.assertEqual(200, response.status_code)

    def test_blog_post_monthly_archive_access(self):
        response = self.c.get(reverse('month', args=[self.post.created.year,
                                      self.post.created.month]))
        self.assertEqual(200, response.status_code)

    def test_blog_post_delete_bulk_comment_access(self):
        response = self.c.get(reverse('delete_comment', args=[self.post.id]))
        self.assertEqual(302, response.status_code)
        if self.c.login(username="Yashwanth", password="yashwanth"):
            response = self.c.get(reverse('delete_comment',
                                          args=[self.post.id]))
            self.assertEqual(200, response.status_code)

    def test_blog_post_delete_single_comment_access(self):
        response = self.c.get(reverse('delete_single_comment',
                                      args=[self.post.id, self.comment.id]))
        self.assertEqual(302, response.status_code)
        if self.c.login(username="Yashwanth", password="yashwanth"):
            response = self.c.get(reverse('delete_single_comment',
                                          args=[self.post.id,
                                                self.comment.id]))
            self.assertEqual(200, response.status_code)

    def test_blog_recent_posts_access(self):
        response = self.c.get(reverse('recentposts'))
        self.assertEqual(200, response.status_code)

    def test_blog_post_user_logout_access(self):
        response = self.c.get(reverse('logout'))
        self.assertEqual(302, response.status_code)
        if self.c.login(username="Yashwanth", password="yashwanth"):
            response = self.c.get(reverse('logout'))
            self.assertEqual(200, response.status_code)
