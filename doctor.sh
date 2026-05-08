#!/data/data/com.termux/files/usr/bin/bash

echo "=============================="
echo " ESSENTIUM SYSTEM DIAGNOSTIC "
echo "=============================="

echo
echo "[+] Python Validation"
find python engine config -name "*.py" -exec python -m py_compile {} \;

echo
echo "[+] Solidity Validation"
find contracts -name "*.sol" -exec solcjs --bin --abi {} \;

echo
echo "[+] File Counts"
echo "Python Files: $(find python -name '*.py' | wc -l)"
echo "Solidity Files: $(find contracts -name '*.sol' | wc -l)"
echo "JS Files: $(find . -name '*.js' | wc -l)"
echo "TS/TSX Files: $(find . -name '*.ts' -o -name '*.tsx' | wc -l)"

echo
echo "[+] Disk Usage"
du -sh .

echo
echo "[+] Complete"
