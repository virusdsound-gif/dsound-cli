const { ethers } = require("ethers");
require("dotenv").config();

async function main() {
    console.log("🌟 EssentiumTrade v11.1 Deployment - The Morning Star Layer");
    console.log("Network: Polygon Amoy Testnet\n");

    const provider = new ethers.JsonRpcProvider("https://rpc-amoy.polygon.technology");
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    console.log("Deploying from:", wallet.address);

    // ==================== UPDATE THESE ====================
    const abi = [ /* Paste full ABI here after compilation */ ];
    const bytecode = "0xYOUR_BYTECODE_HERE";   // Must start with 0x
    // ====================================================

    const factory = new ethers.ContractFactory(abi, bytecode, wallet);
    
    console.log("🚀 Deploying...");
    const contract = await factory.deploy();
    await contract.waitForDeployment();

    console.log("\n✅ SUCCESS!");
    console.log("Address:", await contract.getAddress());
    console.log("Explorer: https://amoy.polygonscan.com/address/" + await contract.getAddress());
}

main().catch(console.error);
