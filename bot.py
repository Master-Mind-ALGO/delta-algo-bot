# ===== FREE WEB SERVICE HACK + ALGO BOT =====

from flask import Flask
import threading
import os
import ccxt
import pandas as pd
import numpy as np
import time

# ---------- FLASK (Fake Web Server for Render Free) ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Algo bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# ---------- START WEB SERVER THREAD ----------
threading.Thread(target=run_web).start()

# ---------- DELTA EXCHANGE CONNECTION (SAFE WAY) ----------
exchange = ccxt.delta({
    "apiKey": os.environ.get("DELTA_API_KEY"),
    "secret": os.environ.get("DELTA_API_SECRET")
})

symbol = "ETH/USDT"
timeframe = "5m"

# ---------- MARKET DATA ----------
def get_data():
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(
        bars,
        columns=["time", "open", "high", "low", "close", "volume"]
    )
    return df

# ---------- INDICATORS ----------
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

# ---------- STRATEGY ----------
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

# ---------- MAIN LOOP ----------
while True:
    df = indicators(get_data())
    signal = strategy(df)

    if signal:
        print("Signal:", signal)

    time.sleep(300)
