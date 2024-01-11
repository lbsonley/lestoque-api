from fastapi import APIRouter
from fastapi.responses import JSONResponse
import yfinance as yf

router = APIRouter()

# pattern code
# https://github.com/TA-Lib/ta-lib-python/blob/master/talib/_func.pxi
patterns = [
    "darkcloudcover",
    "doji",
    "dojistar",
    "engulfing",
    "eveningdojistar",
    "eveningstar",
    "hammer",
    "hangingman",
    "morningdojistar",
    "morningstar",
    "piercing",
]


@router.get(
    "/api/history",
    response_class=JSONResponse,
    status_code=200,
)
def load_history(symbol: str, interval: str, start: str, end: str):
    # fetch data
    stock = yf.Ticker(symbol)
    history = stock.history(interval=interval, start=start, end=end)

    # do japanese candlestick analysis
    cdl = history.ta.cdl_pattern(name=patterns)
    cdl.columns = patterns

    # extract dates where candlestick pattern occured
    signals = {}
    for pattern in cdl.columns:
        col = cdl[[pattern]]
        dates = col[(col[pattern] == 100.0) | (col[pattern] == -100)].index
        signals[pattern] = dates.to_list()

    # explicitly name index column
    history.index.names = ["datetime"]
    # reset the index so that when we convert the dataframe to dict the datetime is present
    history = history.reset_index()
    # make column names lowercase
    history.columns = history.columns.str.lower()
    # select only the columns we need
    history = history.loc[
        :, ["datetime", "open", "high", "low", "close", "volume"]
    ]

    # return data
    return {
        "history": history.to_dict(orient="records"),
        "candlestickSignals": signals,
    }
