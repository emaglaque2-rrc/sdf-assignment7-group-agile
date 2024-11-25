"""This module defines the processing of the input data, 
updating account summaries, checking and maintaining
transactions and statistics while implementing a
configurable logging mechanism.
"""

__author__ = "Neil Tolentino"
__version__ = "0.11.2024"

class DataProcessor:
    """Represents the financial transactions data,
    suspicious transactions, and transaction statistics.
    """

    LARGE_TRANSACTION_THRESHOLD = 10000
    """A constant that sets the maximum transaction amount.
    """

    UNCOMMON_CURRENCIES = ["XRP", "LTC"]
    """A constant that checks transactions with uncommon currencies.
    """

    def __init__(self, transactions: list):
        """Initializes account transactions and statistics.

        Returns:
            list: The account transactions and statistics.
        """
        self.__transactions = transactions
        self.__account_summaries = {}
        self.__suspicious_transactions = []
        self.__transaction_statistics = {}

    @property
    def input_data(self) -> list:
        """Gets the input data.

        Returns:
            list: The list of transactions passed into the constructor.
            """
        return self.__transactions
    
    @property
    def account_summaries(self) -> dict:
        """Gets the account transaction summary.

        Returns:
            dict: all account transaction summaries as a dictionary.
        """
        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """Gets the suspicious account transactions.

        Returns: 
            list: all the list of suspicious transactions.
        """
        return self.__suspicious_transactions
    
    @property
    def transaction_statistics(self) -> dict:
        """Gets the account transaction statistics.

        Returns:
            dict: all account transactions statistics as a dictionary.
        """
        return self.__transaction_statistics

    def process_data(self) -> dict:
        """Process the input transaction statitistics as a dictionary.
        Then generate account summaries, suspicious transactions, and
        transaction statistics.

        Returns:
            dict: dictionary containing account summaries,suspicious
            transactions, and transaction statistics.
        """
        for transaction in self.__transactions:
            self.update_account_summary(transaction)
            self.check_suspicious_transactions(transaction)
            self.update_transaction_statistics(transaction)

        return {
            "account_summaries": self.__account_summaries,
            "suspicious_transactions": self.__suspicious_transactions,
            "transaction_statistics": self.__transaction_statistics
        }

    def update_account_summary(self, transaction: dict) -> None:
        """Updates or creates account transactions summary.

        Args:
            transaction (dict): transaction to be processed.

        Returns:
            dict: Updated account transaction summary.
        """
        account_number = transaction["Account number"]
        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        if account_number not in self.__account_summaries:
            self.__account_summaries[account_number] = {
                "account_number": account_number,
                "balance": 0,
                "total_deposits": 0,
                "total_withdrawals": 0
            }

        if transaction_type == "deposit":
            self.__account_summaries[account_number]["balance"] += amount
            self.__account_summaries[account_number]["total_deposits"] += amount
        elif transaction_type == "withdrawal":
            self.__account_summaries[account_number]["balance"] -= amount
            self.__account_summaries[account_number]["total_withdrawals"] += amount

    def check_suspicious_transactions(self, transaction: dict) -> None:
        """Checks if transactions is suspicious based on the amount and
        currency.

        Args:
            transaction (dict): transaction to be processed.
        """
        amount = float(transaction["Amount"])
        currency = transaction["Currency"]

        if amount > self.LARGE_TRANSACTION_THRESHOLD \
            or currency in self.UNCOMMON_CURRENCIES:
            self.__suspicious_transactions.append(transaction)

    def update_transaction_statistics(self, transaction: dict) -> None:
        """Updates account transaction statistics.

        Args:
            transaction (dict): transaction to be processed.
        """
        transaction_type = transaction["Transaction type"]
        amount = float(transaction["Amount"])

        if transaction_type not in self.__transaction_statistics:
            self.__transaction_statistics[transaction_type] = {
                "total_amount": 0,
                "transaction_count": 0
            }

        self.__transaction_statistics[transaction_type]["total_amount"] += amount
        self.__transaction_statistics[transaction_type]["transaction_count"] += 1

    def get_average_transaction_amount(self, transaction_type: str) -> float:
        """Gets the average transaction amount for the given transaction
        type.

        Args:
            transaction_type (str): The type of transaction.

        Returns:
            float: average transaction amount or zero if there is nothing found.
        """
        total_amount = self.__transaction_statistics[transaction_type]["total_amount"]
        transaction_count = self.__transaction_statistics[transaction_type]["transaction_count"]
    
        return 0 if transaction_count == 0 else total_amount / transaction_count
