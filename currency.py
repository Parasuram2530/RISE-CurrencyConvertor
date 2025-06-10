import tkinter as tk
from tkinter import ttk
import requests


def get_supported_currencies():
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        data = response.json()
        return list(data.keys()) 
    except:
        result_label.config("Sry cant get it!")
        return 

currencies = get_supported_currencies()
def get_live_exchange_rate(base_currency, target_currency):
    try:
        url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
        response = requests.get(url)
        data = response.json()
        return data["rates"][target_currency]
    except:
        return None  

def convert_currency():
    amount = amount_entry.get()
    from_curr = source_currency.get()
    to_curr = target_currency.get()

    try:
        amount = float(amount)
    except ValueError:
        result_label.config(text="Error: Enter a valid number!")
        return

    if from_curr == to_curr:
        result_label.config(text=f"Result: {amount:.2f} {to_curr}")
        return


    rate = get_live_exchange_rate(from_curr, to_curr)
    if rate is None:  
        result_label.config(text="Sry cantget it")
        return 
    

    converted_amount = amount * rate
    result_label.config(text=f"Result: {converted_amount:.2f} {to_curr}")

root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x250")

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

source_currency_label = tk.Label(root, text="From Currency:")
source_currency_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
source_currency = ttk.Combobox(root, values=currencies)
source_currency.grid(row=1, column=1, padx=10, pady=10, sticky="w")
source_currency.set("INR")  

target_currency_label = tk.Label(root, text="To Currency:")
target_currency_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
target_currency = ttk.Combobox(root, values=currencies)
target_currency.grid(row=2, column=1, padx=10, pady=10, sticky="w")
target_currency.set("USD")  


convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Result: -", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()