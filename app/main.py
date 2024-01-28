import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# routes
from .router import (
    watchlists,
    indices,
    sectors,
    industries,
    history,
    outperformers,
    trade,
    commentary,
    etfs,
)

# app
app = FastAPI()

origins = [
    "http://localhost:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route(
    "/", response_class=HTMLResponse, status_code=200, methods=["GET", "HEAD"]
)
async def load_root():
    with open("index.html", "r") as file:
        return file.read()


app.include_router(watchlists.router)
app.include_router(indices.router)
app.include_router(sectors.router)
app.include_router(industries.router)
app.include_router(history.router)
app.include_router(outperformers.router)
app.include_router(trade.router)
app.include_router(commentary.router)
app.include_router(etfs.router)

if __name__ == "__main__":
    port = os.getenv("PORT") or 8080
    uvicorn.run(app, host="127.0.0.1", port=int(port))
