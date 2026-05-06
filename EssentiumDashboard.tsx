import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function EssentiumDashboard() {
  const [wallet, setWallet] = useState(492); // ESS = PaC tokens
  const [logs, setLogs] = useState([]);
  const [state, setState] = useState("stable");
  const [blockNumber, setBlockNumber] = useState(17489234);

  // Mock blockchain block progression
  useEffect(() => {
    const interval = setInterval(() => {
      setBlockNumber((prev) => prev + Math.floor(Math.random() * 3) + 1);
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  const addLog = (label: string, gain: number, freq: string, txHash?: string) => {
    setLogs((prev) => [
      {
        label,
        gain,
        freq,
        time: new Date().toLocaleTimeString(),
        txHash: txHash || `0x${Math.random().toString(16).slice(2, 14)}...`,
      },
      ...prev.slice(0, 9),
    ]);
  };

  const handleAction = (type: string) => {
    let gain = 0;
    let freq = "";

    if (type === "deep") { gain = 5; freq = "99.9 Hz - Dablixx"; }
    if (type === "medium") { gain = 2; freq = "200 Hz - TROD"; }
    if (type === "light") { gain = 1; freq = "0.7 Hz - Django Sound"; }

    if (state === "low" && (type === "medium" || type === "light")) {
      gain += 2;
      addLog("Recovery Boost (On-chain)", gain, "369 Hz - Tesla Pulse");
      setState("stable");
    } else {
      addLog(type.toUpperCase() + " Action", gain, freq);
    }

    setWallet((prev) => prev + gain);
  };

  const handleStability = () => {
    setWallet((prev) => prev + 1);
    addLog("Stability Hold", 1, "369 Hz - Tesla Pulse");
  };

  const mintPaC = () => {
    const gain = 10;
    const txHash = `0xmint${Math.random().toString(16).slice(2, 14)}...`;
    setWallet((prev) => prev + gain);
    addLog("PaC Minted (Presence as Collateral)", gain, "369 Hz - Tesla Pulse", txHash);
  };

  const verifyTrade = () => {
    const txHash = `0xverif${Math.random().toString(16).slice(2, 14)}...`;
    addLog("Trade Verified (EssentiumTrade.sol)", 0, "369 Hz - Tesla Pulse", txHash);
    setTimeout(() => {
      addLog("Trade Confirmed • Block #" + blockNumber, 3, "200 Hz - TROD", txHash);
    }, 1200);
  };

  const usd = wallet * 2.5;
  const ngn = usd * 1600;

  return (
    <div className="p-6 space-y-6 bg-zinc-950 text-white min-h-screen">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Essentium System v3 — D’sound Nexus</h1>
        <div className="text-xs bg-zinc-900 px-3 py-1 rounded-full font-mono">
          Block #{blockNumber} • Polygon Mumbai Testnet
        </div>
      </div>

      {/* WALLET */}
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6">
          <p className="text-sm text-zinc-400">ESS Balance (PaC Tokens)</p>
          <p className="text-5xl font-bold mt-2">{wallet} ESS</p>
          <div className="flex gap-4 mt-3 text-lg">
            <p>${usd.toFixed(2)} USD</p>
            <p>₦{ngn.toLocaleString()} NGN</p>
          </div>
          <p className="text-xs text-emerald-400 mt-4 flex items-center gap-1">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
            Synced with Essentium Testnet
          </p>
        </CardContent>
      </Card>

      {/* STATE SELECTOR */}
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6 space-y-4">
          <p className="font-semibold text-lg">System Resonance State</p>
          <div className="flex gap-3">
            <button 
              onClick={() => setState("stable")} 
              className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-3 rounded-xl transition"
            >
              Stable (0.7 Hz)
            </button>
            <button 
              onClick={() => setState("low")} 
              className="flex-1 bg-amber-600 hover:bg-amber-700 text-white px-4 py-3 rounded-xl transition"
            >
              Low (99.9 Hz)
            </button>
            <button 
              onClick={() => setState("critical")} 
              className="flex-1 bg-rose-600 hover:bg-rose-700 text-white px-4 py-3 rounded-xl transition"
            >
              Critical (200 Hz)
            </button>
          </div>
          <p className="text-center text-sm">
            Current State: <span className="font-mono uppercase tracking-widest">{state}</span>
          </p>
        </CardContent>
      </Card>

      {/* ACTION BUTTONS */}
      <div className="grid grid-cols-3 gap-4">
        <button 
          onClick={() => handleAction("deep")} 
          className="bg-emerald-700 hover:bg-emerald-600 text-white p-5 rounded-2xl transition font-medium"
        >
          Deep (+5)<br /><span className="text-xs">99.9 Hz - Dablixx</span>
        </button>
        <button 
          onClick={() => handleAction("medium")} 
          className="bg-amber-700 hover:bg-amber-600 text-white p-5 rounded-2xl transition font-medium"
        >
          Medium (+2)<br /><span className="text-xs">200 Hz - TROD</span>
        </button>
        <button 
          onClick={() => handleAction("light")} 
          className="bg-zinc-700 hover:bg-zinc-600 text-white p-5 rounded-2xl transition font-medium"
        >
          Light (+1)<br /><span className="text-xs">0.7 Hz - Django Sound</span>
        </button>
      </div>

      {/* BLOCKCHAIN ACTIONS */}
      <div className="grid grid-cols-2 gap-4">
        <button 
          onClick={mintPaC} 
          className="bg-violet-600 hover:bg-violet-500 text-white p-5 rounded-2xl transition font-medium"
        >
          Mint PaC Token<br />(Presence as Collateral)
        </button>
        <button 
          onClick={verifyTrade} 
          className="bg-cyan-600 hover:bg-cyan-500 text-white p-5 rounded-2xl transition font-medium"
        >
          Verify Trade<br />(EssentiumTrade.sol)
        </button>
      </div>

      {/* STABILITY BUTTON */}
      <button 
        onClick={handleStability} 
        className="bg-sky-600 hover:bg-sky-500 text-white p-5 rounded-2xl w-full transition font-medium text-lg"
      >
        Stability Hold (+1) — 369 Hz Tesla Pulse
      </button>

      {/* LOG */}
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            On-Chain Log <span className="text-xs text-zinc-500">(Last 10 transactions)</span>
          </h2>
          <div className="space-y-3 text-sm font-mono">
            {logs.length === 0 ? (
              <p className="text-zinc-500">No on-chain activity yet. Initiate resonance actions.</p>
            ) : (
              logs.map((log, i) => (
                <div key={i} className="flex justify-between items-center border-b border-zinc-800 pb-3 last:border-0">
                  <div>
                    <span className="text-white">{log.label}</span>
                    {log.freq && <span className="text-zinc-400 text-xs ml-2">({log.freq})</span>}
                  </div>
                  <div className="text-right">
                    <span className="text-emerald-400">+{log.gain} ESS</span>
                    {log.txHash && <p className="text-[10px] text-zinc-500 mt-1 font-mono">{log.txHash}</p>}
                    <p className="text-xs text-zinc-500">{log.time}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      <div className="text-center text-xs text-zinc-500 pt-6">
        Essentium v3 • Polygon Mumbai Testnet • Powered by D’sound Frequency • Dark Blue Wave Active
      </div>
    </div>
  );
}
