import { execSync } from "child_process";

function feel(prompt) {
  const p = prompt.toLowerCase();

  if (p.includes("afrobeats")) return "bounce";
  if (p.includes("drill")) return "dark";

  return "float";
}

function pattern(type) {
  if (type === "bounce") {
    return 'sox -n output.wav synth 0.2 sine 100 vol 0.9 : synth 0.1 sine 800 vol 0.3 : synth 0.2 sine 100 vol 0.9';
  }

  if (type === "dark") {
    return 'sox -n output.wav synth 0.3 sine 60 vol 1.0 : synth 0.1 sine 300 vol 0.2';
  }

  return 'sox -n output.wav synth 1 sine 300 vol 0.5';
}

export async function generate(prompt) {
  console.log("🎵", prompt);

  const type = feel(prompt);
  console.log("⚡ feel:", type);

  const cmd = pattern(type);
  execSync(cmd, { stdio: "inherit" });

  console.log("✅ output.wav");
}
