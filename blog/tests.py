from django.test import TestCase

from .views import post, add_comment, \
    month, delete_comment, month, blog
# Create your tests here.


class BlogViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/blog/')
        self.assertEqual(resp.status_code, 200)
