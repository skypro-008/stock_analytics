import json
from datetime import datetime, timedelta

from src.stock_data_fetcher import fetch_stock_data


def analyze_stock_data(start_date: str, end_date: str) -> dict[str, dict[str, float]]:
    """
    Функция принимает на вход две даты, вызывает fetch_stock_data, которая проверит,
    что все данные есть, иначе запросит курсы валют и создаст отсутствующие файлы.
    Далее считывает данные из файлов и возвращает аналитику в виде словаря.
    """
    fetch_stock_data(start_date, end_date)

    stock_data = {}

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    number_of_days = (end_date - start_date).days

    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        file_name = f"data/{date_str}.json"

        with open(file_name, "r") as f:
            data = json.load(f)

        for stock_code, stock_info in data.items():
            if stock_code not in stock_data:
                stock_data[stock_code] = {
                    "min": stock_info["low"],
                    "max": stock_info["high"],
                    "avg": stock_info["close"],
                }
            else:
                stock_data[stock_code]["min"] = min(
                    stock_data[stock_code]["min"], stock_info["low"]
                )
                stock_data[stock_code]["max"] = max(
                    stock_data[stock_code]["max"], stock_info["high"]
                )
                stock_data[stock_code]["avg"] += stock_info["close"]

        start_date += timedelta(days=1)

    for stock_code in stock_data.keys():
        stock_data[stock_code]["avg"] = round(
            stock_data[stock_code]["avg"] / number_of_days, 2
        )

    return stock_data
