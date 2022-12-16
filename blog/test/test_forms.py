from django.test import TestCase
from blog.forms import Blog

class FormTestCase(TestCase):
    def test_valid_form(self):
        title = 'A new title'
        slug = 'some-prob-unique-slug-by-this-test-abc-123'
        content  = 'some content'
        obj = Blog.objects.create(title=title, slug=slug, content=content)
        data = {'title': obj.title, "slug": obj.slug, "publish": obj.publish, "content": content}
        form = Blog(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('title'), obj.title)
        self.assertNotEqual(form.cleaned_data.get("content"), "Another item")

