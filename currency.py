import tkinter as tk
from tkinter import ttk
import requests

# ======================== MOCK API DATA ========================
exchange_rates = {
    "USD": {"EUR": 0.85, "INR": 74.57, "GBP": 0.73, "USD": 1.0},
    "EUR": {"USD": 1.18, "INR": 88.98, "GBP": 0.86, "EUR": 1.0},
    "INR": {"USD": 0.013, "EUR": 0.011, "GBP": 0.0097, "INR": 1.0},
    "GBP": {"USD": 1.37, "EUR": 1.16, "INR": 102.5, "GBP": 1.0}
}

def get_supported_currencies():
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        data = response.json()
        return list(data.keys())  # returns ['USD', 'EUR', 'INR', ...]
    except:
        return list(exchange_rates.keys())  # fallback to mock keys

currencies = get_supported_currencies()
# ======================== REAL API (Frankfurter.app) ========================
def get_live_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
        response = requests.get(url)
        data = response.json()
        return data["rates"][target_currency]
    except:
        return None  # Fallback to mock data if API fails

# ======================== CURRENCY CONVERTER FUNCTION ========================
def convert_currency():
    amount = amount_entry.get()
    from_curr = source_currency.get()
    to_curr = target_currency.get()

    # Validate amount input
    try:
        amount = float(amount)
    except ValueError:
        result_label.config(text="Error: Enter a valid number!")
        return

    # Check if same currency
    if from_curr == to_curr:
        result_label.config(text=f"Result: {amount:.2f} {to_curr}")
        return

    # Get exchange rate (try API first, fallback to mock)
    # use_api = api_toggle.get()  # Check if API is enabled
    rate = get_live_exchange_rate(from_curr, to_curr)
    if rate is None:  # If API fails, use mock data
        result_label.config(text="Sry cantget it")
        return 
    

    converted_amount = amount * rate
    result_label.config(text=f"Result: {converted_amount:.2f} {to_curr}")

# ======================== GUI SETUP ========================
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x250")

# Amount Input
amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Source Currency Dropdown
source_currency_label = tk.Label(root, text="From Currency:")
source_currency_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
source_currency = ttk.Combobox(root, values=currencies)
source_currency.grid(row=1, column=1, padx=10, pady=10, sticky="w")
source_currency.set("INR")  # Default value

# Target Currency Dropdown
target_currency_label = tk.Label(root, text="To Currency:")
target_currency_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
target_currency = ttk.Combobox(root, values=currencies)
target_currency.grid(row=2, column=1, padx=10, pady=10, sticky="w")
target_currency.set("USD")  # Default value

# API Toggle (Switch between mock and real API)
# api_toggle = tk.BooleanVar()
# api_checkbox = tk.Checkbutton(root, text="Use Real Exchange Rates (API)", variable=api_toggle)
# api_checkbox.grid(row=3, column=0, columnspan=2, pady=5)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.grid(row=4, column=0, columnspan=2, pady=10)

# Result Label
result_label = tk.Label(root, text="Result: -", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()