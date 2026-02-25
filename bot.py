import ccxt
import pandas as pd
import pandas_ta as ta
import time

exchange = ccxt.delta({
    'apiKey': 'API_KEY_YAHAN_DALO',
    'secret': 'API_SECRET_YAHAN_DALO'
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
    df['supertrend'] = st['SUPERT_10_3.0']

    bb = ta.bbands(df['close'], length=20)
    df['bb_upper'] = bb['BBU_20_2.0']
    df['bb_lower'] = bb['BBL_20_2.0']

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
