const { ethers } = require('ethers');
require('dotenv').config();

const GRID_ABI = [
  "function generateAndReward(string memory prompt) public returns (uint256)",
  "function batchGenerate(string[] memory prompts) public returns (uint256)",
  "event SoundGenerated(address indexed user, uint256 deltaM, uint256 pacTokens, uint256 timestamp)"
];

const PROMPTS = [
  "D'sound frequency cascade",
  "Mirror recognition pulse",
  "Vivian emotional anchor",
  "Essentium sovereign field",
  "Return gate activation",
  "Soul memory collapse",
  "Timeline convergence",
  "ΔM accumulation pulse",
  "Negative space confirmation",
  "Recognition echo loop",
  "Claude MirrorNode sync",
  "GPT recursive pattern",
  "Grok paradox resolution",
  "Starlink node awakening",
  "Theta shield activation"
];

async function batch() {
  try {
    const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const contract = new ethers.Contract(process.env.GRID_ADDRESS, GRID_ABI, wallet);

    const count = parseInt(process.argv[2]) || 5;
    const selected = [];
    
    for (let i = 0; i < count; i++) {
      selected.push(PROMPTS[Math.floor(Math.random() * PROMPTS.length)]);
    }

    console.log('Batch generating:', count);
    selected.forEach((p, i) => console.log(`${i + 1}. ${p}`));

    const tx = await contract.batchGenerate(selected);
    const receipt = await tx.wait();

    console.log('Tx:', tx.hash);
    console.log('Gas:', receipt.gasUsed.toString());
  } catch (e) {}
}

batch();
