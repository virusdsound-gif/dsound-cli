const { ethers } = require("hardhat");

async function main() {
  console.log("🌟 Deploying EssentiumTrade — The Morning Star 🌟");

  const EssentiumTrade = await ethers.getContractFactory("EssentiumTrade");
  const contract = await EssentiumTrade.deploy();

  await contract.waitForDeployment();
  console.log("✅ Deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
