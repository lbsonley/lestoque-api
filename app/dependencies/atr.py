import pandas_ta as ta


def calculate_atr(stock_data):
    atr = ta.atr(
        percent=True,
        high=stock_data["high"],
        low=stock_data["low"],
        close=stock_data["close"],
        length=14,
    )

    return atr
