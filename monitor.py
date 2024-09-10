import requests
import json
import time
from telegram import Bot

# Load configuration
with open('config.json') as f:
    config = json.load(f)

validator_address = config["validatorAddress"]
rpc_endpoint = config["rpcEndpoint"]
bot_token = config["telegram"]["botToken"]
chat_id = config["telegram"]["chatId"]

# Initialize Telegram bot
bot = Bot(token=bot_token)

def get_data_from_rpc(method):
    response = requests.post(rpc_endpoint, json={"jsonrpc": "2.0", "method": method, "params": [], "id": 1})
    return response.json()

def check_checkpoints():
    # Example methods; replace with actual RPC methods
    signed_checkpoints = get_data_from_rpc("eth_getSignedCheckpoints")
    proposed_checkpoints = get_data_from_rpc("eth_getProposedCheckpoints")
    
    if not signed_checkpoints or not proposed_checkpoints:
        send_alert("Checkpoints not being signed or proposed as expected.")

def check_heights():
    bor_height = get_data_from_rpc("eth_getBorHeight")
    heimdall_height = get_data_from_rpc("eth_getHeimdallHeight")
    
    if bor_height != heimdall_height:
        send_alert("Bor and Heimdall heights are out of sync.")

def send_alert(message):
    bot.send_message(chat_id=chat_id, text=message)

def monitor():
    while True:
        check_checkpoints()
        check_heights()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    monitor()
