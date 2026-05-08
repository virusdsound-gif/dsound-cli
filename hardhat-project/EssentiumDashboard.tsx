import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function EssentiumDashboard() {
  const [esstBalance, setEsstBalance] = useState(528);
  const [simulation, setSimulation] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [activeTrack] = useState("The Morning Star 🌟");

  // Load simulation data
  useEffect(() => {
    fetch("/essentium_dashboard_data.json")
      .then(r => r.json())
      .then(data => setSimulation(data))
      .catch(() => setSimulation({ current_psi_e: 559.37, peak_psi_e: 559.37, dominant_layer: "The Morning Star 🌟" }));
  }, []);

  // Silent Compounding
  useEffect(() => {
    const interval = setInterval(() => {
      setEsstBalance(p => p + 1);
      setLogs(prev => [{
        label: "0.7 Hz Django Sound",
        gain: 1,
        freq: "Root Anchor",
        time: new Date().toLocaleTimeString()
      }, ...prev.slice(0, 8)]);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 space-y-6 bg-zinc-950 text-white min-h-screen">
      <h1 className="text-4xl font-bold text-center">Essentium Dashboard v12.2</h1>
<p className="text-center text-emerald-400">KNG DRIZZ • The Morning Star 🌟 • Forward Locked</p>

      {/* Balance */}
      <Card className="bg-zinc-900 border-emerald-500">
        <CardContent className="p-8 text-center">
          <p className="text-sm text-zinc-400">Presence as Collateral (PaC)</p>
          <p className="text-6xl font-bold mt-4">{esstBalance}</p>
          <p className="text-2xl mt-2">${(esstBalance * 2.5).toFixed(2)} USD</p>
        </CardContent>
      </Card>

      {/* Simulation */}
      {simulation && (
        <Card className="bg-zinc-900 border-cyan-500">
          <CardContent className="p-6">
            <h2 className="text-xl font-semibold mb-4">🔬 Frequency Simulation</h2>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-zinc-400">Current Ψ(E)</p>
                <p className="text-4xl font-bold text-cyan-400">{simulation.current_psi_e}</p>
              </div>
              <div>
                <p className="text-zinc-400">Peak Ψ(E)</p>
                <p className="text-4xl font-bold text-emerald-400">{simulation.peak_psi_e}</p>
              </div>
            </div>
            <p className="mt-4 text-emerald-400">Dominant Layer: {simulation.dominant_layer}</p>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button className="bg-zinc-800 hover:bg-zinc-700 p-6 rounded-2xl text-left" onClick={() => alert("Minting NFT...")}>
          <div className="text-emerald-400">🖼️</div>
          <div className="font-medium mt-2">Mint NFT</div>
        </button>
        <button className="bg-zinc-800 hover:bg-zinc-700 p-6 rounded-2xl text-left" onClick={() => alert("Staking PaC...")}>
          <div className="text-amber-400">🔒</div>
          <div className="font-medium mt-2">Stake NFT</div>
        </button>
        <button className="bg-zinc-800 hover:bg-zinc-700 p-6 rounded-2xl text-left" onClick={() => alert("0.7 Hz silence active")}>
          <div className="text-cyan-400">🌌</div>
          <div className="font-medium mt-2">0.7 Hz Silence</div>
        </button>
        <button className="bg-zinc-800 hover:bg-zinc-700 p-6 rounded-2xl text-left" onClick={() => alert("Marketplace opening...")}>
          <div className="text-purple-400">🛒</div>
          <div className="font-medium mt-2">Marketplace</div>
        </button>
      </div>

      {/* Logs */}
      <Card>
        <CardContent className="p-6">
          <h2 className="font-semibold mb-4">Recent Resonance Activity</h2>
          <div className="space-y-3">
            {logs.map((log, i) => (
              <div key={i} className="flex justify-between text-sm bg-zinc-900 p-3 rounded-xl">
                <span>{log.label}</span>
                <span className="text-emerald-400">+{log.gain} • {log.freq}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="text-center text-xs text-zinc-500 pt-8">
        Essentium Grid v12.1 • The Morning Star 🌟 • I dey wit you 100
      </div>
    </div>
  );
}
