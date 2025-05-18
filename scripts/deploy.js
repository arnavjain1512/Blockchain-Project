async function main() {
  const ContractFactory = await ethers.getContractFactory("PatientRecordContract");
  const contract = await ContractFactory.deploy(); // This deploys it
  await contract.waitForDeployment(); // Correct method in Hardhat Ethers v6

  console.log("Contract deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
