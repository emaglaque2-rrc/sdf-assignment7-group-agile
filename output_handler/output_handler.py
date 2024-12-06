"""This module defines the OutputHandler class."""

__author__ = "Alyssa Urquiola"
__version__ = "0.11.24"

import csv
from io import StringIO
import os

class OutputHandler:
    """A class to handle the CSV reports for account summaries,
    suspicious transactions, and transaction statistics.

    Attributes:
        account_summaries (dict): A dictionary of valid account
        summaries
        suspicious_transactions (list): A list of suspicious
        transactions
        transaction_statistics (dict): A dictionary of dictionaries
        containing summary data
    """

    def __init__(self, account_summaries: dict, 
                       suspicious_transactions: list, 
                       transaction_statistics: dict):
        """Initializes an output handler instance with appropriate data.

        Args: 
            account_summaries (dict): A dictionary of account summaries
            suspicious_transactions (list): A list of dictionaries
            representing suspicious transactions
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
            account_summaries (dict): A dictionary of valid account
            summaries

        Returns:
            dict: A dictionary of account summaries with account numbers
            as keys and the account details as the values.        
        """
        return self.__account_summaries
    
    @property
    def suspicious_transactions(self) -> list:
        """Gets the suspicious transactions.

        Args:
            suspicious_transactions (list): A list of dictionaries
            obtaining suspicious transactions

        Returns:
            list: A list of dictionaries that contains suspicious
            transactions including 'Transaction ID', 'Account number',
            'Date', 'Transaction type', 'Amount', 'Currency', and
            'Description'.
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
        """Writes the account summaries to a CSV file with the expected
        number of rows, including header row.

        Args:
            file_path (str): The path to the CSV file for the account
            summaries.

        Returns:
            expected_content: 'Account number', 'Balance',
            'Total Deposits', 'Total Withdrawals'.
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
        """Writes the suspicious transactions to the CSV file with the
        expected number of rows, including header row.

        Args:
            file_path (str): The path to the CSV file for the suspicious
            transactions.

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
            file_path (str): The path to the CSV file for the
            transaction statistics.

        Returns:
            expected_content: 'Transaction type', 'Total amount',
            'Transaction count'.
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

    # Add Filtering Output Data
    def filter_account_summaries(self, filter_field: str, filter_value: int,
                                 filter_mode: bool) -> dict:
        """Filtering method for account summaries data based on the
        provided filter criteria.

        Args:
            filter_field (str): One of the following filter fields:
            "balance","total_deposits" or "total_withdrawals".
            filter_value (int): An integer value to which the filter
            field will be compared.
            filter_mode (bool): The mode to filter:
                - True: Filter by greater than or equal to the filter
                        value.
                - False: Filter by less than or equal filter value.

        Returns:
            dict: A list containing only the filtered account summaries.     
        """
        if filter_field not in ["balance", "total_deposits", "total_withdrawals"]:
            raise ValueError("Invalid filter field.")
        
        filtered_summaries = {}

        for account_number, summary in self.__account_summaries.items():
            account_value = summary.get(filter_field)

            # Apply filtering logic based on filter_mode
            if filter_mode:
                if account_value >= filter_value:
                    filtered_summaries[account_number] = summary
            else:
                if account_value <= filter_value:
                    filtered_summaries[account_number] = summary

        return filtered_summaries

    def write_filtered_summaries_to_csv(self, filtered_data: dict, file_path: str) -> None:
        """Writes the filtered data to a CSV file.
        
        Args:
            filtered_data (dict): A dictionary containing filtered
            account summaries.
            file_path (str): A path to the CSV file for the filtered
            account summaries.
        """
        # Checks filtered_data if a dictionary
        if not isinstance(filtered_data, dict):
            print("Error: filtered_data is not a dictionary.")
            return
        
        # Checks if file_path is a StringIO (in-memory file) or a
        # string (file path)
        if isinstance(file_path, StringIO):
            file = file_path
            writer = csv.DictWriter(file, fieldnames=
                                    ["Account number","Balance",
                                    "Total Deposits", "Total Withdrawals"])
        else:
            # Ensures the directory exists
            output_dir = os.path.dirname(file_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Open the file for writing
            with open(file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=
                                        ["Account number", "Balance",
                                        "Total Deposits", "Total Withdrawals"])
           
        writer.writeheader()

        # Write each filtered account summary as a row
        for account, data in filtered_data.items():
            writer.writerow({
                "Account number": "account number",
                "Balance": data["balance"],
                "Total Deposits": data["total_deposits"],
                "Total Withdrawals": data["total_withdrawals"]
            })

        print(f"Filtered summaries have been written to {file_path}")

    def main_function():
        """Integrates filtering functionality."""

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Set up OutputHandler instance with the account summaries data
        handler = OutputHandler(
            account_summaries={
                "1001": {"account_number": "1001", "balance": 550,
                         "total_deposits": 1000, "total_withdrawals": 450},
                "1002": {"account_number": "1002", "balance": 1400,
                         "total_deposits": 300, "total_withdrawals": 1700},
                "1003": {"account_number": "1003", "balance": 7950,
                         "total_deposits": 7950, "total_withdrawals": 0}
            },
            suspicious_transactions=[],
            transaction_statistics={}
        )

        def fdp_filter_team_7_csv(self):
            """Filtered filename for the group 7.
                
            Args:
                group_number (int): group number for this project

            Returns:
                - Call filter_account_summaries method with appropriate
                parameters.
                - Call write_filtered_summaries_to_csv with the list
                returned from the filter_account_summaries method.

            Raises:
                KeyError: Raised when no accounts meet the filter
                criteria.
            """
            group_number = 7
            filtered_filename = f"{output_dir}/fdp_filter_team_{7}.csv"

            # Calls the filter_account_summaries method with appropriate
            # parameters
            filtered_data = handler.filter_account_summaries("balance", 1000, True)

            # Calls the write_filtered_summaries_to_csv with the list
            # returned from the filter_account_summaries method
            if filtered_data:
                with open(filtered_filename, "w", newline="") as file:
                    handler.write_filtered_summaries_to_csv(filtered_data, file)

                print(f"Filtered summaries have been written to {filtered_filename}")
            else:
                print("No accounts meet the filter criteria. No file created.")
                