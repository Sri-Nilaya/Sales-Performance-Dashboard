import logging
import pandas as pd
import logging
from src.utils.logger import LoggerManager

class FileHandle:
    def __init__(self, file_path):
        # Store the file path provided when creating an instance
        self.file_path = file_path

        # Initialize DataFrame to None (will be populated when read_file is called)
        self.sales_file_df = None

        # Initialize DataFrame row count to 0 
        self.initial_row_count = 0
 
        # Define the columns we expect in our CSV file
        self.expected_columns = ["Date","Total Sales (USD)","Number of Transactions","Avg Sale per Transaction (USD)","Best-Selling Item"]
           
        # Initialize missing_columns to 0
        self.missing_columns = 0

        logger_manager = LoggerManager(logger_name = __name__, log_level = logging.INFO, log_file_name = "file_handler" )
        self.logger = logger_manager.get_logger()



    
    def read_file(self):
        try:
            # Attempt to read the CSV file into a pandas DataFrame
            self.sales_file_df = pd.read_csv(self.file_path)

            # Display the first 5 rows of data for verification
            print(self.sales_file_df.head())  

            # Store data frame row count 
            self.initial_row_count = len(self.sales_file_df)

        except FileNotFoundError:
            # Handle case where file doesn't exist
            self.logger.error("Error: File not found.")
        except PermissionError:
            # Handle case where file can't be accessed due to permissions
            self.logger.error("Error: Permission denied.")
        except Exception as e:
            # Catch any other unexpected errors
            self.logger.error(f"An unexpected error occurred: {e}")
    
    def validate_data(self):
        # Check if DataFrame object is None
        if self.sales_file_df is None:
            self.logger.warning("Error: No data found. Read the file first.")
            return
        
        # Check if entire DataFrame is empty with no rows, columns
        if self.sales_file_df.empty:
            self.logger.warning("DataFrame is empty")
            return
        
        # Check if any rows, columns are missing
        else:

            # 1. Check if any expected columns are missing and print them
            self.missing_columns = [col for col in self.expected_columns if col not in self.sales_file_df.columns]
        
            if len(self.missing_columns) > 0:
                self.logger.warning(f"These columns are missing: {self.missing_columns}")

            # 2. Check if any unexpected columns are present and print them
            if len(self.sales_file_df.columns) > len(self.expected_columns):
                unexpected_columns = [col for col in self.sales_file_df.columns if col not in self.expected_columns]
                self.logger.warning(f"These columns are unexpected:\n {unexpected_columns}")

            # 3. Check if the DataFrame rows are Null or not
            if self.sales_file_df.shape[0] == 0:
                self.logger.warning("DataFrame has no rows")
                return
            
            # 4. Check if duplicate rows exist
            duplicate_rows = self.sales_file_df.duplicated().sum()
            if duplicate_rows > 0:
                self.logger.warning(f"There are {duplicate_rows} Duplicate rows")

            

    def get_clean_data(self):

        # 1. Drop all rows that have at least one null value
        self.sales_file_df = self.sales_file_df.dropna()
        self.logger.info("Dropped all rows that have atleast one null value")

        # 2. Remove duplicate rows
        self.sales_file_df.drop_duplicates(inplace=True)
        self.logger.info("Removed duplicates")

        # 3. Filter out rows with negative Total Sales (if column exists)
        if "Total Sales (USD)" not in self.missing_columns: 
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Total Sales (USD)'] > 0]
            self.logger.info("Removed rows that had negative Total Sales")
        
        # 4. Filter out rows with zero or negative Number of Transactions (if column exists)
        if "Number of Transactions" not in self.missing_columns:
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Number of Transactions'] > 0]
            self.logger.info("Removed rows with zero or negative Number of Transactions")

        # 5. Convert Date column to proper data time format
        if "Date" not in self.missing_columns:
            self.sales_file_df["Date"] = pd.to_datetime(self.sales_file_df['Date'], dayfirst = True)
            self.logger.info("Converted Date Column to appropriate date time format")

        if self.initial_row_count != len(self.sales_file_df):
            current_rowcount = len(self.sales_file_df)
            self.logger.info(f"Row count post Data cleaning is: {current_rowcount} ")

        return(self.sales_file_df)
        
        

