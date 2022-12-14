from django.test import TestCase

class MyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # This method is run only once, before any other test.
        # It's purpose is to set data needed on a class-level.
        print('setUpTestData')

    def setUp(self):
        # This method is run before each test.
        print('setUp')

    def tearDown(self):
        # This method is run after each test.
        print('tearDown')

    def test_my_first_method(self):
        # This method should perform a test.
        print('test_my_first_method')
        self.assertTrue(True)

    def test_my_second_method(self):
        # This method should perform a test.
        print('test_my_second_method')
        self.assertFalse(False)
