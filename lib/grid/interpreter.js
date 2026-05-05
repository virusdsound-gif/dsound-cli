export function interpret(prompt) {
  if (prompt.includes("afrobeats")) {
    return { bpm: 95, style: "afrobeats", energy: 0.6 };
  }
  return { bpm: 80, style: "ambient", energy: 0.3 };
}
