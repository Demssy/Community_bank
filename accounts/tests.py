import datetime
import os
from django.contrib.auth import get_user_model
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
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Scholarship
class CustomUserTestCase(TestCase):
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
        user_avatar='default.jpg')
             

        self.user.save()

    def test_create_user(self):
        # Test that the user is created successfully
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.college, 'SCE')
        self.assertEqual(self.user.major, 'CE')
        self.assertEqual(self.user.gender, 'M')
        self.assertEqual(self.user.date_of_birth, '1998-01-01')
        self.assertEqual(self.user.bio, 'This is a test user for unit testing')
        self.assertEqual(self.user.is_student, True)
        self.assertEqual(self.user.is_investor, False)
        self.assertEqual(self.user.user_avatar, 'default.jpg')

    def test_delete(self):
        # Test that the user and the user's avatar are deleted successfully
        user_avatar_path = self.user.user_avatar.path
        self.user.delete()
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertFalse(os.path.exists(user_avatar_path))

    def test_str(self):
        # Test that the __str__ method returns the correct string
        self.assertEqual(str(self.user), 'testuser')


    def test_save_is_student(self):
        # Test that the `is_student` field is set to True when the `college` field is filled in
        self.user.college = ''
        self.user.save()
        self.assertEqual(self.user.is_student, False)

        self.user.college = 'SCE'
        self.user.save()
        self.assertEqual(self.user.is_student, True)

    def test_get_absolute_url(self):
        # Test that the get_absolute_url method returns the correct URL
        self.assertEqual(self.user.get_absolute_url(), '/user_profile/1/')

    def test_is_investor_field_false(self):
        # Test that the `is_investor` field is set to True when the `mailing_address` field is filled in
        self.user.mailing_address = '123 Test St'
        self.user.save()
        self.assertFalse(self.user.is_investor, True)

           

class RegisterUserFormTestCase(TestCase):
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

    def test_form_valid(self):
        form_data = {
            'username': 'testuser2',
            'email': 'test2@email.com',
            'first_name': 'Test2',
            'last_name': 'User2',
            'college': 'HEBR',
            'major': 'CE',
            'gender': 'M',
            'date_of_birth': '1990-01-01',
            'password1': 'testpass2',
            'password2': 'testpass2',
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'username': 'testuser2',
            'email': 'test@email.com',
            'first_name': 'Test2',
            'last_name': 'User2',
            'college': 'SCE',
            'major': 'CE',
            'gender': 'M',
            'date_of_birth': '1990-01-01',
            'password1': 'testpass2',
            'password2': 'testpass3',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'password2': ['Passwords do not match']})

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
        self.assertEqual(len(form.errors), 9)

        # Test that the form requires the password fields to match
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'date_of_birth': '1995-01-01',
            'college': 'SCE',
            'major': 'CE',
            'gender': 'M',
            'password1': 'abcdefg',
            'password2': 'hijklmn',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('password2', form.errors)

        # Test an invalid form submission
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': '',  # Email is required
            'date_of_birth': '1999-01-01',
            'gender': 'M',
            'college': 'SCE',
            'major': 'CE',
            'password1': 'testpass',
            'password2': 'testpass',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


   


        # Test a valid form submission
        form_data = {
            'username': 'testuser11',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',  # Email is required
            'date_of_birth': '1999-01-01',
            'gender': 'M',
            'college': 'SCE',
            'major': 'CE',
            'password1': 'testpass1298',
            'password2': 'testpass1298',
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
            'college': 'SCE',
            'major': 'CE',
            'password1': 'testpass',
            'password2': 'incorrectpass',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        # Test that the form saved the data correctly
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(user.username, 'testuser11')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.date_of_birth, datetime.date(1999, 1, 1))
        self.assertEqual(user.gender, 'M')
       

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



