import logging
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('sales_analyzer.log')
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


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
            print("Error: File not found.")
        except PermissionError:
            # Handle case where file can't be accessed due to permissions
            print("Error: Permission denied.")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
    
    def validate_data(self):
        # Check if DataFrame object is None
        if self.sales_file_df == None:
            print("Error: No data found. Read the file first.")
            return
        
        # Check if entire DataFrame is empty with no rows, columns
        if self.sales_file_df.empty:
            print("DataFrame is empty")
            return
        
        # Check if any rows, columns are missing
        else:

            # 1. Check if any expected columns are missing and print them
            self.missing_columns = [col for col in self.expected_columns if col not in self.sales_file_df.columns]
        
            if len(self.missing_columns) > 0:
                logger.warning(f"These columns are missing: {self.missing_columns}")

            # 2. Check if any unexpected columns are present and print them
            if len(self.sales_file_df.columns) > len(self.expected_columns):
                unexpected_columns = [col for col in self.sales_file_df.columns if col not in self.expected_columns]
                logger.warning(f"These columns are unexpected:\n {unexpected_columns}")

            # 3. Check if the DataFrame rows are Null or not
            if self.sales_file_df.shape[0] == 0:
                logger.warning("DataFrame has no rows")
                return
            
            # 4. Check if duplicate rows exist
            duplicate_rows = self.sales_file_df.duplicated().sum()
            if duplicate_rows > 0:
                logger.warning(f"There are {duplicate_rows} Duplicate rows")

            

    def get_clean_data(self):

        # 1. Drop all rows that have at least one null value
        self.sales_file_df = self.sales_file_df.dropna()

        # 2. Remove duplicate rows
        self.sales_file_df.drop_duplicates(inplace=True)

        # 3. Filter out rows with negative Total Sales (if column exists)
        if "Total Sales (USD)" not in self.missing_columns: 
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Total Sales (USD)'] > 0]
        
        # 4. Filter out rows with zero or negative Number of Transactions (if column exists)
        if "Number of Transactions" not in self.missing_columns:
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Number of Transactions'] > 0]

        # 5. Convert Date column to proper data time format
        if "Date" not in self.missing_columns:
            self.sales_file_df["Date"] = pd.to_datetime(self.sales_file_df['Date'], dayfirst = True)

        if self.initial_row_count != len(self.sales_file_df):
            current_rowcount = len(self.sales_file_df)
            logger.info(f"Row count post Data cleaning is: {current_rowcount} ")

        return(self.sales_file_df)
        
        

