import motor.motor_asyncio
import pandas as pd

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/watchlists"
    # "mongodb+srv://lbsonley:Trad34amil@lestoque-report.plbtscq.mongodb.net/"
)
db = client.watchlists
indices_collection = db.get_collection("indices")
sectors_collection = db.get_collection("sectors")
industries_collection = db.get_collection("industries")
outperformers_collection = db.get_collection("outperformers")
trades_collection = db.get_collection("trades")
commentary_collection = db.get_collection("commentary")
etfs_collection = db.get_collection("etfs")

# dynamically create collections to hold constituents for each of the industry etfs
industry_etfs = pd.read_csv(
    filepath_or_buffer="app/db/static/industries.csv", index_col="symbol"
)

industry_collections = {}

for symbol in industry_etfs.index.to_list():
    industry_collections[symbol] = db.get_collection(symbol)
