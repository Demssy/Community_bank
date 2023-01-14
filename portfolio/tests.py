from django.test import TestCase, Client, override_settings
from accounts.models import CustomUser
from django.urls import reverse
from .forms import PortfolioForm
from.models import Project
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO  
import base64               # for decoding base64 image
import tempfile             # for setting up tempdir for media

class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )
        self.image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )

        self.project = Project.objects.create(
            title='Test Project', 
            description='This is a test project for testing the Project model.',
            user=self.user,
            image = self.image,
            url = 'www.test.url',
            project_type='WEB_DEV'
        )

    def test_project_creation(self):
        # Check if the project was created successfully
        self.assertTrue(isinstance(self.project, Project))
        self.assertEqual(self.project.__str__(), self.project.title)

    def test_project_type_name(self):
        # Check if the get_project_type_name method returns the correct project type name
        self.assertEqual(self.project.get_project_type_name(self.project.project_type), 'Web Development')

    def test_project_deletion(self):
        # Delete the project and check if it was deleted successfully
        self.project.delete()
        self.assertFalse(Project.objects.filter(title='Test Project').exists())    

    def test_project_title(self):
        """Test that the title of the project is set correctly"""
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.title, "Test Project")  

    def test_project_description(self):
        """Test that the description of the project is set correctly"""
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.description, "This is a test project for testing the Project model.")

    def test_project_image(self):
        """Test that the image of the project is set correctly"""
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        self.project = Project.objects.create(
            title='Test Project', 
            description='This is a test project for testing the Project model.',
            user=self.user,
            image = 'media/default.jpg',
            url = 'www.test.url',
            project_type='WEB_DEV'
        )
        self.assertEqual(self.project.image, 'media/default.jpg')

    def test_project_url(self):
        """Test that the user of the project is set correctly"""
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.url, 'www.test.url')    

    def test_project_user(self):
        """Test that the user foreign key of the blog is set correctly"""
        project = Project.objects.get(title="Test Project")
        self.assertEqual(project.user.username, "testuser")    


    def test_project_delete_method(self):
        """Test that the delete method deletes a Project object"""
        project = Project.objects.get(title="Test Project")
        project.delete()
        self.assertEqual(Project.objects.count(), 0)





class ProjectFormTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg')

        self.image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        self.form_data = {
            'title': 'Test Project',
            'description': 'This is a test project for testing the PortfolioForm.',
            'image': 'image',
            'url': 'https://www.testproject.com',
            'project_type': 'WEB_DEV'
        }
    def test_valid_form(self):
        form = PortfolioForm(data=self.form_data, files={'image':self.image})
        self.assertTrue(form.is_valid())
    
    
    def test_invalid_form(self):
        # Test for missing required fields
        form_data = {'title': 'Test Project'}
        form = PortfolioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = PortfolioForm(data=self.form_data, files={'image':self.image})
        project = form.save()
        self.assertEqual(project.title, self.form_data['title'])    
    
    def test_form_invalid_without_image(self):
        """Test that the form is invalid if the image field is left blank"""
        form_data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'project_type': 'WEB_DEV',
            'url': 'http://example.com/test-project'
        }
        form = PortfolioForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_valid_without_url(self):
        """Test that the form is valid if the url field is left blank"""
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        form_data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'project_type': 'WEB_DEV',
            'url': ''
        }
        
        form = PortfolioForm(data=form_data, files={'image':image})
        self.assertTrue(form.is_valid())   
    
    def test_form_invalid_without_description(self):
        """Test that the form is invalid if the description field is left blank"""
        form_data = {
            'title': 'Test Project',
            'description': '',
            'project_type': 'WEB_DEV',
            'image': 'media/avatars/default.jpg',
            'url': 'http://example.com/test-project'
        }
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        form = PortfolioForm(data=form_data, files={'image':image})
        self.assertFalse(form.is_valid())        



class UserPortfolioViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'https://www.testproject.com', user = self.user)
        self.url = reverse('userPortfolio')
        self.client.login(username="testuser", password="testpass")
    
    def test_view_returns_correct_data_p(self):
        
        # Check if the view returns the correct data
        response = self.client.get(reverse('userPortfolio'))
        self.assertEqual(response.context['projects'].first().title, 'Test Project')
    
    def test_view_url_accessible_by_name_p(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('userPortfolio'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        # Log the test user in
        # Check if the view uses the correct template
        response = self.client.get(reverse('userPortfolio'))
        self.assertTemplateUsed(response, 'userPortfolio.html')
    
    def test_view_returns_correct_context_p(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['projects'].count(), 1)
        self.assertEqual(response.context['projects'][0].title, "Test Project")        
        self.assertContains(response, 'Test Project')

    def test_view_returns_correct_data(self):
        # Check if the view returns the correct data
        response = self.client.get(reverse('userPortfolio'))
        self.assertEqual(response.context['projects'].first().title, 'Test Project')    


class ProjectsPageViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'www.test.url', user = user)
        self.url = reverse('projects_page') 
        self.client.login(username="testuser", password="testpass")

    def test_view_url_exists_at_desired_location_pp(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_pp(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('projects_page'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template_pp(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects_page.html')
    
    def test_view_returns_correct_context_pp(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['projects'].count(), 1)
        self.assertEqual(response.context['projects'][0].title, "Test Project") 




class DetailpViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        self.project = Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'www.test.url', user = user)

        self.client.login(username="testuser", password="testpass")
        self.url = reverse('detailp', kwargs={'project_id': self.project.pk})
    
    def test_view_url_exists_at_desired_location_dp(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)               


    def test_view_url_accessible_by_name_dp(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('detailp', kwargs={'project_id': self.project.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template_dp(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailp.html')
    
    def test_view_returns_correct_context_dp(self):
        """Test that the view returns the correct context data"""
        response = self.client.get(self.url)
        self.assertEqual(response.context['project'], self.project)         
        



class CreateProjectViewTestCase(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        #Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'www.test.url', user = user)
        self.url = reverse('createPortfolio')
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location_cp(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_cp(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('createPortfolio'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template_cp(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createPortfolio.html')
    
    def test_view_form_submission_cp(self):
        """Test that the view creates a new Project object on successful form submission"""
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'project_type': 'WEB_DEV',
            'image': image,
            'url': 'http://example.com/test-project'
        }
        
        self.client.post(self.url, data=data)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().title, "Test Project")        


    def test_view_form_submission_error_cp(self):
        """Test that the view returns an error message on unsuccessful form submission"""
        data = {
            'title': '',
            'description': 'This is a test project',
            'project_type': 'WEB_DEV',
            'image': 'media/avatars/default.jpg',
            'url': 'http://example.com/test-project'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.context['error'], 'Bad data passed in. Try again')  





class EditProjectViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        self.project = Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'www.test.url', user = user)

        self.url = reverse('editProject', kwargs={'project_id': self.project.pk})
        self.client.login(username="testuser", password="testpass")
    
    def test_view_url_exists_at_desired_location_ep(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_ep(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('editProject', kwargs={'project_id': self.project.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template_ep(self):
        """Test that the view uses the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editProject.html')
    
    def test_view_form_submission_ep(self):
        """Test that the view updates the Blog object on successful form submission"""
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        data = {
            'title': 'Updated Test Project',
            'description': 'This is an updated test project for unit testing',
            'project_type': 'WEB_DEV',
            'image': image,
            'url': 'http://example.com/test-project'
        }
        self.client.post(self.url, data=data)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().title, "Updated Test Project")
    
    def test_view_form_submission_error(self):
        """Test that the view returns an error message on unsuccessful form submission"""
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        data = {
            'title': '',
            'description': 'This is an updated test project for unit testing',
            'project_type': 'WEB_DEV',
            'image': image,
            'url': 'http://example.com/test-project'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.context['error'], 'Bad info') 


class DeleteProjectViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass",
        first_name="Test",
        last_name="User",
        college="SCE",
        major="CE",
        gender="M",
        date_of_birth="1998-01-01",
        bio="This is a test user for unit testing",
        user_avatar='media/default.jpg'
    )

        self.project = Project.objects.create(title = 'Test Project', description = 'This is a test project for unit testing',project_type = 'WEB_DEV' , image = 'user_profile/avatars/test.jpg', url = 'www.test.url', user = user)

        self.url = reverse('deleteProject', kwargs={'project_id': self.project.pk})
        self.client.login(username="testuser", password="testpass") 

        
    def test_view_form_submission_dep(self):
        """Test that the view deletes the Blog object on form submission"""
        self.client.post(self.url)
        self.assertEqual(Project.objects.count(), 0) 

    def test_view_redirects_after_form_submission_dep(self):
        """Test that the view redirects to the correct URL after form submission"""
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('userPortfolio'))

    def test_view_only_allows_project_owner_to_delete(self):
        """Test that the view only allows the project owner to delete the project"""
        other_user = CustomUser.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="otherpass",
            first_name="Other",
            last_name="User",
            college="BGU",
            major="CE",
            gender="F",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.client.login(username="otheruser", password="otherpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)


    def test_view_handles_invalid_project_id(self):
        """Test that the view handles the case where the project ID passed in the URL does not exist in the database"""
        invalid_url = reverse('deleteProject', kwargs={'project_id': 12345})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)

    

TEST_IMAGE = '''
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
'''.strip()  