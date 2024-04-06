import yfinance as yf
import plotext as plt
import pandas as pd
from asyncio import *
import asyncio
import requests


# Url de historico de BTC hasta un año
url = "https://api.blockchain.info/charts/market-price?timespan=1year&sampled=true&metadata=false&daysAverageString=1d&cors=true&format=json"


async def fetch_status(url: str) -> dict:
    return await asyncio.to_thread(requests.get, url, None)


async def main():
    try:
        global midata
        server_data: Task[dict] = asyncio.create_task(fetch_status(url))
        mydata = await server_data
        midata = mydata.json()
        print(midata["values"])
    except:
        pass


# Como usar plotext
# https://medium.com/@SrvZ/how-to-create-stunning-graphs-in-the-terminal-with-python-2adf9d012131

# Como usar yfinance
# https://webgeeksai.medium.com/gathering-stock-and-crypto-data-using-python-and-yfinance-e2f1734d80ef

# Datos de yfinance con fechas, se puede incluir en los ticker todas las cripto que quieren
# data = yf.download(tickers=["DOGE-USD", "BTC-USD"], start="2020-01-01", end="2021-01-01")

# Datos de yfinance con periodos
# data = yf.download(tickers="DOGE-USD", period="1mo", interval="15m")
# Intervalos validos : [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

tickers = "BTC-USD"  # Cambiar el simbolo aqui para usar otra moneda
file_name = "Data-" + tickers + ".json"
data = yf.download(
    tickers=tickers,
    period="60d",  # 7 dia
    interval="15m",  # 15 minuto
    # period="60d",  # 60 dias maximo con esta biblioteca
    # interval="30m",  #30 minutos
)

dates = plt.datetimes_to_string(data.index)
plt.clf()
plt.theme("dark")
plt.candlestick(dates, data)
plt.title(tickers + " Stock Price CandleSticks from last 60 days")
plt.show()
data.to_json(file_name)
print(
    "Los datos historicos de {} estan almacenados en el archivo {} \n".format(
        tickers, file_name
    )
)
print(data)

print("Los siguientes datos son los historicos anuales del BTC-USD \n")
asyncio.run(main=main())
