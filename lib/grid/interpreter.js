export function interpret(prompt) {
  const lower = prompt.toLowerCase();

  if (lower.includes("afrobeats")) {
    return {
      bpm: 95,
      style: "afrobeats",
      energy: 0.7,
      pattern: "bounce"
    };
  }

  if (lower.includes("drill")) {
    return {
      bpm: 140,
      style: "drill",
      energy: 0.9,
      pattern: "dark"
    };
  }

  return {
    bpm: 80,
    style: "ambient",
    energy: 0.3,
    pattern: "slow"
  };
}
