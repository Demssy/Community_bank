from urllib.parse import urlencode
from django.test import TestCase, tag ,Client
from accounts.models import CustomUser
from django.urls import reverse
from app.models import Scholarship,SmmaryDataBank
from blog.models import Blog
import json
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


    def test_SmmaryData(self):
        client=Client()
        response=client.get(reverse('SmmaryDataBank'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'app/SmmaryDataBank.html')

    def test_Scholarship(self):
        client = Client()
        response = client.get(reverse('Scholarship'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/Scholarship.html')


    def test_detail(self):
        client = Client()
        response = client.get(reverse('detail',args=['detailProject']))
        Blog.objects.create(name='detailProject',app=1000)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')


    #def test_detail_POST(self):



    def test_AdminHome(self):
        client=Client()
        response=client.get(reverse('AdminHome'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'app/admin/AdminHome.html')


    def test_InvestorHome(self):
        client=Client()
        response=client.get(reverse('InvestorHome'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'app/investor/InvestorHome.html')

