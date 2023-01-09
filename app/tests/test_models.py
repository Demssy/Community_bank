from django.test import TestCase
from app.models import SmmaryDataBank,Scholarship


class TestModels(TestCase):
    def setUp(self):
        self.project1=Scholarship.objects.create(
            name='project1',
            app=1000
        )

    def test_scholarship_delete(self):
        self.assertEqual(self.project1.delete,'project1')

