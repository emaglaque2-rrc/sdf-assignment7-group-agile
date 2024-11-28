"""
Description: A script that defines and runs tests by using the
unittest framework for testing the properties and methods of
the OutputHandler class.
Author: Alyssa Urquiola
Date: 2024-11-22
Usage: To run the tests for the OutputHandler class and execute
the script from the command line using python test_output_handler.py
"""

from unittest import TestCase, main
from output_handler.output_handler import OutputHandler
from unittest.mock import patch, mock_open, call

class TestOutputHandler(TestCase):
    """Unit test class for OutputHandler class."""

    def setUp(self):
        # Test data for account summaries
        self.account_summaries = { 
            "1001": {
                "account_number": "1001", 
                "balance": 50, 
                "total_deposits": 100, 
                "total_withdrawals": 50
            },
            "1002": {
                "account_number": "2", 
                "balance": 200, 
                "total_deposits": 200, 
                "total_withdrawals": 0
            }
        }

        # Test data for suspicious transactions
        self.suspicious_transactions = [
            {
                "Transaction ID": "1",
                "Account number": "1001",
                "Date": "2023-03-14",
                "Transaction type": "deposit",
                "Amount": 250,
                "Currency": "XRP",
                "Description": "crypto investment"
            }
        ]

        # Test data for self transaction statistics
        self.transaction_statistics = {
            "deposit": {
                "total_amount": 300, 
                "transaction_count": 2
            }, 
            "withdrawal": {
                "total_amount": 50, 
                "transaction_count": 1
            }
        }

        # Represents the OutputHandler instance with test data
        self.handler = OutputHandler(
            self.account_summaries,
            self.suspicious_transactions,
            self.transaction_statistics
        )

    def test_initialization(self):
        # Arrange
        account_summaries = self.account_summaries
        suspicious_transactions = self.suspicious_transactions
        transaction_statistics = self.transaction_statistics

        # Assert
        self.assertEqual(self.handler.account_summaries,
                         self.account_summaries)
        self.assertEqual(self.handler.suspicious_transactions,
                         self.suspicious_transactions)
        self.assertEqual(self.handler.transaction_statistics,
                         self.transaction_statistics)

    def test_account_summaries_property(self):
        # Arrange
        expected = self.account_summaries

        # Assert - returns the current state
        self.assertEqual(self.handler.account_summaries, expected)

    def test_suspicious_transactions_property(self):
        # Arrange
        expected = self.handler.suspicious_transactions

        # Assert - returns the current state
        self.assertEqual(expected, self.suspicious_transactions)
    
    def test_transaction_statistics_property(self):
        # Arrange
        expected = self.handler.transaction_statistics

        # Assert - returns the current state
        self.assertEqual(expected, self.transaction_statistics)

    def test_write_account_summaries_to_csv(self):
        # Arrange
        file_path = "output_data_account_summaries.csv"
        expected_file_content = (
            "Account number,Balance,Total Deposits,Total Withdrawals\r\n",
            "1001,50,100,50\r\n",
            "1002,200,200,0\r\n"
        )

        # Act
        with patch('builtins.open', mock_open()) as mocked_open:
            self.handler.write_account_summaries_to_csv(file_path)

            # Assert correct file path and mode
            mocked_open.assert_called_once_with(file_path, "w", newline="")

            # Get the mock file handle and check write calls
            mock_file_handle = mocked_open()
        
            # Check that the content written to the file matches expected values
            mock_file_handle.write.assert_any_call
            ("Account number,Balance,Total Deposits,Total Withdrawals\r\n")
            mock_file_handle.write.assert_any_call("1001,50,100,50\r\n")
            mock_file_handle.write.assert_any_call("1002,200,200,0\r\n")

            # Assert expected number of rows including the header row
            self.assertEqual(mock_file_handle.write.call_count,
                             len(expected_file_content))

    def test_write_suspicious_transaistions_to_csv(self):

        # Arrange
        file_path = "output_data_suspicious_transactions.csv"
        expected_file_content = (
            "Transaction ID,Account number,Date,Transaction type,Amount,Currency,Description\r\n",
            "1,1001,2023-03-14,deposit,250,XRP,crypto investment\r\n"
        )
        
        # Act
        with patch('builtins.open', mock_open()) as mocked_open:
            self.handler.write_suspicious_transactions_to_csv(file_path)

            # Assert correct file path and mode
            mocked_open.assert_called_once_with(file_path, "w", newline="")

            # Checks that the content written to the file matches expected values
            mock_file_handle = mocked_open()
            mock_file_handle.write.assert_any_call
            ("Transaction ID,Account number,Date,Transaction type,Amount,Currency,Description\r\n")
            mock_file_handle.write.assert_any_call
            ("1,1001,2023-03-14,deposit,250,XRP,crypto investment\r\n")

            # Assert expected number of rows including header row
            self.assertEqual(mock_file_handle.write.call_count, len(expected_file_content))

    def test_write_transaction_statistics_to_csv(self):
        # Arrange
        file_path = "output_data_transaction_statistics.csv"
        expected_file_content = (
            "Transaction type,Total amount,Transaction count\r\n",
            "deposit,300,2\r\n",
            "withdrawal,50,1\r\n"
        )

        # Act
        with patch('builtins.open', mock_open()) as mocked_open:
            self.handler.write_transaction_statistics_to_csv(file_path)

            # Assert correct file path and mode
            mocked_open.assert_called_once_with(file_path, "w", newline="")

            # Get the mock file handle and check write calls
            mock_file_handle = mocked_open()
            
            # Assert actual content
            written_calls = mock_file_handle.write.call_args_list

            # Print actual content being written for debugging purposes
            written_content = [call[0][0] for call in written_calls]
            print("Written Content: ", written_content)

            # Assert the number of write calls matches the expected content
            self.assertEqual(len(written_calls), len(expected_file_content))

            for expected_content in expected_file_content:
                self.assertIn(expected_content, written_content)

if __name__ == "__main__":
    main()
    