import unittest
from main import parse_config, parse_value

class TestConfigParser(unittest.TestCase):
    def test_parse_global_constants(self):
        text = """
        global port = 8080;
        global host = @"localhost";
        """
        expected = {
            "port": 8080,
            "host": "localhost"
        }
        self.assertEqual(parse_config(text), expected)

    def test_parse_dictionary(self):
        text = """
        {
            document_root = @"/var/www/html"
            max_clients = 100
        }
        """
        expected = {
            "document_root": "/var/www/html",
            "max_clients": 100
        }
        self.assertEqual(parse_config(text), expected)

    def test_parse_mixed_globals_and_dictionary(self):
        text = """
        global port = 8080;
        {
            document_root = @"/var/www/html"
            max_clients = 50
        }
        """
        expected = {
            "port": 8080,
            "document_root": "/var/www/html",
            "max_clients": 50
        }
        self.assertEqual(parse_config(text), expected)

    def test_parse_value_integer(self):
        self.assertEqual(parse_value("42"), 42)

    def test_parse_value_string(self):
        self.assertEqual(parse_value('@"Hello World"'), "Hello World")

    def test_invalid_syntax(self):
        text = "global name value;"
        with self.assertRaises(SyntaxError):
            parse_config(text)

    def test_invalid_value(self):
        with self.assertRaises(ValueError):
            parse_value("invalid_value")

if __name__ == "__main__":
    unittest.main()
