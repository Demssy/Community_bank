import datetime
import os
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from .models import CustomUser
from.form import RegisterUserForm
from blog.models import Blog
from portfolio.models import Project
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class CustomUserModelTestCase(TestCase):

    def setUp(self):
        # Create the file that will be associated with the CustomUser instance
        with open(os.path.join('media/user_profile/avatars/test.jpg'), 'w') as f:
            f.write('Test file')

    def test_custom_user_model(self):
        # Create a new CustomUser instance
        user = CustomUser(username='testuser', email='test@example.com', is_student=True, college='MIT')
        # Save the instance to the database
        user.save()
        # Retrieve the instance from the database
        retrieved_user = CustomUser.objects.get(pk=user.pk)
        # Assert that the field values are correct
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertTrue(retrieved_user.is_student)
        self.assertEqual(retrieved_user.college, 'MIT')

    


    def test_delete_method(self):
        # Create a new CustomUser instance with an avatar image
        user = CustomUser(username='testuser', email='test@example.com', is_student=True, college='MIT', user_avatar='user_profile/avatars/test.jpg')
        user.save()
        # Check that the file exists before deleting the model
        self.assertTrue(os.path.exists(user.user_avatar.path))
        # Delete the model
        user.delete()
        # Check that the file was deleted after the model was deleted
        self.assertFalse(os.path.exists(user.user_avatar.path))


    def test_str_method(self):
        # Create a new CustomUser instance
        user = CustomUser(username='testuser', email='test@example.com', is_student=True, college='MIT')
        # Check that the __str__ method returns the correct string representation
        self.assertEqual(str(user), 'testuser')

    def test_password_handling(self):
        # Create a new CustomUser instance and set a password
        user = CustomUser(username='testuser', email='test@example.com', is_student=True, college='MIT')
        user.set_password('password')
        # Save the user to the database
        user.save()
        # Retrieve the user from the database and check that the password is correct
        retrieved_user = CustomUser.objects.get(pk=user.pk)
        self.assertTrue(retrieved_user.check_password('password'))
        # Check that the password is incorrect if the wrong password is provided
        self.assertFalse(retrieved_user.check_password('incorrectpassword'))


    def test_email_field(self):
        # Check that the email field is required
        with self.assertRaises(ValidationError):
            user = CustomUser(username='testuser', is_student=True, college='MIT')
            user.full_clean()

        # Check that the email field is validated as a proper email address
        with self.assertRaises(ValidationError):
            user = CustomUser(username='testuser', email='invalidemail', is_student=True, college='MIT')
            user.full_clean()

        # Check that the email field must be unique
        user1 = CustomUser(username='testuser1', email='test@example.com', is_student=True, college='MIT')
        user1.save()
        with self.assertRaises(IntegrityError):
            user2 = CustomUser(username='testuser2', email='test@example.com', is_student=True, college='MIT')
            user2.save()   


    def test_avatar_field(self):
        # Create a new CustomUser instance with an avatar image
        user = CustomUser(username='testuser', email='test@example.com', is_student=True, college='MIT', user_avatar='user_profile/avatars/test.jpg')
        user.save()
        # Check that the avatar file was saved correctly
        self.assertTrue(os.path.exists(user.user_avatar.path))
        # Check that the avatar field is non optional by creating a new user with default avatar
        user2 = CustomUser(username='testuser2', email='test2@example.com', is_student=True, college='MIT')
        user2.save()
        self.assertEqual(user2.user_avatar, 'user_profile/avatars/default.jpg')        

class RegisterUserFormTestCase(TestCase):
    def test_register_user_form(self):
    # Test that the form requires all required fields
        form_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'date_of_birth': '',
            'gender': '',
            'password1': '',
            'password2': '',}
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)

        # Test that the form requires the password fields to match
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'date_of_birth': '1995-01-01',
            'gender': 'M',
            'password1': 'abcdefg',
            'password2': 'hijklmn',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('password2', form.errors)

        # Test an invalid form submission
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': '',  # Email is required
            'date_of_birth': '1999-01-01',
            'gender': 'M',
            'college': 'Test College',
            'major': 'Test Major',
            'password1': 'testpass',
            'password2': 'testpass',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


   


        # Test a valid form submission
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'date_of_birth': '1999-01-01',
            'gender': 'M',
            'college': 'Test College',
            'major': 'Test Major',
            'password1': 'test1298',
            'password2': 'test1298',
        }
        form = RegisterUserForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        user = form.save()

        # Test an invalid form submission with mismatched passwords
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'date_of_birth': '1999-01-01',
            'gender': 'M',
            'college': 'Test College',
            'major': 'Test Major',
            'password1': 'testpass',
            'password2': 'incorrectpass',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        # Test that the form saved the data correctly
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.date_of_birth, datetime.date(1999, 1, 1))
        self.assertEqual(user.gender, 'M')
        self.assertTrue(user.check_password('test1298'))

class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        username='testuser',
        first_name='Test',
        last_name='User',
        email='test@example.com',
        date_of_birth='1999-01-01',
        gender='M',
        college='Test College',
        major='Test Major',
        password='test1298', )
        self.user.save()  # Save the user to the database

        self.blog = Blog.objects.create(
            user=self.user,
            title='Test Blog',
            description ='This is a test blog post.',
            date = datetime.datetime.now())


        self.project = Project.objects.create(
            user=self.user,
            title='Test Project',
            description='This is a test project.',
            image = 'media/default.jpg')
            

    def test_user_profile_view(self):
        

        # Test authenticated access
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_profile', kwargs={'user_id': self.user.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        
        




        
        self.assertEqual(response.context['blogs'][0], self.blog)
        self.assertEqual(response.context['projects'][0], self.project)
        self.assertEqual(response.context['user'], self.user)
        self.assertTemplateUsed(response, 'user_profile.html')

        # Check that the username is present in the response
        self.assertContains(response, self.user.username)



