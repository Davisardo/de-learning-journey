import requests
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_crypto_data():
    """Ambil data top 10 crypto dari CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False,
    }


    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Berhasil ambil {len(data)} data crypto")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Gagal ambil data:{e}")
        raise

if __name__ == "__main__":
    data = extract_crypto_data()
    for coin in data:
        print(f"{coin['name']}: ${coin['current_price']}")
