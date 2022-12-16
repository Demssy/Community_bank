from django.test import TestCase
from blog.models import Blog

class ViewTestCase(TestCase):
    def create_post(self, title='This title'):
        return Blog.objects.create(title=title)

    def test_allBlogs_view(self):
        list_url = Blog("blog:list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)


    def test_detail_view(self):
        obj = self.create_post(title='Another New Title Test')
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    
    def test_create_view(self):
        obj = self.create_post(title='Another New Title Test')
        edit_url = reverse("posts:update", kwargs={"slug": obj.slug})
        print(edit_url)
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_view(self):
        obj = self.create_post(title='Another New Title Test')
        delete_url = obj.get_absolute_url() + "delete/"
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 404)
