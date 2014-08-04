from django.test import TestCase

# Create your tests here.


class BlogViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/blog/')
        self.assertEqual(resp.status_code, 200)
