"""This module defines the OutputHandler class."""

__author__ = "Alyssa Urquiola"
__version__ = "0.11.24"

import csv

class OutputHandler:
    """A class to handle the CSV reports for account summaries,
    suspicious transactions, and transaction statistics.

    Attributes:
        account_summaries (dict): A dictionary of valid account summaries
        suspicious_transactions (list): A list of suspicious transactions
        transaction_statistics (dict): A dictionary of dictionaries
        containing summary data
    """

    def __init__(self, account_summaries: dict, 
                       suspicious_transactions: list, 
                       transaction_statistics: dict):
        """Initializes an output handler instance with appropriate data.

        Args: 
            account_summaries (dict): A dictionary of account summaries
            suspicious_transactions (list): A list of dictionaries representing
            suspicious transactions
            transaction_statistics (dict): A dictionary containing keys
            (transaction types) and values (summary data)
        """
        # Represents the object parameters.
        self.__account_summaries = account_summaries
        self.__suspicious_transactions = suspicious_transactions
        self.__transaction_statistics = transaction_statistics 
    
    # Accessors for account summaries.
    @property
    def account_summaries(self) -> dict:
        """Gets the account summaries.

        Args:
            account_summaries (dict): A dictionary of valid account summaries

        Returns:
            dict: A dictionary of account summaries with account numbers
            as keys and the account details as the values.        
        """
        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """Gets the suspicious transactions.

        Args:
            suspicious_transactions (list): A list of dictionaries obtaining
            suspicious transactions

        Returns:
            list: A list of dictionaries that contains suspicious transactions
            including 'Transaction ID', 'Account number', 'Date',
            'Transaction type', 'Amount', 'Currency', and 'Description'.
        """
        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """Gets the transaction statistics.

        Args:
            transaction_statistics (dict): A dictionary containing
            'Transaction type', 'Total amount', and 'Total count'.

        Returns:
            dict: A dictionary where each key is a transaction type
            ('deposit', 'withdrawal'), and each value contains the
            account details ('total_amount', 'transaction_count').
        """
        return self.__transaction_statistics

    def write_account_summaries_to_csv(self, file_path: str) -> None:
        """Writes the account summaries to a CSV file with the expected number
        of rows, including header row.

        Args:
            file_path (str): The path to the CSV file for the account summaries.

        Returns:
            expected_content: 'Account number', 'Balance', 'Total Deposits',
            'Total Withdrawals'.
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow([
                "Account number", 
                "Balance", 
                "Total Deposits", 
                "Total Withdrawals"
            ])

            for account_number, summary in self.__account_summaries.items():
                writer.writerow([
                    account_number,
                    summary["balance"],
                    summary["total_deposits"],
                    summary["total_withdrawals"]
                ])

    def write_suspicious_transactions_to_csv(self, file_path: str) -> None:
        """Writes the suspicious transactions to the CSV file with the expected
        number of rows, including header row.

        Args:
            file_path (str): The path to the CSV file for the suspicious transactions.

        Returns:
            expected_content: 'Transaction ID', 'Account number', 'Date',
            'Transaction type', 'Amount', 'Currency', 'Description'.
        """
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow([
                "Transaction ID", 
                "Account number", 
                "Date", 
                "Transaction type", 
                "Amount", 
                "Currency", 
                "Description"
            ])

            for transaction in self.__suspicious_transactions:
                writer.writerow([
                    transaction["Transaction ID"],
                    transaction["Account number"],
                    transaction["Date"],
                    transaction["Transaction type"],
                    transaction["Amount"],
                    transaction["Currency"],
                    transaction["Description"]
                ])

    def write_transaction_statistics_to_csv(self, file_path: str) -> None:
        """Writes the transaction statistics data to a CSV file.

        Args:
            file_path (str): The path to the CSV file for the transaction statistics.

        Returns:
            expected_content: 'Transaction type', 'Total amount', 'Transaction count'.
        """        
        with open(file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow([
                "Transaction type", 
                "Total amount", 
                "Transaction count"
            ])

            for transaction_type, statistic in self.__transaction_statistics.items():
                writer.writerow([
                    transaction_type,
                    statistic["total_amount"],
                    statistic["transaction_count"]
                ])
