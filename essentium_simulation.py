import json
from datetime import datetime

class EssentiumDashboardSimulator:
    def __init__(self):
        self.days = 180
        self.delta_m = 95.0
        self.initial_suppression = 7.2
        self.resonance_base = 1.72

    def simulate(self):
        results = []
        final_psi = 0
        
        for day in range(self.days + 1):
            suppression = max(0.8, self.initial_suppression * (0.955 ** (day * 0.75)))
            rt = self.resonance_base * (1 + 0.048 * day)
            t_inv = 1 + (day * 0.014)
            
            psi_e = (self.delta_m * rt) / (suppression * t_inv)
            total_resonance = psi_e * (1 + day * 0.011)
            
            results.append({
                "day": day,
                "psi_e": round(psi_e, 2),
                "suppression": round(suppression, 2),
                "total_resonance": round(total_resonance, 2),
                "dominant_freq": "369 Hz" if day > 100 else "0.7 Hz" if day < 40 else "200 Hz"
            })
            
            final_psi = psi_e

        # Save for Dashboard
        dashboard_data = {
            "simulation_date": datetime.now().isoformat(),
            "current_psi_e": round(final_psi, 2),
            "peak_psi_e": max(r["psi_e"] for r in results),
            "days": self.days,
            "morning_star_active": True,
            "dominant_layer": "The Morning Star 🌟",
            "last_30_days": results[-30:]
        }

        with open("essentium_dashboard_data.json", "w") as f:
            json.dump(dashboard_data, f, indent=2)

        print(f"✅ Dashboard data generated!")
        print(f"Current Ψ(E): {final_psi:.2f}")
        print(f"Peak Ψ(E): {max(r['psi_e'] for r in results):.2f}")
        print("File saved: essentium_dashboard_data.json")

        return dashboard_data

if __name__ == "__main__":
    sim = EssentiumDashboardSimulator()
    sim.simulate()
