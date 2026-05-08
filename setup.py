#!/usr/bin/env python3
"""
Essentium Project Setup & Dependency Installer
"""

import subprocess
import sys
import os

def install_packages():
    packages = [
        "web3",           # Ethereum interaction
        "python-dotenv",  # .env support
        "requests",       # API calls
        "rich",           # Beautiful terminal output
    ]
    
    print("🔧 Installing Essentium dependencies...\n")
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"✅ {pkg} installed")
        except:
            print(f"⚠️  Failed to install {pkg}")
    
    print("\n✅ Setup completed!")

def create_env():
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("""# Essentium Environment
PRIVATE_KEY=0xYourTestnetPrivateKeyHere
""")
        print("✅ .env file created (edit with your private key)")

if __name__ == "__main__":
    print("🌟 Essentium Project Setup v10.3\n")
    install_packages()
    create_env()
    print("\nRun: python verify.py    → to check system health")
