import requests 
import pandas as pd
import time

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

data = fetch_crypto_data()

top_5_by_market_cap = sorted(data, key=lambda x: x['market_cap'], reverse=True)[:5]

average_price = sum(coin['current_price'] for coin in data) / len(data)

highest_price_change = max(data, key=lambda x: x['price_change_percentage_24h'])
lowest_price_change = min(data, key=lambda x: x['price_change_percentage_24h'])
print(highest_price_change)

def write_to_excel(data):
    df = pd.DataFrame(data, columns=["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"])
    df.to_excel("crypto_data.xlsx", index=False)



while True:
    data = fetch_crypto_data()
    if data:
        write_to_excel(data)
        print("Data updated in Excel sheet.")
    time.sleep(300)  # Wait for 5 minutes (300 seconds)
