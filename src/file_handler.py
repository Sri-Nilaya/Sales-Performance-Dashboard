import pandas as pd

class FileHandle:
    def __init__(self, file_path):
        # Store the file path provided when creating an instance
        self.file_path = file_path
        # Initialize DataFrame to None (will be populated when read_file is called)
        self.sales_file_df = None
    
    def read_file(self):
        try:
            # Attempt to read the CSV file into a pandas DataFrame
            self.sales_file_df = pd.read_csv(self.file_path)
            # Display the first 5 rows of data for verification
            print(self.sales_file_df.head())  
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
        # Check if DataFrame has been populated by read_file
        if self.sales_file_df == None:
            print("Error: No data found. Read the file first.")
            return
        else:
            # Define the columns we expect in our CSV file
            expected_columns = ["Date","Total Sales (USD)","Number of Transactions","Avg Sale per Transaction (USD)","Best-Selling Item"]
            # Check if any expected columns are missing
            missing_columns = [col for col in expected_columns if col not in self.sales_file_df.columns]

        # Filter out rows with negative Total Sales (if column exists)
        if "Total Sales (USD)" not in missing_columns: 
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Total Sales (USD)'] > 0]
        
        # Filter out rows with zero or negative Number of Transactions (if column exists)
        if "Number of Transactions" not in missing_columns:
            self.sales_file_df = self.sales_file_df[self.sales_file_df['Number of Transactions'] > 0]
        
        