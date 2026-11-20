import re
import requests
from bs4 import BeautifulSoup

def scrape_iraq_exchange_rates():
    url = "https://iraqsm.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text(" ", strip=True)

        market_match = re.search(r"السوق الموازية اليوم نحو\s*([\d,]+)", page_text)
        official_match = re.search(r"مقابل\s*([\d,]+)\s*ديناراً هو السعر الرسمي", page_text)

        market_rate = float(market_match.group(1).replace(",", "")) if market_match else 1707.0
        official_rate = float(official_match.group(1).replace(",", "")) if official_match else 1510.0

        return official_rate, market_rate, True

    except Exception:
        return 1510.0, 1707.0, False

def calculate_tiktok_earnings():
    coins = int(input("Enter the number of TikTok coins: "))

    diamond_rate = 0.005
    usd_before_paypal = coins * diamond_rate

    paypal_percent = 0.029
    paypal_fixed = 0.30

    if usd_before_paypal > paypal_fixed:
        paypal_fee = (usd_before_paypal * paypal_percent) + paypal_fixed
        usd_after_paypal = usd_before_paypal - paypal_fee
    else:
        paypal_fee = 0.0
        usd_after_paypal = usd_before_paypal

    official_rate, market_rate, is_live = scrape_iraq_exchange_rates()
    status = "Live from IraqSM" if is_live else "Offline Fallback"

    iqd_official = usd_after_paypal * official_rate
    iqd_market = usd_after_paypal * market_rate

    print("-" * 55)
    print(f"Rate Source: {status}")
    print(f"Total Coins: {coins:,}")
    print(f"TikTok Net (Before PayPal):       ${usd_before_paypal:,.2f}")
    print(f"Standard PayPal Fee (2.9%+$0.30):-${paypal_fee:,.2f}")
    print(f"Final Net (After PayPal):         ${usd_after_paypal:,.2f}")
    print("-" * 55)
    print(f"Official Rate (1 USD = {official_rate:,.0f} IQD): {iqd_official:,.0f} IQD")
    print(f"Market Rate   (1 USD = {market_rate:,.0f} IQD): {iqd_market:,.0f} IQD")
    print("-" * 55)

if __name__ == "__main__":
    calculate_tiktok_earnings()
