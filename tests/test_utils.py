import unittest
from src.utils.parsing import parse_input, format_output

class TestUtils(unittest.TestCase):

    def test_parse_input(self):
        # Test cases for parse_input function
        self.assertEqual(parse_input("Hello, how are you?"), "Hello, how are you?")
        self.assertEqual(parse_input(""), "")
        self.assertEqual(parse_input("12345"), "12345")

    def test_format_output(self):
        # Test cases for format_output function
        self.assertEqual(format_output("Hello!"), "Formatted: Hello!")
        self.assertEqual(format_output(""), "Formatted: ")
        self.assertEqual(format_output("Goodbye!"), "Formatted: Goodbye!")