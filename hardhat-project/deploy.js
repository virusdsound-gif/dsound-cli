const { ethers } = require("ethers");
require("dotenv").config();
const fs = require("fs");

async function main() {
    console.log("🌟 Deploying with Auto-Address Save...");

    const provider = new ethers.JsonRpcProvider("https://rpc-amoy.polygon.technology");
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    // Deploy EssentiumTrade
    const TradeFactory = await ethers.getContractFactory("EssentiumTrade");
    const trade = await TradeFactory.deploy();
    await trade.waitForDeployment();
    const tradeAddr = await trade.getAddress();

    // Deploy Music NFT
    const NFTFactory = await ethers.getContractFactory("EssentiumMusicNFT");
    const nft = await NFTFactory.deploy(tradeAddr);   // PaC address = Trade address
    await nft.waitForDeployment();
    const nftAddr = await nft.getAddress();

    // Save addresses automatically
    const addresses = {
        "EssentiumTrade": tradeAddr,
        "EssentiumMusicNFT": nftAddr,
        "PaC_Token": tradeAddr,   // Trade contract also mints PaC
        "last_updated": new Date().toISOString()
    };

    fs.writeFileSync("../contract_addresses.json", JSON.stringify(addresses, null, 2));

    console.log("\n✅ DEPLOYMENT SUCCESSFUL!");
    console.log("EssentiumTrade :", tradeAddr);
    console.log("EssentiumMusicNFT:", nftAddr);
    console.log("\n📁 Addresses saved to contract_addresses.json");
}

main().catch(console.error);
