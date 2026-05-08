#!/usr/bin/env python3
"""
Essentium Web3 Integration v12.1
Full NFT Marketplace Support
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv()

class EssentiumWeb3:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider("https://rpc-amoy.polygon.technology"))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.private_key = os.getenv("PRIVATE_KEY")
        self.account = self.w3.eth.account.from_key(self.private_key)

        try:
            with open("contract_addresses.json") as f:
                self.addresses = json.load(f)
        except:
            self.addresses = {"EssentiumMusicNFT": "", "EssentiumNFTMarketplace": ""}

        print(f"✅ Connected: {self.account.address}")

    def list_nft(self, token_id: int, price: int):
        """List NFT for sale on marketplace"""
        contract = self.w3.eth.contract(
            address=self.addresses["EssentiumNFTMarketplace"],
            abi=[{
                "inputs": [{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"}],
                "name":"listNFT","outputs":[],"stateMutability":"nonpayable","type":"function"
            }]
        )

        tx = contract.functions.listNFT(token_id, price).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 500000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"🚀 Listing Tx: {tx_hash.hex()}")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ NFT #{token_id} listed for {price} PaC!")

    def buy_nft(self, token_id: int):
        """Buy listed NFT"""
        contract = self.w3.eth.contract(
            address=self.addresses["EssentiumNFTMarketplace"],
            abi=[{
                "inputs": [{"internalType":"uint256","name":"tokenId","type":"uint256"}],
                "name":"buyNFT","outputs":[],"stateMutability":"nonReentrant","type":"function"
            }]
        )

        tx = contract.functions.buyNFT(token_id).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 600000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"🚀 Buy Tx: {tx_hash.hex()}")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Successfully bought NFT #{token_id}!")

if __name__ == "__main__":
    print("Essentium NFT Marketplace Ready")
