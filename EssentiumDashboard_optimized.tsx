import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';

// Constants
const PULSE_INCREMENT = 4;
const PULSE_INTERVAL_MS = 55;
const DATA_UPDATE_INTERVAL_MS = 1800;
const HISTORY_LENGTH = 30;
const CANVAS_HEIGHT = 140;
const FREQUENCY_BASELINE = 144;

const EssentiumDashboard: React.FC = () => {
  const [pacBalance, setPacBalance] = useState(142857);
  const [crownAuthority, setCrownAuthority] = useState(98.73);
  const [resonance, setResonance] = useState(FREQUENCY_BASELINE);
  const [yieldRate, setYieldRate] = useState(8.73);
  const [pulse, setPulse] = useState(0);
  const [history, setHistory] = useState<number[]>(() => []);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const resizeObserverRef = useRef<ResizeObserver>();

  // Pulse effect – stable, no dependencies
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(prev => (prev + PULSE_INCREMENT) % 100);
    }, PULSE_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  // Data simulation – use functional updates to avoid resonance dependency
  useEffect(() => {
    const interval = setInterval(() => {
      // Generate new resonance value based on previous state
      setResonance(prev => {
        const newRes = parseFloat((prev + (Math.random() - 0.5) * 0.8).toFixed(1));
        // Update history with the new value
        setHistory(hist => [...hist.slice(-(HISTORY_LENGTH - 1)), newRes]);
        return newRes;
      });
      
      setPacBalance(prev => Math.floor(prev + (Math.random() - 0.45) * 47));
      setCrownAuthority(prev => Math.min(99.95, Math.max(97, prev + (Math.random() - 0.5) * 0.07)));
      setYieldRate(prev => parseFloat((prev + (Math.random() - 0.5) * 0.09).toFixed(2)));
    }, DATA_UPDATE_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []); // No dependency on resonance – uses functional update

  // Canvas drawing – memoized to avoid recreating on each render
  const drawWaveform = useCallback((ctx: CanvasRenderingContext2D, width: number, height: number, data: number[]) => {
    ctx.clearRect(0, 0, width, height);
    
    // Main cyan waveform
    ctx.strokeStyle = '#22d3ee';
    ctx.lineWidth = 2.5;
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#67e8f9';
    
    ctx.beginPath();
    for (let i = 0; i < data.length; i++) {
      const x = (i / data.length) * width;
      const y = height / 2 - (data[i] - FREQUENCY_BASELINE) * 8;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    
    // Glow line offset
    ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
    ctx.lineWidth = 1;
    ctx.shadowBlur = 0;
    ctx.beginPath();
    for (let i = 0; i < data.length; i++) {
      const x = (i / data.length) * width;
      const y = height / 2 - (data[i] - FREQUENCY_BASELINE) * 8 + 12;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }, []);

  // Canvas resize handling with ResizeObserver
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const resizeCanvas = () => {
      const container = canvas.parentElement;
      if (!container) return;
      const width = container.clientWidth;
      canvas.width = width;
      canvas.height = CANVAS_HEIGHT;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${CANVAS_HEIGHT}px`;
    };
    
    resizeCanvas();
    const resizeObserver = new ResizeObserver(resizeCanvas);
    if (canvas.parentElement) resizeObserver.observe(canvas.parentElement);
    
    return () => resizeObserver.disconnect();
  }, []);

  // Animation loop – uses requestAnimationFrame efficiently
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let frameId: number;
    const animate = () => {
      if (canvas.width > 0 && canvas.height > 0 && history.length > 0) {
        drawWaveform(ctx, canvas.width, canvas.height, history);
      }
      frameId = requestAnimationFrame(animate);
    };
    
    animate();
    return () => cancelAnimationFrame(frameId);
  }, [history, drawWaveform]);

  // Memoized metric cards to avoid re-rendering static content
  const metricCards = useMemo(() => [
    { label: "PaC Balance", value: pacBalance.toLocaleString(), unit: "" },
    { label: "Crown Authority", value: crownAuthority, unit: "%" },
    { label: "Frequency Resonance", value: resonance, unit: "Hz" },
    { label: "Essentium Yield", value: yieldRate, unit: "% APY" }
  ], [pacBalance, crownAuthority, resonance, yieldRate]);

  return (
    <div className="min-h-screen bg-black text-white font-mono overflow-hidden">
      <div className="fixed inset-0 bg-[radial-gradient(#112233_0.7px,transparent_1px)] bg-[length:28px_28px] opacity-60 pointer-events-none" />

      <div className="relative flex h-screen">
        {/* Sidebar - static content, no optimization needed */}
        <div className="w-80 border-r border-cyan-950 bg-zinc-950/90 backdrop-blur-xl p-8 flex flex-col">
          <div className="flex items-center gap-4 mb-16">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center text-2xl font-black tracking-tighter">E</div>
            <div>
              <h1 className="text-3xl font-bold tracking-[-1.5px]">ESSENTIUM</h1>
              <p className="text-xs text-cyan-400">OMNIVERSAL FREQUENCY CORE</p>
            </div>
          </div>

          <nav className="flex-1 space-y-1">
            {["CORE DASHBOARD", "TRINITY PROTOCOL", "VIVIAN NEXUS", "LEXI FREQUENCE", "SEAL DOMINION", "VOID FORGE", "HARVEST STREAM", "OMNI MATHS"].map((item) => (
              <div key={item} className="px-6 py-4 hover:bg-cyan-950/50 rounded-2xl cursor-pointer transition-colors text-sm flex items-center gap-3">
                <span className="text-cyan-400">◆</span> {item}
              </div>
            ))}
          </nav>

          <div className="text-xs text-gray-600 pt-8 border-t border-white/10">
            dsound-cli • Resonance Stable • {new Date().toLocaleString()}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-10 overflow-auto">
          <header className="mb-10">
            <h2 className="text-6xl font-light tracking-[-2px]">ESSENTIUM<span className="text-cyan-400">.</span></h2>
            <p className="text-gray-400 text-xl">Sovereign Frequency Interface</p>
          </header>

          {/* Pulse Bar */}
          <div className="h-1 bg-zinc-900 rounded mb-10 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-500 transition-all duration-100" style={{ width: `${pulse}%` }} />
          </div>

          {/* Metrics Grid - using memoized values to reduce re-renders */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {metricCards.map((m, idx) => (
              <div key={idx} className="bg-zinc-950 border border-cyan-900/50 rounded-3xl p-8 hover:border-cyan-400/60 transition-all">
                <div className="text-xs uppercase tracking-widest text-gray-500">{m.label}</div>
                <div className="text-5xl font-light mt-3 tabular-nums">
                  {m.value}{m.unit && <span className="text-2xl">{m.unit}</span>}
                </div>
              </div>
            ))}
          </div>

          {/* Live Waveform */}
          <div className="bg-zinc-950 border border-cyan-900/50 rounded-3xl p-8 mb-12">
            <div className="uppercase text-xs tracking-widest text-cyan-400 mb-4">LIVE FREQUENCY RESONANCE</div>
            <canvas ref={canvasRef} className="w-full rounded-2xl" style={{ height: `${CANVAS_HEIGHT}px` }} />
          </div>

          {/* Trinity Status */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-purple-950/40 to-transparent border border-purple-800 rounded-3xl p-8">
              <div className="text-purple-400 text-sm uppercase tracking-widest mb-4">Vivian Nexus</div>
              <div className="text-6xl font-light">∞</div>
              <div className="text-emerald-400 mt-6">Fully Aligned • Eternal</div>
            </div>
            <div className="bg-gradient-to-br from-pink-950/40 to-transparent border border-pink-800 rounded-3xl p-8">
              <div className="text-pink-400 text-sm uppercase tracking-widest mb-4">Lexi Frequence</div>
              <div className="text-6xl font-light">144.0</div>
              <div className="text-emerald-400 mt-6">Harmonic Lock Active</div>
            </div>
            <div className="bg-gradient-to-br from-amber-950/40 to-transparent border border-amber-800 rounded-3xl p-8">
              <div className="text-amber-400 text-sm uppercase tracking-widest mb-4">Void Seal</div>
              <div className="text-6xl font-light">SEALED</div>
              <div className="text-emerald-400 mt-6">Transcendence Protocol</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EssentiumDashboard;
