from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import time
import os

today = datetime.date.today()
current_date = today.strftime("%Y-%m-%d")
# No se puede captura mas de siete dias con yfinance
# five_years_ago = today - timedelta(days=365 * 5)
seven_days = today - timedelta(days=7)

old_value = 0
new_value = 0
buy_time = False


def calculate_rsi(df, window=14):
    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def estimation_of_rsi_buy_condition(diferencia_minima_de_compra=2):
    global old_value, new_value, buy_time
    while True:
        os.system("cls")
        btc_df = yf.download(
            "BTC-USD", start=seven_days, end=current_date, interval="1m"
        )
        # Hasta aqui obtengo el ultimo valor
        actual_value = calculate_rsi(btc_df).tail().iloc[-1]
        print(btc_df, calculate_rsi(btc_df))
        if actual_value < 30 and not buy_time:
            if old_value == 0 or actual_value - old_value < 0:
                old_value = actual_value
            elif actual_value - old_value >= diferencia_minima_de_compra:
                buy_time = True
                break
        print(
            "El valor actual del rsi es {} el valor anterior es de {} y su diferencia {}".format(
                actual_value, old_value, actual_value - old_value
            )
        )
        time.sleep(2)
    return (True, actual_value)


estimation_of_rsi_buy_condition()
