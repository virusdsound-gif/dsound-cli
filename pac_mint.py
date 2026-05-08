#!/usr/bin/env python3
"""
Essentium PaC Minting Tool v11.2
The Morning Star 🌟 Layer
"""

import os
import json
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv()

class PaCMinter:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider("https://rpc-amoy.polygon.technology"))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.private_key = os.getenv("PRIVATE_KEY")
        if not self.private_key:
            raise ValueError("PRIVATE_KEY not found in .env")
        
        self.account = self.w3.eth.account.from_key(self.private_key)
        print(f"Connected as: {self.account.address}")

    def mint_pac(self, energy_input: int, frequency_tier: int = 0):
        """Mint PaC tokens via EssentiumTrade"""
        # Replace with your deployed contract address after deployment
        contract_address = "0xYourDeployedContractAddressHere"
        
        # Minimal ABI for minting
        abi = [
            {"inputs":[{"internalType":"uint256","name":"_energyInput","type":"uint256"},{"internalType":"bytes32","name":"_dsoundSignature","type":"bytes32"},{"internalType":"uint256","name":"_frequencyTier","type":"uint256"}],"name":"verifyTrade","outputs":[],"stateMutability":"nonReentrant","type":"function"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"PaCMinted","type":"event"}
        ]

        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        
        # Create unique signature (simple hash for testing)
        signature = self.w3.keccak(text=f"DSOUND_{self.account.address}_{energy_input}")
        
        tx = contract.functions.verifyTrade(
            energy_input,
            signature,
            frequency_tier
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 500000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"✅ Transaction sent! Hash: {tx_hash.hex()}")
        print("Waiting for confirmation...")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"🎉 PaC Minted Successfully! Block: {receipt.blockNumber}")
        return receipt

if __name__ == "__main__":
    minter = PaCMinter()
    print("\n=== Essentium PaC Minter ===")
    energy = int(input("Enter Energy Input (e.g. 100): "))
    tier = int(input("Frequency Tier (0=0.7Hz, 1=99.9Hz, 2=200Hz, 3=369Hz): "))
    
    minter.mint_pac(energy, tier)
