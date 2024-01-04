import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/watchlists"
)
db = client.watchlists
outperformers_collection = db.get_collection("outperformers")
industries_collection = db.get_collection("industries")
