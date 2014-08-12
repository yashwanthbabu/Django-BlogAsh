from django.test import TestCase
from django.test.client import Client

class BlogEntriesTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_entries_access(self):
        response = self.c.get('/blog/posts/')
        self.assertEqual(response.status_code, 200)