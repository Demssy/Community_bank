import datetime
from multiprocessing import AuthenticationError
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from accounts.form import RegisterUserForm
from .forms import UserSetting
from .models import ContactUsModel, ContactAdmin
from portfolio.models import Project
from blog.models import Blog
from accounts.models import CustomUser

class ContactUsModelTestCase(TestCase):
    def setUp(self):
        ContactUsModel.objects.create(
            name='John Smith',
            email='john@example.com',
            subject='Hello',
            message='Hello, I am reaching out to you to say hello!'
        )
        ContactUsModel.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            subject='Hi',
            message='Hi, just wanted to say hi!'
        )

    def test_contact_us_model_str(self):
        """
        This test case first creates two instances of the ContactUsModel, one for John and one for Jane. It then tests that the __str__ method of the model is correct by checking that the string representation of each instance is equal to the expected email.
        """
        john = ContactUsModel.objects.get(name='John Smith')
        jane = ContactUsModel.objects.get(name='Jane Doe')
        self.assertEqual(str(john), 'john@example.com')
        self.assertEqual(str(jane), 'jane@example.com')

    

    def test_contact_us_model_fields(self):
        john = ContactUsModel.objects.get(name='John Smith')
        jane = ContactUsModel.objects.get(name='Jane Doe')
        self.assertEqual(john.name, 'John Smith')
        self.assertEqual(john.email, 'john@example.com')
        self.assertEqual(john.subject, 'Hello')
        self.assertEqual(john.message, 'Hello, I am reaching out to you to say hello!')
        self.assertEqual(jane.name, 'Jane Doe')
        self.assertEqual(jane.email, 'jane@example.com')
        self.assertEqual(jane.subject, 'Hi')
        self.assertEqual(jane.message, 'Hi, just wanted to say hi!')

    def test_created_at_field(self):
        hello = ContactUsModel.objects.get(subject='Hello')
        self.assertIsInstance(hello.created_at, datetime.datetime)

    def test_updated_at_field(self):
        hello = ContactUsModel.objects.get(subject='Hello')
        self.assertIsInstance(hello.updated_at, datetime.datetime)


class ContactAdminTestCase(TestCase):
    
    def setUp(self):
        ContactAdmin.objects.create(
            subject='Hello',
            message='Hello, I am reaching out to you to say hello!'
        )
        ContactAdmin.objects.create(
            subject='Hi',
            message='Hi, just wanted to say hi!'
        )

    def test_contact_admin_model_str(self):
        hello = ContactAdmin.objects.get(subject='Hello')
        hi = ContactAdmin.objects.get(subject='Hi')
        self.assertEqual(str(hello), 'Hello')
        self.assertEqual(str(hi), 'Hi')

    def test_subject_max_length(self):
        hello = ContactAdmin.objects.get(subject='Hello')
        self.assertLessEqual(len(hello.subject), 100)

    def test_message_max_length(self):
        hello = ContactAdmin.objects.get(subject='Hello')
        self.assertLessEqual(len(hello.message), 500)

    def test_created_at_field(self):
        hello = ContactAdmin.objects.get(subject='Hello')
        self.assertIsInstance(hello.created_at, datetime.datetime)

    def test_updated_at_field(self):
        hello = ContactAdmin.objects.get(subject='Hello')
        self.assertIsInstance(hello.updated_at, datetime.datetime)
    


class UserSettingFormTestCase(TestCase):
    def test_form_has_required_fields(self):
        form = UserSetting()
        required_fields = ['major', 'college', 'first_name', 'last_name', 'email', 'user_avatar', 'date_of_birth', 'gender', 'bio']
        for field in required_fields:
            self.assertTrue(field in form.fields)    

    def test_form_inputs_have_expected_attributes(self):
        form = UserSetting()
        self.assertTrue(form.fields['date_of_birth'].widget.attrs['class'] == 'form-control')
        self.assertTrue(form.fields['date_of_birth'].widget.attrs['placeholder'] == 'Select a date')
        self.assertTrue(form.fields['date_of_birth'].widget.attrs['input_type'] == 'date')

    def test_form_validation_for_blank_fields(self):
        form_data = {
            'major': '',
            'college': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'user_avatar': '',
            'date_of_birth': '',
            'gender': '',
            'bio': '',
        }
        form = UserSetting(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_validation_for_valid_data(self):
        form_data = {
            'major': 'Computer Science',
            'college': 'University',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'user_avatar': 'media/avatars/default.jpg',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'bio': 'I am a computer science student at UC Berkeley.',
        }
        form = UserSetting(data=form_data)
        self.assertTrue(form.is_valid())        

    


class HomeViewTestCase(TestCase):
    def setUp(self):
        # Create a user that can be logged in to access the view
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='test1298',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
        self.client.login(username='testuser', password='test1298')

    def test_home_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('home'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains the expected data
        self.assertContains(response, 'Home')
        
        # Check that the view is using the correct template
        self.assertTemplateUsed(response, 'home.html')
            

class SearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="test1298",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Male",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.user2 = CustomUser.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
            college="Test University",
            major="Computer Science",
            gender="Female",
            date_of_birth="1998-01-01",
            bio="This is a test user for unit testing",
            user_avatar='media/default.jpg'
        )
        self.project1 = Project.objects.create(title="Test Project 1", description="This is a test project for unit testing", image ='media/default.jpg' , user=self.user1)
        self.project2 = Project.objects.create(title="Test Project 2", description="This is a test project for unit testing", image ='media/default.jpg', user=self.user2)
        self.blog1 = Blog.objects.create(title="Test Blog 1", description="This is a test blog for unit testing", date="2022-01-01", user=self.user1)
        self.blog2 = Blog.objects.create(title="Test Blog 2", description="This is a test blog for unit testing", date="2022-01-01", user=self.user2)
        self.client.login(username='testuser1', password='test1298')
        self.url = reverse('search')     


    def test_view_url_exists_at_desired_location(self):
        """Test that the view URL exists at the desired location"""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the view URL is accessible by name"""
        response = self.client.get(reverse('search'), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
    
    def test_view_form_submission(self):
        """Test that the view performs a search on form submission and returns the correct results"""
        response = self.client.post(reverse('search'), {'searched': 'Test'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project 1')
        self.assertContains(response, 'Test Project 2')
        self.assertContains(response, 'Test Blog 1')
        self.assertContains(response, 'Test Blog 2')
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')
    

class PersonalAreaViewTestCase(TestCase):
    def setUp(self):
        # Create a user that can be logged in to access the view
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
        
    def test_personal_area_view(self):
        # Log in the user
        #self.client.login(username='testuser', password='testpass')
        self.client.force_login(self.user)
        # Send a GET request to the view
        response = self.client.get(reverse('personalArea'), follow=True)
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains the expected data
        self.assertContains(response, 'This is a test user')
       
        # Check that the view is using the correct template
        self.assertTemplateUsed(response, 'personalArea.html')     




class UserSettingsViewTestCase(TestCase):
    def setUp(self):
        # Create a user that can be logged in to access the view
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='test1298',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
        self.client.login(username='testuser', password='test1298')

    def test_user_settings_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('userSettings'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains the user's data
        self.assertEqual(response.context['user'], self.user)
        # Check that the rendered template is the correct one
        self.assertTemplateUsed(response, 'userSettings.html')


    def test_user_settings_view_handles_invalid_form_submission(self):
        # Send a POST request to the view with invalid form data
        response = self.client.post(reverse('userSettings'), {'email': 'invalid'})
        
        # Check that the response includes an error message
        self.assertContains(response, 'Enter a valid email address.')
        
        # Check that the form is re-rendered with the invalid data
       
        self.assertEqual(response.context['form'].data['email'], 'invalid')

    def test_user_settings_view_updates_user_data_on_valid_form_submission(self):
        # Send a POST request to the view with valid form data
        response = self.client.post(reverse('userSettings'), {
            'email': 'testuser2@example.com',
            'first_name': 'Test2',
            'last_name': 'User2',
            'college': 'Test College 2',
            'major': 'Test Major 2',
            'date_of_birth':'1996-11-24',
            'password1': 'newpass1298',
             'password2': 'newpass1298'
        })
        
        # Get the updated user from the database
        updated_user = CustomUser.objects.get(pk=self.user.pk)
        
        # Check that the user's data is updated
        self.assertEqual(updated_user.email, 'testuser2@example.com')
        self.assertEqual(updated_user.first_name, 'Test2')
        self.assertEqual(updated_user.last_name, 'User2')
        self.assertEqual(updated_user.college, 'Test College 2')
        self.assertEqual(updated_user.major, 'Test Major 2')    


            # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        
        # Check that the response's location header points 
        self.assertEqual(response['location'], '/personalArea/')
       
        #self.assertRedirects(response, 'personalArea.html')



class SignupViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
                username='testuser',
                password='test1298',
                email='testuser@example.com',
                first_name='Test',
                last_name='User',
                college='Test College',
                major='Test Major',
                gender='Male',
                date_of_birth='2000-01-01',
                bio='This is a test user',
                user_avatar='user_profile/avatars/test.jpg'
            )
        #self.client.login(username='testuser', password='test1298')    
    def test_signup_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('signupuser'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains a form
        self.assertIsInstance(response.context['form'], RegisterUserForm)
        
        # Check that the rendered template is the correct one
        self.assertTemplateUsed(response, 'signupuser.html')
        
    def test_signup_view_creates_user_on_valid_form_submission(self):
        # Send a POST request to the view with valid form data
        response = self.client.post(reverse('signupuser'), {
            'username': 'testuser1',
            'password1': 'testpass',
            'password2': 'testpass',
            'first_name': 'Test',
            'last_name': 'User',
            'college': 'Test College',
            'date_of_birth': '2020-01-01',
            'gender': 'M',
            'email': 'testuser@example.com',
            'major': 'Test Major'
        })        


         # Check that the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Check that the user is redirected to the home page
        self.assertRedirects(response, '/')
        
        # Check that the user is saved in the database
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.first().username, 'testuser')



    def test_signup_view_displays_error_on_non_matching_passwords(self):
        # Send a POST request to the view with non-matching passwords
        response = self.client.post(reverse('signupuser'), {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'differentpass',
            'first_name': 'Test',
            'last_name': 'User',
            'college': 'Test College',
            'date_of_birth': '2020-01-01',
            'gender': 'M',
            'email': 'testuser@example.com',
            'major': 'Test Major'
        })
        
        # Check that the view displays an error message
        self.assertContains(response, 'Passwords did not match')    



    def test_signup_view_displays_error_on_duplicate_username(self):
       
        response = self.client.post(reverse('signupuser'), {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass',
            'first_name': 'Test',
            'last_name': 'User',
            'college': 'Test College',
            'date_of_birth': '2020-01-01',
            'gender': 'M',
            'email': 'testuser@example.com',
            'major': 'Test Major',
        })
        
        # Check that the view displays an error message
        self.assertContains(response, 'That username has already been taken. Please try again.')    



class LoginViewTestCase(TestCase):
    def setUp(self):
        # Create a user to log in
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='test1298',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
    
    def test_login_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('loginuser'))
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains a form
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        
        # Check that the rendered template is the correct one
        self.assertTemplateUsed(response, 'loginuser.html')


    def test_login_view_authenticates_user_on_valid_form_submission(self):    
        # Send a POST request to the view with valid form data
        response = self.client.post(reverse('loginuser'), {
            'username': 'testuser',
            'password': 'test1298'
        })
        
        # Check that the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # Check that the user is redirected to the home page
        self.assertRedirects(response, '/')

   

    def test_login_view_displays_error_on_invalid_credentials(self):
        # Send a POST request to the view with invalid credentials
        response = self.client.post(reverse('loginuser'),{
            'username': 'testuser',
            'password': 'testpasssss'
        })

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check that the rendered context contains a form
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        
        # Check that the rendered template is the correct one
        self.assertTemplateUsed(response, 'loginuser.html')
        
        # Check that the view displays an error message
        self.assertContains(response, 'Username and password did not match')
        
        # Check that the user is not logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)




class ContactUsViewTestCase(TestCase):        
    def setUp(self):
        # Create a user to log in
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='test1298',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
        self.client.login(username='testuser', password='test1298')



    def test_contactus_view_get(self):
        # Send a GET request to the contactus view
        response = self.client.get('/contactus/')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactus.html')


    def test_contactus_view(self):
        # Send a POST request to the contactus view with valid form data
        response = self.client.post('/contactus/', {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactus.html')


    def test_contactus_view_with_invalid_form_data(self):
        # Send a POST request to the contactus view with invalid form data
        response = self.client.post('/contactus/', {
            'name': '',  # Name is required but left blank
            'email': 'invalid',  # Invalid email format
            'subject': '',  # Subject is required but left blank
            'message': ''  # Message is required but left blank
        })

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactus.html')

        # Assert that the rendered context contains the expected form errors
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertFormError(response, 'form', 'subject', 'This field is required.')    
        self.assertFormError(response, 'form', 'message', 'This field is required.')



class ContactAdminViewTestCase(TestCase):

    def setUp(self):
        # Create a user to log in
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='test1298',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            college='Test College',
            major='Test Major',
            gender='Male',
            date_of_birth='2000-01-01',
            bio='This is a test user',
            user_avatar='user_profile/avatars/test.jpg'
        )
        self.client.login(username='testuser', password='test1298')

    def test_contactadmin_view_get(self):
        # Send a GET request to the contactadmin view
        response = self.client.get('/contactadmin/')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactadmin.html')   



    def test_contactadmin_view(self):
        # Send a POST request to the contactadmin view with valid form data
        response = self.client.post('/contactadmin/', {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactadmin.html')

        # Assert that the message and hasError variables in the context are as expected
        self.assertEqual(response.context['message'], 'Message was sent successfully')
        self.assertFalse(response.context['hasError'])             


    def test_contactadmin_view_with_invalid_form_data(self):
        # Send a POST request to the contactadmin view with invalid form data
        response = self.client.post('/contactadmin/', {
            'name': '',  # Name is required but left blank
            'email': 'invalid',  # Invalid email format
            'subject': '',  # Subject is required but left blank
            'message': ''  # Message is required but left blank
        })

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the correct template
        self.assertTemplateUsed(response, 'contactadmin.html')

        # Assert that the message and hasError variables in the context are as expected
        self.assertEqual(response.context['message'], 'Please make sure all fields are valid')
        self.assertTrue(response.context['hasError'])    