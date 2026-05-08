async function main() {
  const Contract = await ethers.getContractFactory("EssentiumTrade");

  const contract = await Contract.deploy();

  await contract.waitForDeployment();

  console.log("Deployed:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
