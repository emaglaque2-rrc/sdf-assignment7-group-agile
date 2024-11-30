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
        
        Raises:
            FileNotFoundError: Raised when the file_path does not exist.
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

        return transactions

    def read_csv_data(self) -> list:
        """Reads input data from a csv file.

        Returns:
            list: The input data from a csv file as a list of
                  dictionaries, where each row represents a row of the
                  CSV file.
        
        Raises:
            FileNotFoundError: Raised when the file_path does not exist.
        """
        # Checks if the file exists at the given path
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
