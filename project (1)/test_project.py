import unittest
from project import app, caracters, history, writehistory
from flask_testing import TestCase
import tempfile
import csv


class TestProject(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # test valid input city
    def test_fetch_valid(self):
        response = self.client.get("/?city=Amsterdam")
        self.assert200(response)
        self.assert_template_used('index.html')
        self.assert_context('current_city', 'Amsterdam')

    # test invalid input country
    def test_fetch_invalid(self):
        response = self.client.get("/?city=Germany")
        self.assert200(response)
        self.assert_template_used('index.html')
        self.assert_context('error_message', 'Please enter a valid city')
        self.assert_context('current_city', 'Amsterdam')

    # test invalid input city
    def test_invalid_characters_input(self):
        response = self.client.get("/?city=1234")
        self.assert200(response)
        self.assert_template_used('index.html')
        self.assert_context('error_message', 'Please enter a valid city')
        self.assert_context('current_city', 'Amsterdam')

class TestCaractersFunction(unittest.TestCase):
    # set valid input
    def test_caracters_valid(self):
        valid_input = "Amsterdam"
        self.assertTrue(caracters(valid_input))

    # set invalid input
    def test_caracters_invalid(self):
        invalid_input = "1234"
        self.assertFalse(caracters(invalid_input))


class TestHistoryFunctions(unittest.TestCase):
    def setUp(self):
        # create temp file
        self.temp_csv_file = 'temp_history.csv'

    def tearDown(self):
        # delete temp file
        import os
        if os.path.exists(self.temp_csv_file):
            os.remove(self.temp_csv_file)

    def test_history(self):
        # trite data to temp csv
        with open(self.temp_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["City1"])
            writer.writerow(["City2"])

        # test history function
        result = history(self.temp_csv_file)

        # verify
        self.assertEqual(result, ["City1", "City2"])

    def test_writehistory(self):
        # set csv file path to temp file
        csv_file_path = self.temp_csv_file

        # test writehistory function
        writehistory("Berlin", csv_file_path)

        # read contents temp file
        with open(csv_file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            content = [row[0] for row in reader if row]

        # verify
        self.assertIn("Berlin", content)

if __name__ == '__main__':
    unittest.main()
