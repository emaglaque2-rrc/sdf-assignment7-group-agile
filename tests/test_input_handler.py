"""This module defines the tests for the InputHandler class."""

__author__ = "Edraque Maglaque"
__version__ = "0.11.2024"

import unittest
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import mock_open
from csv import DictReader
from json import loads
from input_handler.input_handler import InputHandler

class InputHandlerTests(TestCase):
    """Defines the unit tests for the InputHandler class."""

    def setUp(self):
        self.FILE_CONTENTS = \
            ("Transaction ID,Account number,Date,Transaction type,"
            + "Amount,Currency,Description\n"
            + "1,1001,2023-03-01,deposit,1000,CAD,Salary\n"
            + "2,1002,2023-03-01,deposit,1500,CAD,Salary\n"
            + "3,1001,2023-03-02,withdrawal,200,CAD,Groceries")
        
        # Imitates the self.FILE_CONTENTS sample, but in json format for sample data
        # for unit tests. Gets rid of file content/system dependency of the unit test.
        self.MOCKED_JSON_CONTENTS = '''
        [
            {
                "Transaction ID": 1,
                "Account number": 1001,
                "Date": "2023-03-01",
                "Transaction type": "deposit",
                "Amount": 1200,
                "Currency": "CAD",
                "Description": "Salary"
            },
            {
                "Transaction ID": 2,
                "Account number": 1002,
                "Date": "2023-03-01",
                "Transaction type": "deposit",
                "Amount": 1800,
                "Currency": "CAD",
                "Description": "Salary"
            }
        ]
        '''

    ### get_file_format() Test

    def test_get_file_format_returns_file_extension_of_file_path(self):
        # Arrange
        test_file = InputHandler("example.csv")

        # Act
        actual = test_file.get_file_format()

        # Assert
        expected = "csv"
        self.assertEqual(expected, actual)

    ### read_csv_data() Tests

    def test_read_csv_data_raises_FileNotFoundError_when_file_path_invalid(self):
        # Arrange
        test_file = InputHandler("test.test")

        # Act
        with self.assertRaises(FileNotFoundError) as context:
            test_file.read_csv_data()

        # Assert
        expected = f"File: test.test does not exist."
        actual = str(context.exception)
        self.assertEqual(expected, actual)

    def test_read_csv_data_returns_list_containing_transaction_data_from_csv_file(self):
        # Arrange
        # Placeholder, won't actually be read and so it doesn't raise exception.
        input_handler = InputHandler("input/input_data.csv")

        # Act
        # Mocks the open() function, and reads the self.FILE_CONTENTS
        # Patch used to not raise exception and for it to have less dependencies.
        with \
        patch("os.path.isfile", return_value=True), \
        patch("builtins.open", mock_open(read_data = self.FILE_CONTENTS)):          
            actual_list = input_handler.read_csv_data()

        # Assert
        expected_list = [
            {
                "Transaction ID": row["Transaction ID"],
                "Account number": row["Account number"],
                "Date": row["Date"],
                "Transaction type": row["Transaction type"],
                "Amount": row["Amount"],
                "Currency": row["Currency"],
                "Description": row["Description"]
            }
            # DictReader used so no hard-coding; it's more scalable and less error-prone.
            for row in DictReader(self.FILE_CONTENTS.splitlines())
        ]

        self.assertListEqual(expected_list, actual_list)
        
    ### read_input_data() Tests

    def test_read_input_data_returns_list_containing_transaction_data_from_csv_file(self):
        # Arrange
        input_handler = InputHandler("input/input_data.csv")

        # Act
        # Patch used to not raise exception and for it to have less dependencies.
        with \
        patch("os.path.isfile", return_value=True), \
        patch("builtins.open", mock_open(read_data = self.FILE_CONTENTS)):
            actual_list = input_handler.read_input_data()

        # Assert
        expected_list = [
            {
                "Transaction ID": row["Transaction ID"],
                "Account number": row["Account number"],
                "Date": row["Date"],
                "Transaction type": row["Transaction type"],
                "Amount": row["Amount"],
                "Currency": row["Currency"],
                "Description": row["Description"]
            }
            for row in DictReader(self.FILE_CONTENTS.splitlines())
        ]

        self.assertListEqual(expected_list, actual_list)

    def test_read_input_data_returns_list_containing_transaction_data_from_json_file(self):
        # Arrange
        input_handler = InputHandler("input/input_data.json")
        # Loads function parses the mocked json content in setUp into a python 
        # list which I can utilize to dynamically construct expected_list.
        mocked_file_contents = loads(self.MOCKED_JSON_CONTENTS)

        # Act
        # Patch used to not raise exception and for it to have less dependencies.
        with \
        patch("os.path.isfile", return_value=True), \
        patch("builtins.open", mock_open(read_data = self.MOCKED_JSON_CONTENTS)):        
            actual_list = input_handler.read_input_data()

        # Assert
        expected_list = [
            {
                "Transaction ID": item["Transaction ID"],
                "Account number": item["Account number"],
                "Date": item["Date"],
                "Transaction type": item["Transaction type"],
                "Amount": item["Amount"],
                "Currency": item["Currency"],
                "Description": item["Description"]
            }
            # This is dynamically structured so I don't have to hard-code every
            # data for comparison, more scalable and less error-prone.
            for item in mocked_file_contents
        ]

        self.assertListEqual(expected_list, actual_list)
        
    def test_read_input_data_returns_empty_list_if_file_is_not_csv_or_json(self):
        # Arrange
        input_handler = InputHandler("unsupported_file.gojetsgo")

        # Act
        # Patch used to not raise exception and for it to have less dependencies.
        with patch("os.path.isfile", return_value = True):
            actual_list = input_handler.read_input_data()

        # Assert
        expected_list = []
        self.assertEqual(expected_list, actual_list)

if __name__ == "__main__":
    unittest.main()
