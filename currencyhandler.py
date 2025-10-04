import json
import os
import requests
from datetime import datetime, timedelta
from typing import Any



class CurrencyHandler:
    def __init__(self, base_currency: str = "USD"):
        self.base_currency = base_currency.upper()
        self.currency_data = {}
        self.last_updated = None
        data = self.load_currency_data()
        if data:
            self.currency_data = data.get("rates", {})
            timestamp = data.get("timestamp", 0)
            self.last_updated = datetime.fromtimestamp(data.get("timestamp"))
        else:
            self.fetch_currency_data()

    def fetch_currency_data(self) -> dict[str, Any]:
        app_id = "22127c485fd642da9820bdfddc79eeca"                                                                                                                    
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
        headers = {"accept": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.currency_data = data.get("rates", {})
            self.last_updated = datetime.fromtimestamp(data.get("timestamp"))

            return data
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return {}
                

    def convert_from_usd(self, to_currency: str, amount: float) -> float:
        to_currency = to_currency.upper()

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        if to_currency not in self.currency_data:
            raise ValueError(f"Currency '{to_currency}' not supported")

        rate = self.currency_data[to_currency]
        converted_amount = amount * rate
        return converted_amount

    def convert_any_currency(self, from_currency: str, to_currency: str, amount: float) -> float:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        if from_currency not in self.currency_data or to_currency not in self.currency_data:
            raise ValueError("One or both currency codes are invalid")

        amount_in_usd = amount / self.currency_data[from_currency]
        return amount_in_usd * self.currency_data[to_currency]

    
    def list_currencies(self) -> list[str]:
        return sorted(self.currency_data.keys())

    def load_currency_data(self) -> dict[str, Any]:
        if not os.path.isfile("currency_data.json"):
            return {}

        try:
            with open("currency_data.json", "r") as f:
                data = json.load(f)

            timestamp = data.get("timestamp", 0)
            last_update = datetime.fromtimestamp(timestamp)

            if (datetime.now() - last_update).total_seconds() > 3600:
                return self.fetch_currency_data()

            return data
        except (IOError, json.JSONDecodeError):
            return self.fetch_currency_data()
       
        
    def export_to_json(self) -> None:
        try:
            data = {
                "rates": self.currency_data,
                "timestamp": int(datetime.now().timestamp())
            }
            with open("currency_data.json", "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Failed to export data: {e}")

    def load_currency_data(self) -> dict[str, Any]:
        if not os.path.isfile("currency_data.json"):
            return {}

        try:
            with open("currency_data.json", "r") as f:
                data = json.load(f)

            timestamp = data.get("timestamp", 0)
            last_update = datetime.fromtimestamp(timestamp)

            # Check if data is older than 1 hour
            if (datetime.now() - last_update).total_seconds() > 3600:
                return self.fetch_currency_data()

            return data

        except (IOError, json.JSONDecodeError):
            return self.fetch_currency_data()

    def get_historical_rate(self, date: str, base_currency: str) -> dict[str, Any]:
        app_id = "22127c485fd642da9820bdfddc79eeca"
        url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={app_id}&base={base_currency}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("rates", {})
        except requests.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return {}

    def list_historical_rates_for_currency(self, currency: str, days: int) -> list[tuple[str, float]]:
        rates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            data = self.get_historical_rate(date, self.base_currency)
            rate = data.get(currency.upper())
            if rate:
                rates.append((date, rate))
        return rates
    
    def plot_rate_trend(self, currency: str, days: int = 7):
        currency = currency.upper()
        data = self.list_historical_rates_for_currency(currency, days)

        if not data:
            print(f"No historical data found for {currency}.")
            return

        dates = [item[0] for item in data]
        rates = [item[1] for item in data]

        import matplotlib.pyplot as plt  # You can also move this to the top
        plt.plot(dates, rates, marker='o')
        plt.title(f"{currency} Exchange Rate Trend (Last {days} Days)")
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()