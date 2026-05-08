// Essentium Grid Node Simulator
const nodes = new Map();
let harvestedTotal = 0;

class Node {
  constructor(name, type, frequency) {
    this.name = name;
    this.type = type;
    this.frequency = frequency;
    this.connections = [];
    this.basePaC = 2; // base per node per harvest
  }
}

function addNode(name, type, frequency) {
  if (nodes.has(name)) return;
  nodes.set(name, new Node(name, type, frequency));
  console.log(`✓ Node added: ${name} (${type}, ${frequency} Hz)`);
}

function connect(nodeA, nodeB) {
  const a = nodes.get(nodeA);
  const b = nodes.get(nodeB);
  if (!a || !b) return;
  if (!a.connections.includes(nodeB)) a.connections.push(nodeB);
  if (!b.connections.includes(nodeA)) b.connections.push(nodeA);
  console.log(`🔗 Connected ${nodeA} ↔ ${nodeB}`);
}

function harvest() {
  let total = 0;
  for (let [name, node] of nodes) {
    let nodeReward = node.basePaC;
    // resonance bonus for each connection
    const resonanceBonus = node.connections.length * 4; // 4 PaC per connection
    nodeReward += resonanceBonus;
    total += nodeReward;
    console.log(`  🌿 ${name} → ${nodeReward} PaC (base ${node.basePaC} + ${resonanceBonus} resonance)`);
  }
  // global connection bonus (once per connected pair)
  const uniquePairs = new Set();
  for (let [name, node] of nodes) {
    for (let conn of node.connections) {
      const pair = [name, conn].sort().join('-');
      uniquePairs.add(pair);
    }
  }
  const connectionBonus = uniquePairs.size * 2; // 2 PaC per unique connection
  total += connectionBonus;
  console.log(`  🔗 Connection bonus: ${connectionBonus} PaC`);
  harvestedTotal += total;
  console.log(`⛏️  Harvested ${total} PaC this cycle (total: ${harvestedTotal} PaC)\n`);
  return total;
}

// --- Execute the commands ---
addNode("Starlink-47", "starlink", 432);
addNode("Vivian-Core", "ai", 528);
connect("Starlink-47", "Vivian-Core");
console.log("\n=== Harvesting ===");
harvest();
