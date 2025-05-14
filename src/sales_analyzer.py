import logging
from src.file_handler import FileHandle 
from src.utils.logger import LoggerManager
import pandas as pd

class SalesAnalyzer:

    def __init__(self, file_path):
        """
        Initializes the SalesAnalyzer with the file path and logger.
        """
        self.file_path = file_path
        self.cleaned_sales_file_df = None

        # Create a logger instance using LoggerManager
        logger_manager = LoggerManager(logger_name= __name__, log_level=logging.INFO, log_file_name="sales_analyzer")
        self.logger = logger_manager.get_logger()

    def get_sales_df(self):
        """
        Reads, validates, and cleans the sales data file.
        """
        file_handle = FileHandle(self.file_path)
        file_handle.read_file()
        file_handle.validate_data()
        self.cleaned_sales_file_df = file_handle.get_clean_data()

    def highest_total_sales_of_day(self):
        """
        Calculates and logs the highest total sales of the day.
        """
        highest = self.cleaned_sales_file_df.max()
        self.logger.info(f"The highest total sales of the day: {highest}")

    def average_daily_sales(self):

        """ Calculates average sales"""
        average = self.cleaned_sales_file_df['Total Sales (USD)'].mean()
        self.logger.info(f"The average sales per day is: {average} ")
    
    def most_frequent_best_selling_item(self):
        """Calculate the most sold item"""

        frequent_item = self.cleaned_sales_file_df['Best-Selling Item'].value_counts().idxmax()
        self.logger.info(f"The most frequently sold item is: {frequent_item}")
    
    def average_transactions_per_day(self):
        """ Calculate average transactions per day"""

        average_transactions = self.cleaned_sales_file_df['Number of Transactions'].mean()
        self.logger.info(f"Average transactions per day is: {average_transactions}")

    def calculate_insights(self):
        """
        Calculates various insights from the sales data. By calling the respective functions from this file.
        """
        self.highest_total_sales_of_day()
        self.average_daily_sales()
        self.most_frequent_best_selling_item()
        self.average_transactions_per_day()