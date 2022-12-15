
from portfolio.models import Project
from django.test import TestCase
from accounts.models import CustomUser

class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # This method is run only once, before any other test.
        # It's purpose is to set data needed on a class-level.
        # below code will fix AttributeError: type object 'Model Test' has no attribute 'cls_atomics' error.
        super(ModelTest, cls).setUpClass()

         # create and save a Project object.
        proj = Project(title='python', description='Quality Assurance', user_id = 1)
        proj.save() 

        # create a User model object in temporary database.
        user = CustomUser(username='tom', password='tom')
        user.save()


         # get student user.
        user = CustomUser.objects.get(username='tom')
        print('Added user data : ')
        print(user)
        print('')

        # get student's project.
        proj = Project.objects.get(title='python')
        print('Added project data : ')
        print(proj)
        print('')

    def setUp(self):
        # This method is run before each test.
        print('setUp')

    def tearDown(self):
        #project = Project.objects.get(title= )
        print('tearDown')

    def test_project_get_from_db(self):
        # This method should perform a test.
        proj = Project.objects.get(title='python')
        self.assertEqual(proj.description, 'Quality Assurance')

    def test_abstract_user_models(self):
        # This method should perform a test.
        user = CustomUser.objects.get(username = 'tom')
        self.assertEqual(user.username, 'tomm')