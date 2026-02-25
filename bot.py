import warnings
warnings.filterwarnings("ignore")

import ccxt
import pandas as pd
import pandas_ta as ta
import time

exchange = ccxt.delta({
    'apiKey': HOepFWatHvK315mkXnS5GsnmNO1bg6
    'secret': R5aWJ4Broa50pUjO9GF0K6gImKTbYG3SqSKRpie8fmMDX3SatyjtaX0Co49v
})

symbol = 'ETH/USDT'
timeframe = '5m'

def get_data():
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(bars, columns=['time','open','high','low','close','volume'])
    return df

def apply_indicators(df):
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['ema9'] = ta.ema(df['close'], length=9)
    df['ema20'] = ta.ema(df['close'], length=20)

    st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3)
    df['supertrend'] = st.iloc[:, 0]

 bb = ta.bbands(df['close'], length=20, std=2)
df['bb_upper'] = bb.iloc[:, 0]
df['bb_lower'] = bb.iloc[:, 2]

    return df

def strategy(df):
    last = df.iloc[-1]

    if (
        last['rsi'] > 50 and
        last['ema9'] > last['ema20'] and
        last['close'] > last['supertrend']
    ):
        return "BUY"

    if (
        last['rsi'] < 50 and
        last['ema9'] < last['ema20'] and
        last['close'] < last['supertrend']
    ):
        return "SELL"

    return None

while True:
    df = get_data()
    df = apply_indicators(df)
    signal = strategy(df)

    if signal:
        print("Signal:", signal)

    time.sleep(300)
