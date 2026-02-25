import ccxt
import pandas as pd
import numpy as np
import time

exchange = ccxt.delta({
    "apiKey": "HOepFWatHvK315mkXnS5GsnmNO1bg6",
    "secret": "R5aWJ4Broa50pUjO9GF0K6gImKTbYG3SqSKRpie8fmMDX3SatyjtaX0Co49v"
})

symbol = "ETH/USDT"
timeframe = "5m"

def get_data():
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(bars, columns=["time","open","high","low","close","volume"])
    return df

def indicators(df):
    # EMA
    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    sma = df["close"].rolling(20).mean()
    std = df["close"].rolling(20).std()
    df["bb_upper"] = sma + 2 * std
    df["bb_lower"] = sma - 2 * std

    return df

def strategy(df):
    last = df.iloc[-1]

    if (
        last["rsi"] > 50 and
        last["ema9"] > last["ema20"] and
        last["close"] > last["ema20"]
    ):
        return "BUY"

    if (
        last["rsi"] < 50 and
        last["ema9"] < last["ema20"] and
        last["close"] < last["ema20"]
    ):
        return "SELL"

    return None

while True:
    df = indicators(get_data())
    signal = strategy(df)

    if signal:
        print("Signal:", signal)

    time.sleep(300)
