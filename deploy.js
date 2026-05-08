const { ethers } = require("ethers");
require("dotenv").config();

async function main() {
    console.log("🌟 EssentiumTrade.sol — The Morning Star 🌟 Deployment");
    console.log("Network: Polygon Amoy Testnet\n");

    const RPC_URL = "https://rpc-amoy.polygon.technology";
    const PRIVATE_KEY = process.env.PRIVATE_KEY;

    if (!PRIVATE_KEY) {
        console.error("❌ PRIVATE_KEY not found in .env file!");
        console.log("Create .env and add: PRIVATE_KEY=0xYourPrivateKeyHere");
        return;
    }

    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

    console.log("Deploying from:", wallet.address);

    // ==================== PASTE YOUR COMPILED DATA HERE ====================
    const abi = [
        // Paste full ABI array here (from compilation)
    ];

    const bytecode = "0xYOUR_FULL_BYTECODE_HERE";   // Must start with 0x
    // =====================================================================

    if (bytecode === "0xYOUR_FULL_BYTECODE_HERE" || abi.length === 0) {
        console.error("❌ Please update ABI and bytecode in deploy.js first!");
        return;
    }

    const factory = new ethers.ContractFactory(abi, bytecode, wallet);

    console.log("🚀 Deploying EssentiumTrade...");
    const contract = await factory.deploy();
    await contract.waitForDeployment();

    const address = await contract.getAddress();

    console.log("\n✅ DEPLOYMENT SUCCESSFUL!");
    console.log("📍 Contract Address:", address);
    console.log("\n🔗 View on Amoy Explorer:");
    console.log(`https://amoy.polygonscan.com/address/${address}`);
    
    console.log("\n💡 Next: Add this
cat > deploy.js << 'EOF'
const { ethers } = require("ethers");
require("dotenv").config();

async function main() {
    console.log("🌟 EssentiumTrade.sol — The Morning Star 🌟 Deployment");
    console.log("Network: Polygon Amoy Testnet\n");

    const RPC_URL = "https://rpc-amoy.polygon.technology";
    const PRIVATE_KEY = process.env.PRIVATE_KEY;

    if (!PRIVATE_KEY) {
        console.error("❌ PRIVATE_KEY not found in .env file!");
        console.log("Create .env and add: PRIVATE_KEY=0xYourPrivateKeyHere");
        return;
    }

    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

    console.log("Deploying from:", wallet.address);

    // ==================== PASTE YOUR COMPILED DATA HERE ====================
    const abi = [
        // Paste full ABI array here (from compilation)
    ];

    const bytecode = "0xYOUR_FULL_BYTECODE_HERE";   // Must start with 0x
    // =====================================================================

    if (bytecode === "0xYOUR_FULL_BYTECODE_HERE" || abi.length === 0) {
        console.error("❌ Please update ABI and bytecode in deploy.js first!");
        return;
    }

    const factory = new ethers.ContractFactory(abi, bytecode, wallet);

    console.log("🚀 Deploying EssentiumTrade...");
    const contract = await factory.deploy();
    await contract.waitForDeployment();

    const address = await contract.getAddress();

    console.log("\n✅ DEPLOYMENT SUCCESSFUL!");
    console.log("📍 Contract Address:", address);
    console.log("\n🔗 View on Amoy Explorer:");
    console.log(`https://amoy.polygonscan.com/address/${address}`);
    
    console.log("\n💡 Next: Add this address to your Essentium system.");
}

main().catch((error) => {
    console.error("❌ Deployment failed:", error.message);
});
