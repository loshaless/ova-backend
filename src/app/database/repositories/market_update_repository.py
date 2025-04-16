import yfinance as yf
import requests
from bs4 import BeautifulSoup

tickers = {
    "IHSG": "^JKSE",
    "Nikkei 225": "^N225",
    "Dow Jones": "^DJI",
    "USD/IDR": "USDIDR=X",
    "SGD/IDR": "SGDIDR=X",
    "EUR/USD": "EURUSD=X",
    "AUD/USD": "AUDUSD=X",
    "Crude Oil": "CL=F",
}

def fetch_market_data():
    results = {}
    for name, ticker in tickers.items():
        try:
            data = yf.Ticker(ticker).history(period="5d")
            if data.empty:
                results[name] = "No data available"
            else:
                last_valid = data["Close"].dropna().iloc[-1]
                results[name] = round(float(last_valid), 2)
        except Exception as e:
            results[name] = f"Error: {str(e)}"
    return results

def fetch_bi_rate():
    url = "https://www.bi.go.id/id/statistik/indikator/bi-rate.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.find('table')
        first_row = table.find_all('tr')[1]
        cols = first_row.find_all('td')

        tanggal = cols[0].text.strip()
        bi_rate = cols[1].text.strip()

        return {
            "tanggal": tanggal,
            "bi_rate": bi_rate
        }

    except Exception as e:
        return {"error": str(e)}
