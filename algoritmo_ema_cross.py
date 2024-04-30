from binance.client import Client  # pip install python-binance.py
from binance.enums import *
import time

# crea tu cuenta en binance
API_KEY = ""
API_SECRET = ""
client = Client(API_KEY, API_SECRET, tld="com")


class EMA_CROSS_CLASS:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, tld="com")

    def get_tickets_from_binance(self, pair, symbol_pair):
        for ticket in self.client.get_all_tickers():
            if ticket[pair] == symbol_pair:
                return (ticket[pair], ticket["price"])

    def sma_intervalo_1hs(self, periodo, ticker):
        data_historical = client.get_historical_klines(
            ticker, Client.KLINE_INTERVAL_1HOUR, "800 hour ago UTC"
        )
        if len(data_historical) == 800:
            return (
                sum([float(data_historical[i][4]) for i in range((800 - periodo), 800)])
                / periodo
            )

    def ema_intervalo_1hs(self, periodo, ticker):
        ema = []
        precios_de_cierres = []
        data_historical = client.get_historical_klines(
            ticker, Client.KLINE_INTERVAL_1HOUR, "800 hour ago UTC"  # 250
        )
        ema.append(self.sma_intervalo_1hs(periodo, ticker))
        if len(data_historical) == 800:
            for i in range(len(data_historical)):
                precios_de_cierres.append(float(data_historical[i][4]))
            for price in precios_de_cierres[periodo:]:
                ema.append(
                    (price * (2 / (periodo + 1))) + ema[-1] * (1 - (2 / (periodo + 1)))
                )
            return round(ema.pop(), 6)
        else:
            print("no se pudo obtener el historial de las velas")

    def calcular_emas_cross(self, periodo1, periodo2, periodo3, ticket):
        cambio = False
        while not cambio:
            emap1, emap2, emap3 = [
                self.ema_intervalo_1hs(x, ticket)
                for x in [periodo1, periodo2, periodo3]
            ]
            if emap1 > emap2 and emap1 > emap3:
                print(
                    "Ticker "
                    + ticket
                    + "Ema rapida por encima de la otras dos - posible movimiento alcista."
                )
                return True
            if emap1 < emap2 and emap1 < emap3:
                print(
                    "Ticker "
                    + ticket
                    + "Ema rapida por debajo de la otras dos - posible movimiento bajista."
                )
                return True
            time.sleep(2)
        print("No se puede verificar la estrategia")
        return False


ema = EMA_CROSS_CLASS()
ema.calcular_emas_cross(4, 8, 16, "BTCUSD")
