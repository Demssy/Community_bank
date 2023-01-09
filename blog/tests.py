from django.test import TestCase, Client
from django.urls import reverse
from .models import Blog
from accounts.models import CustomUser
import datetime
from .forms import BlogForm


class BlogModelTestCase(TestCase):
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="Test University",
        major="Computer Science",
        gender="Male",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar=None
    )
        Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date=datetime.date(year=2023, month=1, day=7), user=user)
    
    def test_blog_title(self):
        """Test that the title of the blog is set correctly"""
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.title, "Test Blog")

    def test_blog_description(self):
        """Test that the description of the blog is set correctly"""
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.description, "This is a test blog for unit testing")

    def test_blog_date(self):
        """Test that the date of the blog is set correctly"""
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.date, datetime.date(year=2023, month=1, day=7))

    def test_blog_user(self):
        """Test that the user foreign key of the blog is set correctly"""
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.user.username, "testuser")
    
    def test_blog_create_method(self):
        """Test that the create method creates a new Blog object"""
        blog = Blog.create("Test Blog 2", "This is another test blog for unit testing", "2022-01-02", CustomUser.objects.get(username="testuser"))
        self.assertEqual(blog.title, "Test Blog 2")
        self.assertEqual(Blog.objects.count(), 2)
    
    def test_blog_delete_method(self):
        """Test that the delete method deletes a Blog object"""
        blog = Blog.objects.get(title="Test Blog")
        blog.delete_blog()
        self.assertEqual(Blog.objects.count(), 0)

class BlogFormTestCase(TestCase):
    def setUp(self):
        self.form_data = {
            'title': 'Test Blog',
            'date': '2022-01-01',
            'description': 'This is a test blog for unit testing',
        }
    
    def test_form_valid(self):
        """Test that the form is valid with correct data"""
        form = BlogForm(data=self.form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_without_title(self):
        """Test that the form is invalid if the title field is left blank"""
        self.form_data['title'] = ''
        form = BlogForm(data=self.form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_invalid_without_date(self):
        """Test that the form is invalid if the date field is left blank"""
        self.form_data['date'] = ''
        form = BlogForm(data=self.form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_invalid_without_description(self):
        """Test that the form is invalid if the description field is left blank"""
        self.form_data['description'] = ''
        form = BlogForm(data=self.form_data)
        self.assertFalse(form.is_valid())



class AllBlogsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('all_blogs')
        user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar= 'media/default.jpg'
        )
        Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date="2022-01-01", user=user)
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('all_blogs'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_blogs.html')
    
    def test_view_returns_correct_context(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['blogs'].count(), 1)
        self.assertEqual(response.context['blogs'][0].title, "Test Blog")        


class BlogsPageViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('blogs_page')
        user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date="2022-01-01", user=user)
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location_bp(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_bp(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('blogs_page'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template_bp(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs_page.html')
    
    def test_view_returns_correct_context_bp(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['blogs'].count(), 1)
        self.assertEqual(response.context['blogs'][0].title, "Test Blog") 



class DetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.blog = Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date="2022-01-01", user=user)
        self.url = reverse('detail', kwargs={'blog_id': self.blog.pk})
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)               


    def test_view_url_accessible_by_name(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('detail', kwargs={'blog_id': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
    
    def test_view_returns_correct_context(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['blog'], self.blog)   


class CreateBlogViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('createBlog')
        self.user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('createBlog'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createPost.html')
    
    def test_view_form_submission(self):
        """Test that the view creates a new Blog object on successful form submission"""
        data = {
            'title': "Test Blog",
            'description': "This is a test blog for unit testing",
            'date': "2022-01-01"
        }
        self.client.post(self.url, data=data)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.first().title, "Test Blog")        


    def test_view_form_submission_error(self):
        """Test that the view returns an error message on unsuccessful form submission"""
        data = {
            'title': "",
            'description': "This is a test blog for unit testing",
            'date': "2022-01-01"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.context['error'], 'Bad data passed in. Try again')   


class EditBlogViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.blog = Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date="2022-01-01", user=self.user)
        self.url = reverse('editBlog', kwargs={'blog_id': self.blog.pk})
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('editBlog', kwargs={'blog_id': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editBlog.html')
    
    def test_view_form_submission(self):
        """Test that the view updates the Blog object on successful form submission"""
        data = {
            'title': "Updated Test Blog",
            'description': "This is an updated test blog for unit testing",
            'date': "2022-01-01"
        }
        self.client.post(self.url, data=data)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.first().title, "Updated Test Blog")
    
    def test_view_form_submission_error(self):
        """Test that the view returns an error message on unsuccessful form submission"""
        data = {
            'title': "",
            'description': "This is an updated test blog for unit testing",
            'date': "2022-01-01"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.context['error'], 'Bad info') 


class DeleteBlogViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.blog = Blog.objects.create(title="Test Blog", description="This is a test blog for unit testing", date="2022-01-01", user=self.user)
        self.url = reverse('deleteBlog', kwargs={'blog_id': self.blog.pk})
        self.client.login(username="testuser", password="testpass") 

        
    def test_view_form_submission(self):
        """Test that the view deletes the Blog object on form submission"""
        self.client.post(self.url)
        self.assertEqual(Blog.objects.count(), 0)                   



    def test_view_redirects_after_form_submission_dep(self):
        """Test that the view redirects to the correct URL after form submission"""
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('all_blogs'))

    def test_view_only_allows_project_owner_to_delete(self):
        """Test that the view only allows the project owner to delete the project"""
        other_user = CustomUser.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="otherpass",
            first_name="Other",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.client.login(username="otheruser", password="otherpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


    def test_view_handles_invalid_project_id(self):
        """Test that the view handles the case where the project ID passed in the URL does not exist in the database"""
        invalid_url = reverse('deleteBlog', kwargs={'blog_id': 12345})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)    