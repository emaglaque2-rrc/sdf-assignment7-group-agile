"""This module provides unit tests for the Class data processor.
"""

__author__ = "Neil Tolentino"
__version__ = "0.11.2024"

import unittest
from unittest import TestCase
from data_processor.data_processor import DataProcessor

class TestDataProcessor(TestCase):
    """Defines the unit tests for the DataProcessor class."""

    def setUp(self):
        """This function is invoked before executing a unit test
        function.

        The following class attribute has been provided to reduce the 
        amount of code needed when creating DataProcessor class objects 
        in the tests that follow.
        
        Example:
            >>> data_processor = DataProcessor(self.transactions)
        """
        self.account1_deposit_transaction1 = {
            "Transaction ID": "1",
            "Account number": "1001",
            "Date": "2023-03-01",
            "Transaction type": "deposit",
            "Amount": 1000,
            "Currency": "CAD",
            "Description": "Salary"
        }

        self.account2_deposit_transaction1 = {
            "Transaction ID": "2",
            "Account number": "1002",
            "Date": "2023-03-01",
            "Transaction type": "deposit",
            "Amount": 1500,
            "Currency": "CAD",
            "Description": "Salary"
        }

        self.account1_withdraw_transaction1 = {
            "Transaction ID": "3",
            "Account number": "1001",
            "Date": "2023-03-02",
            "Transaction type": "withdrawal",
            "Amount": 300,
            "Currency": "CAD",
            "Description": "Groceries"
        }

        self.transactions = [
            self.account1_deposit_transaction1, 
            self.account2_deposit_transaction1
        ]

    # Define unit test functions below

    ## Update account summary tests

    def test_update_account_summary_dict_deposit_transaction(self):
        """Test the update_account_summary creates entry in account
        summary list for deposit transaction when account number
        does not exist.
        """

        #Arrange
        data_processor = DataProcessor([])    
        deposit_transaction = self.account1_deposit_transaction1        
        expected_number_of_entries = 1 
        account_number = deposit_transaction["Account number"]
        expected_entry = {           
            "account_number": account_number,
            "balance": 1000,
            "total_deposits": 1000,
            "total_withdrawals": 0
        }

        # Act
        data_processor.update_account_summary(deposit_transaction)
        result = data_processor.account_summaries

        # Assert
        # There should be 1 entry in the account summaries list
        self.assertEqual(len(result), expected_number_of_entries)
        # The Entry should be dict entry
        self.assertEqual(result[account_number], expected_entry)

    def test_update_account_summary_dict_withdrawal_transaction(self):
        """Test the update_account_summary creates an entry in the
        account summary list for withdraw transaction when account
        number does not exist.
        """

        # Arrange
        data_processor = DataProcessor([])    
        withdrawal_transaction = self.account1_withdraw_transaction1                   
        expected_number_of_entries = 1 
        account_number = withdrawal_transaction["Account number"]
        expected_entry = {           
            "account_number": account_number,
            "balance": -300,
            "total_deposits": 0,
            "total_withdrawals": 300
        }

        # Act
        data_processor.update_account_summary(withdrawal_transaction)
        result = data_processor.account_summaries

        # Assert
        # There should be 1 entry in the account summaries list
        self.assertEqual(len(result), expected_number_of_entries)
        # The entry should be dict entry
        self.assertEqual(result[account_number], expected_entry)

    ## Check suspicious transactions tests

    def test_check_suspicious_transactions_deposit_exceeds_threshold(self):
        """Test check_suspicious_transactions adds a deposit transaction
        as suspicious when amount exceeds the threshold.
        """

        # Arrange
        data_processor = DataProcessor([])       
        suspicious_transaction = self.account1_deposit_transaction1
        suspicious_transaction["Amount"] = 10001        
        expected_number_of_entries = 1 
        expected_entry = suspicious_transaction

        # Act
        data_processor.check_suspicious_transactions(suspicious_transaction)
        result = data_processor.suspicious_transactions

        # Assert
        # There should be 1 entry in the suspicious transaction list
        self.assertEqual(len(result), expected_number_of_entries)
        # The entry should be dict entry
        self.assertEqual(result[0], expected_entry)

    def test_check_suspicious_transactions_withdraw_exceeds_threshold(self):
        """Test the check_suspicious_transactions adds a withdrawal
        transaction as suspicious when the amount exceeds the threshold.
        """

         # Arrange
        data_processor = DataProcessor([])       
        suspicious_transaction = self.account1_withdraw_transaction1
        suspicious_transaction["Amount"] = 20000        
        expected_number_of_entries = 1 
        expected_entry = suspicious_transaction

        # Act
        data_processor.check_suspicious_transactions(suspicious_transaction)
        result = data_processor.suspicious_transactions

        # Assert
        # There should be 1 entry in the suspicious transactions list
        self.assertEqual(len(result), expected_number_of_entries)
        # The entry should be a dict entry
        self.assertEqual(result[0], expected_entry)

    def test_check_suspicious_transactions_uncommon_currency(self):
        """Test the check_suspicious_transaction adds a transaction
        as a suspicious when the currency is uncommon.
        """

        # Arrange
        data_processor = DataProcessor([]) 
        suspicious_transactions = []
        for currency in data_processor.UNCOMMON_CURRENCIES:
            suspicious_transaction = {
                "Transaction ID": "3",
                "Account number": "1001",
                "Date": "2023-03-02",
                "Transaction type": "withdrawal",
                "Amount": 300,
                "Currency": currency,
                "Description": "Crypto Investment"
            }

            suspicious_transactions.append(suspicious_transaction)            
        expected_number_of_entries = len(data_processor.UNCOMMON_CURRENCIES)

        # Act
        for transaction in suspicious_transactions:
            data_processor.check_suspicious_transactions(transaction)
        result = data_processor.suspicious_transactions

        # Assert
        # There should be 2 entry in the suspicious transaction list
        self.assertEqual(len(result), expected_number_of_entries)
        # The entries should be the expected dict entries
        for i in range(len(result)):
            self.assertEqual(result[i], suspicious_transactions[i])

    def test_check_suspicious_transactions_not_suspicious_transactions(self):
        """Test check_suspicious_transaction does not add transaction
        as suspicious when amount exceeds threshold and currency is
        uncommon.
        """

        # Arrange
        data_processor = DataProcessor([])       
        legit_transaction = self.account1_deposit_transaction1
        expected_number_of_entries = 0 
        
        # Act
        data_processor.check_suspicious_transactions(legit_transaction)
        result = data_processor.suspicious_transactions

        # Assert
        # There should be no entries in the suspicious transactions list
        self.assertEqual(len(result), expected_number_of_entries)
    
    ## Update transaction statistics tests

    def test_update_transaction_statistics_captures_normal_transaction(self):
        """Test update_transaction_statistics captures a normal transaction.
        """
        # Arrange
        data_processor = DataProcessor([])       
        normal_transaction = self.account1_deposit_transaction1
        transaction_type = normal_transaction["Transaction type"]
        expected_number_of_entries = 1 
        expected_entry = {
            "total_amount": normal_transaction["Amount"],
            "transaction_count": expected_number_of_entries
        }

        # Act
        data_processor.update_transaction_statistics(normal_transaction)
        result = data_processor.transaction_statistics

        # Assert
        # There should be 1 entry in the transaction statistics list
        self.assertEqual(len(result), expected_number_of_entries)
        # The entry should be expected dict entry
        self.assertEqual(result[transaction_type], expected_entry)

if __name__ == "__main__":
    unittest.main()
