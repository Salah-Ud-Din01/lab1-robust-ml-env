from typing import Any
import requests
from currencyhandler import CurrencyHandler

def main() -> None:
    currency_handler = CurrencyHandler()

    while True:
        print("\nCurrency Converter Menu:")
        print("[0] - List all currencies")
        print("[1] - Convert USD to a currency of choice")
        print("[2] - Refresh the data (fetch new currency data)")
        print("[3] - Export the data to JSON")
        print("[4] - Convert from any currency to any currency")
        print("[5] - Get historical exchange rate")
        print("[6] - Get rate trend for a currency")
        print("[7] - Exit the application")

        choice = input("Enter your choice (0-7): ")

        if choice == "0":
            currencies = currency_handler.list_currencies()
            print("Available currencies:")
            for currency in currencies:
                print(currency)

        elif choice == "1":
            to_currency = input("Enter the currency you want to convert to: ")
            amount_str = input("Enter your amount in USD: ")
            try:
                amount = float(amount_str)
                converted = currency_handler.convert_from_usd(to_currency, amount)
                print(f"{amount} USD is {converted:.2f} {to_currency.upper()}")
            except ValueError:
                print("Invalid amount or currency.")

        elif choice == "2":
            print("Refreshing data...")
            currency_handler.fetch_currency_data()
            print("Currency data updated.")

        elif choice == "3":
            try:
                currency_handler.export_to_json()
                print("Currency data has been exported to JSON.")
            except ValueError:
                print("Failed to export currency data.")

        elif choice == "4":
            from_currency = input("Enter the currency you want to convert from: ")
            to_currency = input("Enter the currency you want to convert to: ")
            amount_str = input("Enter the amount: ")
            try:
                amount = float(amount_str)
                converted = currency_handler.convert_any_currency(from_currency, to_currency, amount)
                print(f"{amount} {from_currency.upper()} is {converted:.2f} {to_currency.upper()}")
            except ValueError:
                print("Invalid amount or currency.")

        elif choice == "5":
            date = input("Enter the date (YYYY-MM-DD): ")
            base_currency = input("Enter the base currency: ")
            data = currency_handler.get_historical_rate(date, base_currency)
            if data:
                for currency, rate in data.items():
                    print(f"{currency}: {rate}")
            else:
                print("No data found for the given date and currency.")

        elif choice == "6":
            currency_code = input("Enter the currency you want to analyze: ").strip().upper()
            try:
                currency_handler.plot_rate_trend(currency_code)
                print(f"Trend for {currency_code} plotted successfully.")
            except ValueError as e:
                print("Error:", e)

        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()