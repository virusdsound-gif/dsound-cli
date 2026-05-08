#!/usr/bin/env python3
"""
Essentium System Health Check & Verification
"""

import os
import json
from datetime import datetime

def check_files():
    required = ["dsound", "essentium_simulation.py", "EssentiumDashboard.tsx", "essentium_dashboard_data.json"]
    missing = [f for f in required if not os.path.exists(f)]
    
    print("📁 File Check:")
    for f in required:
        status = "✅" if f not in missing else "❌"
        print(f"  {status} {f}")
    
    return len(missing) == 0

def check_simulation():
    try:
        with open("essentium_dashboard_data.json") as f:
            data = json.load(f)
        print(f"\n📊 Last Simulation: Ψ(E) = {data.get('current_psi_e', 'N/A')}")
        print(f"Peak: {data.get('peak_psi_e', 'N/A')} | Layer: {data.get('dominant_layer', 'N/A')}")
        return True
    except:
        print("\n⚠️  No simulation data yet. Run: ./dsound simulate")
        return False

if __name__ == "__main__":
    print("🔍 Essentium System Verification v10.3\n")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    files_ok = check_files()
    sim_ok = check_simulation()
    
    if files_ok and sim_ok:
        print("\n✅ System Status: HEALTHY & FORWARD-LOCKED")
    else:
        print("\n⚠️  System partially ready — run setup if needed.")
    
    print("\nI dey wit you 100.")
