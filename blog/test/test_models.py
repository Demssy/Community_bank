from django.test import TestCase
from .test_models import Blog

class BlogModelTestCase(TestCase):
    def setUp(self):
        Blog.objects.create(title='A new title', slug='some-prob-unique-slug-by-this-test-abc-123')

    def create_post(self, title='This title'):
        return Blog.objects.create(title=title)

    def test_post_title(self):
        obj = Blog.objects.get(slug='some-prob-unique-slug-by-this-test-abc-123')
        self.assertEqual(obj.title, 'A new title')
        self.assertTrue(obj.content == "")

    def test_post_slug(self):
        # generate slug
        title1 = 'another title abc'
        title2 = 'another title abc'
        title3 = 'another title abc'
        slug1 = Blog(title1)
        slug2 = Blog(title2)
        slug3 = Blog(title3)
        obj1 = self.create_post(title=title1)
        obj2 = self.create_post(title=title2)
        obj3 = self.create_post(title=title2)
        self.assertEqual(obj1.slug, slug1)
        self.assertNotEqual(obj2.slug, slug2)
        self.assertNotEqual(obj3.slug, slug3)

    def test_post_qs(self):
        title1 = 'another title abc'
        obj1 = self.create_post(title=title1)
        obj2 = self.create_post(title=title1)
        obj3 = self.create_post(title=title1)
        qs = Blog.objects.filter(title=title1)
        self.assertEqual(qs.count(), 3)
        qs2 = Blog.objects.filter(slug=obj1.slug)
        self.assertEqual(qs2.count(), 1)
