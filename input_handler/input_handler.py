"""This module defines the InputHandler Class."""

__author__ = "Edraque Maglaque"
__version__ = "0.11.2024"

import csv
import json
from os import path

class InputHandler:
    """Represents the intake functionality of the program for files."""

    def __init__(self, file_path: str):
        """Initializes a new instance of the InputHandler class.
        
        Args:
            file_path (str): The file path of the input data file that 
                             will be read.
        """
        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        """Gets the file path of the input data file.

        Returns:
            str: The file path of the input data file.
        """
        return self.__file_path

    def get_file_format(self) -> str:
        """Gets the file format of the input data file.

        Returns:
            str: The file format of the input data file.
        """
        return self.__file_path.split(".")[-1]

    def read_input_data(self) -> list:
        """Reads input data from a file based on it's format.

        Returns:
            list: The input data as a list.

        Raises: 
            FileNotFoundError: Raised when the file_path does not exist.
            ValueError: Raised when "Amount" value cannot be parsed 
                        into a float.
            KeyError: Raised when "Transaction type" and "Amount"
                      is missing a value.
        """
        # Initialize an empty list to store transactions.
        transactions = []
        file_format = self.get_file_format()
        
        # Reads data if file format is csv.
        if file_format == "csv":
            transactions =  self.read_csv_data()  
        # Reads data if file format is json.
        elif file_format == "json":
            transactions = self.read_json_data()

        # Invokes data_validation method to validate data before returning it.
        return self.data_validation(transactions)

    def read_csv_data(self) -> list:
        """Reads input data from a csv file.

        Returns:
            list: The input data from a csv file as a list of
                  dictionaries, where each row represents a row of the
                  CSV file.
        
        Raises:
            FileNotFoundError: Raised when the file_path does not exist.
        """
        # Checks if the file exists at the given path.
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        transactions = []

        with open(self.__file_path, "r") as input_file:
            # Reads file as a list of dictionaries.
            reader = csv.DictReader(input_file)
            for row in reader:
                # Append each row as a dictionary to the list.
                transactions.append(row)
            
        return transactions
            
    def read_json_data(self) -> list:
        """Reads input data from a json file.

        Returns:
            list: The input data from a json file as a list.
        
        Raises:
            FileNotFoundError: Raised when the file_path does not exist.
        """
        # Checks if the file exists at the given path.
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        with open(self.__file_path, "r") as input_file:
            # json.load will parse the JSON file into a Python object.
            transactions = json.load(input_file)

        return transactions
    
    def data_validation(self, transactions: list) -> list:
        """Validates data and returns a new list only containing
        valid transactions.
        
        Args:
            transactions (list): A list of dictionaries containing
                                 transaction data.
        
        Returns:
            list: A list of dictionaries containing only
                  valid transactions.
        
        Raises:
            ValueError: Raised when "Amount" cannot be parsed 
                        into a float.
            KeyError: Raised when "Transaction type" and "Amount"
                      is missing a value.
        """
        valid_transactions = []
        VALID_TRANSACTION_TYPES = ("deposit", "withdrawal", "transfer")

        for transaction in transactions:
            is_valid = True # Resets boolean flag for each iteration.

            try:
                # Extracts the amount value and attempt to parse it as a float value.
                amount = float(transaction["Amount"])
                transaction_type = transaction["Transaction type"]
            except (ValueError, KeyError):
                # If an exception occurs (invalid/missing values), mark as invalid.
                is_valid = False

            # Check if amount is non-negative and transaction type is valid.
            else:
                is_valid = amount > 0 and transaction_type in VALID_TRANSACTION_TYPES

            # If the transaction is valid, add it to the list of valid transactions.
            if is_valid:
                valid_transactions.append(transaction)
        
        return valid_transactions
