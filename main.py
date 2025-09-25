from typing import Any

import requests
from currencyhandler import CurrencyHandler

def main() -> None:
    """
    The main function that runs the currency conversion application.

    This function should:
    1. Create an instance of the CurrencyHandler class.
    2. Display a menu of options to the user.
    3. Handle user input and call the appropriate methods of the CurrencyHandler.
    4. Provide a loop to allow multiple operations in a single session.
    5. Handle any errors or exceptions that may occur during operation.

    """
    
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
            
            print("list all the currenices:")
            currencies = currency_handler.list_currrencies()
            print("Avalaible currencies")
            for currency in currencies:
                print("currency")

        elif choice == "1":
            to_currency= input("enter the currency you want to convert:")
            amount_str= input ("enter your amount in USD:")
            
            try:
                amount = float(amount_str)
                converted = currency_handler.convert_from_usd(to_currency, amount)
                print(f"{amount} USD is {converted:2f} to {to_currency.upper()}")
            except ValueError:
                print("invalid amount or currency")


        elif choice == "2":
            print("Refreshing data")
            currency_handler.fetch_currency_data()
            print("currency data updated.")

        elif choice == "3":
            try:
                export= currency_handler.export_to_JSON()
                print("currency data has been exported to JSON")
            except ValueError:
                print("failed to export currency data ")

        elif choice == "4":
            from_currency=input("Enter the currency you want to convert:")
            to_currency=input("Enter the currency you want to convert to:")
            amount_str = input("Enter the amount:")
            try:
                amount=float(amount_str)
                converted =currency_handler.convert_anycurrency_(from_currency, to_currency, amount)
                print(f"{amount} {from_currency.upper()is {converted:.2f} {to_currencycurrency.upper()}")
            except ValueError:
                print("invalid amount or currency")


        elif choice == "5":
            date=input("enter the date")
            base_currency=input("enter the base currency:")
            data=currency_handler.get_historical_rate(date, base_currency)
            if data:
                for currency, rate in data.items():
                    print(f"{currency}: {rate}")
        
        else:
            print("no data found foe the give date and currencies:")
            

        elif choice == "6":


        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
