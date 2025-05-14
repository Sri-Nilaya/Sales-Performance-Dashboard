from src.sales_analyzer import SalesAnalyzer

def main():
    file_path = "data\sales_data.csv"
    
    sales1 = SalesAnalyzer(file_path)
    sales1.get_sales_df()
    sales1.calculate_insights()

if __name__ == "__main__":
    main()

