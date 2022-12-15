from urllib.parse import urlencode
from django.test import TestCase, tag
from accounts.models import CustomUser

class MyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # This method is run only once, before any other test.
        # It's purpose is to set data needed on a class-level.
        user = CustomUser(username = 'tom', password = 'tom12345')
        user.save()


        user = CustomUser.objects.get(username='tom')
        print('Added user data : ')
        print(user)
        print('')


        return
        

    def setUp(self):
        # This method is run before each test.
        print('setUp')

    def tearDown(self):
        # This method is run after each test.
        print('tearDown')

    def test_get_login(self):
        response = self.client.get('/login/')
       
        self.assertEqual(response.status_code, 200)


    @tag('unit-test')
    def test_login_user(self):
        #data = urlencode({'username':'tom', 'password': 'tom'})
        login = self.client.login(username = 'tom', password = 'tom12345')

        print('is login possible ',login)
        self.assertFalse(login)