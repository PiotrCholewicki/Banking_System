import unittest
from utils.validators import validate_amount


class TestValidators(unittest.TestCase):

    def test_correct_data(self):
        result = validate_amount(1000)
        self.assertTrue(result)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            validate_amount(-5)

    def test_non_number(self):
        with self.assertRaises(TypeError):
            validate_amount("abc")



