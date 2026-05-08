#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Compiling Python..."
find . -name "*.py" -exec python -m py_compile {} \;

echo "[+] Compiling Solidity..."
find . -name "*.sol" -exec solcjs --bin --abi {} \;

echo "[+] Checking TypeScript..."
npx tsc --noEmit

echo "[+] Finished"
