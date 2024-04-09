import talib
import numpy as np
import ccxt

# Configuración de la API de Binance
api_key = "TU_API_KEY"
api_secret = "TU_API_SECRET"
exchange = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
    }
)

# Símbolo del par de trading
symbol = "BTC/USDT"

# Función para obtener los datos históricos y actuales
def fetch_ohlcv(symbol, timeframe, since=None, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    return ohlcv


# Función para calcular los indicadores técnicos
def calculate_indicators(ohlcv):
    closes = np.array([x[4] for x in ohlcv], dtype=float)

    # Calcular indicadores técnicos
    sma = talib.SMA(closes, timeperiod=20)
    upper_band, middle_band, lower_band = talib.BBANDS(
        closes, timeperiod=20, nbdevup=2, nbdevdn=2
    )
    rsi = talib.RSI(closes, timeperiod=14)
    macd, signal, _ = talib.MACD(closes)

    return sma, upper_band, middle_band, lower_band, rsi, macd, signal


# Función para identificar niveles de soporte y resistencia
def identify_support_resistance(ohlcv):
    highs = np.array([x[2] for x in ohlcv], dtype=float)
    lows = np.array([x[3] for x in ohlcv], dtype=float)

    # Calcular niveles de soporte y resistencia utilizando, por ejemplo, mínimos y máximos locales
    support_levels = talib.MINMAX(lows, timeperiod=20)[0]
    resistance_levels = talib.MINMAX(highs, timeperiod=20)[1]

    return support_levels, resistance_levels


# Función para realizar operaciones de compra y venta basadas en inteligencia artificial
def trading_strategy(indicators, support_levels, resistance_levels, amount_to_invest):
    sma, upper_band, middle_band, lower_band, rsi, macd, signal = indicators

    last_sma = sma[-1]
    last_rsi = rsi[-1]
    last_macd = macd[-1]
    last_signal = signal[-1]

    # Lógica de la estrategia de trading
    if (
        last_sma > lower_band[-1]
        and last_rsi < 30
        and last_macd > last_signal
        and support_levels[-1] < exchange.fetch_ticker(symbol)["last"]
    ):
        # Realizar una operación de compra
        exchange.create_market_buy_order(symbol, amount_to_invest)
        print("Compra realizada en soporte")
    elif (
        last_sma < upper_band[-1]
        and last_rsi > 70
        and last_macd < last_signal
        and resistance_levels[-1] > exchange.fetch_ticker(symbol)["last"]
    ):
        # Realizar una operación de venta
        exchange.create_market_sell_order(symbol, amount_to_invest)
        print("Venta realizada en resistencia")


# Función principal
def main():
    # Obtener los datos históricos y actuales
    ohlcv = fetch_ohlcv(symbol, "1h", limit=100)

    # Calcular los indicadores técnicos
    indicators = calculate_indicators(ohlcv)

    # Identificar niveles de soporte y resistencia
    support_levels, resistance_levels = identify_support_resistance(ohlcv)

    # Definir la cantidad a invertir
    amount_to_invest = 100  # Por ejemplo, 100 USDT

    # Ejecutar la estrategia de trading
    trading_strategy(indicators, support_levels, resistance_levels, amount_to_invest)


# Ejecutar la función principal
if __name__ == "main":
    main()
