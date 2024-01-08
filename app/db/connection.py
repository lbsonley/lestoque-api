import motor.motor_asyncio
import pandas as pd

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/watchlists"
)
db = client.watchlists
outperformers_collection = db.get_collection("outperformers")
industries_collection = db.get_collection("industries")

industry_etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/industries.csv", index_col="symbol"
)

industry_collections = {}

for symbol in industry_etfs.index.to_list():
    industry_collections[symbol] = db.get_collection(symbol)
