from django.test import  TestCase

from app.calc import add, substract



class Calctests(TestCase):

    def test_add_numbers(self):
        """
        Test that two numbers are added together
        :return: 
        """
        self.assertEqual(add(3,8), 11)


    def test_subtract_numbers(self):
        """
        Test that values are subtracted and returned
        :return: 
        """
        self.assertEqual(substract(5,11), 6)
