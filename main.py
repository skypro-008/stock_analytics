import sys
from datetime import datetime

from analytics import analyze_stock_data

if __name__ == "__main__":
    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    stock_data = analyze_stock_data(start_date_str, end_date_str)

    for stock_code, stock_info in stock_data.items():
        print(f"{stock_code}:")
        print(f"  Min value: {stock_info['min']}")
        print(f"  Max value: {stock_info['max']}")
        print(f"  Average value: {stock_info['avg']}")
