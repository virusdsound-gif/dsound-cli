#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Validating Python..."
find python -name "*.py" -exec python -m py_compile {} \;

echo "[+] Validating Solidity..."
find contracts -name "*.sol" -exec solcjs --bin --abi {} \;

echo "[+] Validation complete"
