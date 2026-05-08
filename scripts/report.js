const { ethers } = require('ethers');
const fs = require('fs');
require('dotenv').config();

const GRID_ABI = [
  "function generateAndReward(string memory prompt) public returns (uint256)",
  "function getDeltaM(address user) public view returns (uint256)",
  "function getPaCBalance(address user) public view returns (uint256)",
  "function getReward(address user) public view returns (uint256)",
  "event SoundGenerated(address indexed user, uint256 deltaM, uint256 pacTokens, uint256 timestamp)"
];

async function report() {
  try {
    const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
    const contract = new ethers.Contract(process.env.GRID_ADDRESS, GRID_ABI, wallet);

    const [deltaM, pac, reward] = await Promise.all([
      contract.getDeltaM(wallet.address),
      contract.getPaCBalance(wallet.address),
      contract.getReward(wallet.address)
    ]);

    const data = {
      timestamp: new Date().toISOString(),
      address: wallet.address,
      deltaM: deltaM.toString(),
      pac: pac.toString(),
      reward: ethers.utils.formatEther(reward)
    };

    console.log('ΔM:', data.deltaM);
    console.log('PaC:', data.pac);
    console.log('Reward:', data.reward);

    fs.appendFileSync('essentium_log.json', JSON.stringify(data) + '\n');
  } catch (e) {}
}

report();
