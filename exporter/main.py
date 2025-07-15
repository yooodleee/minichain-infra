from fastapi import FastAPI
from prometheus_client import start_http_server, Gauge
from web3 import Web3
import threading
import time

app = FastAPI()

# JSON-RPC URL (geth)
web3 = Web3(Web3.HTTPProvider("http://geth:8545"))

block_height = Gauge("ethereum_block_height", "Current block height")
peer_count = Gauge("ethereum_peer_count", "Number of peers")


def update_metrics():
    while True:
        try:
            block_number = web3.eth.block_number
            peers = web3.net.peer_count
            block_height.set(block_number)
            peer_count.set(peers)
        except Exception as e:
            print("Error fetching metrics:", e)
        time.sleep(15)


@app.get("/")
def health():
    return {"status": "ok"}

# Start Prometheus metrics server
threading.Thread(target=lambda: start_http_server(9000)).start()
threading.Thread(target=update_metrics).start()