import time
import datetime
from datetime import timedelta
import yfinance as yf
import threading
from send_email import EmailSender


class RSIAnalyzer:
    COINS = ["ETH-USD", "BTC-USD", "SOL-USD"]
    RSI_WINDOW = 14
    ANALYSIS_DAYS = 14
    MIN_BUY_DIFFERENCE = 2
    MIN_RSI_THRESHOLD = 32
    RSI_CHANGE_THRESHOLD = 3

    def init(self, email_sender: EmailSender):
        self.rsi_values = {coin: None for coin in self.COINS}
        self.min_rsi_values = {coin: None for coin in self.COINS}
        self.min_rsi_last_values = {coin: 100 for coin in self.COINS}
        self.email_sender = email_sender

    def calculate_rsi(self, symbol):
        today = datetime.date.today()
        current_date = today.strftime("%Y-%m-%d")
        seven_days = today - timedelta(days=self.ANALYSIS_DAYS)
        # Download price data for the coin
        stock_data = yf.download(
            symbol, interval="1d", start=seven_days, end=current_date
        )
        # Calculate RSI with a 14-day period
        delta = stock_data["Close"].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(span=self.RSI_WINDOW, adjust=True).mean()
        avg_loss = loss.ewm(span=self.RSI_WINDOW, adjust=True).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Return the latest RSI value
        return rsi.iloc[-1]

    def update_rsi(self, symbol: str):
        while True:
            try:
                current_rsi = self.calculate_rsi(symbol)
                self.rsi_values[symbol] = current_rsi
                if (
                    self.min_rsi_values[symbol] is None
                    or current_rsi < self.min_rsi_values[symbol]
                ):
                    self.min_rsi_values[symbol] = current_rsi
                time.sleep(3)
            except Exception as e:
                print(e)

    def analyze_coins(self):
        threads = []
        for coin in self.COINS:
            thread = threading.Thread(target=self.update_rsi, args=(coin,), daemon=True)
            thread.start()
            threads.append(thread)

        while True:
            for coin, rsi_value in self.rsi_values.items():
                min_rsi = self.min_rsi_values[coin]
                if (
                    rsi_value is not None
                    and rsi_value < self.MIN_RSI_THRESHOLD
                    and rsi_value < self.min_rsi_last_values[coin]
                ):
                    self.min_rsi_last_values[coin] = rsi_value
                    self.email_sender.send_email(
                        "navegabit.2020@gmail.com",
                        "navegabit.2020@gmail.com",
                        f"Moneda {coin} en sobre Venta. " f"Precio: {rsi_value}",
                    )
                if (
                    min_rsi is not None
                    and (rsi_value - self.min_rsi_last_values[coin])
                    >= self.RSI_CHANGE_THRESHOLD
                ):
                    self.min_rsi_last_values[coin] = rsi_value
                    self.email_sender.send_email(
                        "navegabit.2020@gmail.com",
                        "navegabit.2020@gmail.com",
                        f"Momento de compra para moneda {coin}. Precio: "
                        f"{rsi_value}",
                    )
            time.sleep(10)


# Usage of the RSIAnalyzer class
analyzer = RSIAnalyzer(EmailSender())
analyzer.analyze_coins()
