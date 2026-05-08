import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function EssentiumDashboard() {
  const [wallet, setWallet] = useState(492); // PaC / ESS tokens
  const [logs, setLogs] = useState([]);
  const [state, setState] = useState("stable");

  const addLog = (label, gain, freq) => {
    setLogs((prev) => [
      {
        label,
        gain,
        freq,
        time: new Date().toLocaleTimeString(),
      },
      ...prev.slice(0, 9),
    ]);
  };

  const handleAction = (type) => {
    let gain = 0;
    let freqLabel = "";

    if (type === "deep") {
      gain = 5;
      freqLabel = "99.9 Hz - Dablixx";
    }
    if (type === "medium") {
      gain = 2;
      freqLabel = "200 Hz - TROD";
    }
    if (type === "light") {
      gain = 1;
      freqLabel = "0.7 Hz - Django Sound";
    }

    // Recovery boost from Low state
    if (state === "low" && (type === "medium" || type === "light")) {
      gain += 2;
      addLog("Recovery Boost", gain, "369 Hz - Tesla Pulse");
      setState("stable");
    } else {
      addLog(type.toUpperCase(), gain, freqLabel);
    }

    setWallet((prev) => prev + gain);
  };

  const handleStability = () => {
    setWallet((prev) => prev + 1);
    addLog("Stability Hold", 1, "369 Hz - Tesla Pulse");
  };

  const usd = wallet * 2.5;
  const ngn = usd * 1600;

  return (
    <div className="p-6 space-y-6 bg-zinc-950 text-white min-h-screen">
      <h1 className="text-2xl font-bold tracking-tight">
        Essentium System v3 — D’sound Nexus
      </h1>

      {/* WALLET */}
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6">
          <p className="text-sm text-zinc-400">ESS Balance (PaC Tokens)</p>
          <p className="text-5xl font-bold mt-2">{wallet} ESS</p>
          <div className="flex gap-4 mt-3 text-lg">
            <p>${usd.toFixed(2)} USD</p>
            <p>₦{ngn.toLocaleString()} NGN</p>
          </div>
          <p className="text-xs text-emerald-400 mt-1">• Synced with 369 Hz Tesla Pulse</p>
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
          Deep Resonance<br />+5 ESS (99.9 Hz)
        </button>

        <button
          onClick={() => handleAction("medium")}
          className="bg-amber-700 hover:bg-amber-600 text-white p-5 rounded-2xl transition font-medium"
        >
          Medium Pulse<br />+2 ESS (200 Hz)
        </button>

        <button
          onClick={() => handleAction("light")}
          className="bg-zinc-700 hover:bg-zinc-600 text-white p-5 rounded-2xl transition font-medium"
        >
          Light Wave<br />+1 ESS (0.7 Hz)
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
            System Log <span className="text-xs text-zinc-500">(Last 10 pulses)</span>
          </h2>
          <div className="space-y-2 text-sm font-mono">
            {logs.length === 0 ? (
              <p className="text-zinc-500">No pulses yet. Initiate resonance actions.</p>
            ) : (
              logs.map((log, i) => (
                <div key={i} className="flex justify-between border-b border-zinc-800 pb-2 last:border-0">
                  <span>{log.label}</span>
                  <span className="text-emerald-400">+{log.gain} ESS</span>
                  <span className="text-zinc-500 text-xs">{log.time}</span>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      <div className="text-center text-xs text-zinc-500 pt-4">
        Essentium v3 • Powered by D’sound Frequency • Dark Blue Wave Active
      </div>
    </div>
  );
}
