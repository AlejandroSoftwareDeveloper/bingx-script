import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Descargar datos historicos de Bitcoin (BTC-USD) para los ultimos 5 a�os
btc_df = yf.download("BTC-USD", start="2019-04-08", end="2024-04-08")

# Calcular las EMAs de 20 dias y 50 dias
btc_df["ema_short"] = btc_df["Close"].ewm(span=20, adjust=False).mean()
btc_df["ema_long"] = btc_df["Close"].ewm(span=50, adjust=False).mean()

# Calcular senales de cruce EMA
btc_df["bullish"] = np.where(btc_df["ema_short"] > btc_df["ema_long"], 1.0, 0.0)
btc_df["crossover"] = btc_df["bullish"].diff()


# Calcular el RSI
def calculate_rsi(df, window=14):
    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


btc_df["rsi"] = calculate_rsi(btc_df)

# Visualizar las senales de cruce EMA y el RSI
fig, ax = plt.subplots(figsize=(12, 6))
btc_df["Close"].plot(ax=ax, label="Precio de cierre", color="b") # Cierre, azul
btc_df["ema_short"].plot(ax=ax, label="EMA 20 dias", color="r")  
btc_df["ema_long"].plot(ax=ax, label="EMA 50 dias", color="g")
ax.set_ylabel("Precio en $")
ax2 = ax.twinx()
btc_df["rsi"].plot(ax=ax2, label="RSI", color="purple", linestyle="--")
ax2.set_ylabel("RSI")
plt.title("EMA CROSS y RSI para Bitcoin (BTC-USD)")
plt.legend()
plt.show()
