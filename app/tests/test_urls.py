from django.test import SimpleTestCase
from django.urls import reverse,resolve
from app.views import Scholarship,SmmaryDataBank,AdminHome,InvestorHome

class TestUrls(SimpleTestCase):
    def test_SmmaryData_url_resolves(self):
        url=reverse('SmmaryDataBank')
        self.assertEqual(resolve(url).func,SmmaryDataBank)


    def test_Scholarship_url_resolves(self):
        url=reverse('Scholarship')
        self.assertEqual(resolve(url).func,Scholarship)



    def test_AdminHome_url_resolves(self):
        url=reverse('AdminHome')
        self.assertEqual(resolve(url).func,AdminHome)



    def test_InvestorHome_url_resolves(self):
        url=reverse('InvestorHome')
        self.assertEqual(resolve(url).func,InvestorHome)