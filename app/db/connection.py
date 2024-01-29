import motor.motor_asyncio
import pandas as pd

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/watchlists"
)
db = client.watchlists
outperformers_collection = db.get_collection("outperformers")
trades_collection = db.get_collection("trades")
commentary_collection = db.get_collection("commentary")
etfs_collection = db.get_collection("etfs")
holdings_collection = db.get_collection("holdings")
