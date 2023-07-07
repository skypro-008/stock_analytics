import json
import os
from datetime import datetime, timedelta

import requests

from dotenv import load_dotenv

load_dotenv()


def fetch_stock_data(start_date: str, end_date: str) -> None:
    """
    Проверяет, что в data/ есть json-файлы для всех дней между переданными датами.
    Для недостающих дат идет API-запрос курса акций и файл создается.
    """
    supported_stocks = json.load(open("supported_stocks.json"))
    url = "https://finnhub.io/api/v1/stock/candle"
    token = os.environ["FINN_HUB"]

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        file_name = f"data/{date_str}.json"

        if not os.path.exists(file_name):
            stock_data = {}

            for stock_code in supported_stocks.keys():
                params = {
                    "symbol": stock_code,
                    "resolution": "D",
                    "from": int(datetime.timestamp(start_date)),
                    "to": int(datetime.timestamp(start_date + timedelta(days=1))),
                    "token": token,
                }

                response = requests.get(url, params=params)
                response.raise_for_status()
                response_json = response.json()
                try:
                    stock_data[stock_code] = {
                        "open": response_json["o"][0],
                        "high": response_json["h"][0],
                        "low": response_json["l"][0],
                        "close": response_json["c"][0],
                        "volume": response_json["v"][0],
                    }
                except KeyError:
                    print(f"No data available for {stock_code} on {date_str}")

            with open(file_name, "w") as f:
                json.dump(stock_data, f)

        start_date += timedelta(days=1)
