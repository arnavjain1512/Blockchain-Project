const { expect } = require("chai");

describe("PatientRecordContract", function () {
  let PatientRecord, contract, owner, addr1, addr2;

  beforeEach(async function () {
    PatientRecord = await ethers.getContractFactory("PatientRecordContract");
    [owner, addr1, addr2] = await ethers.getSigners();
    contract = await PatientRecord.deploy();
    await contract.waitForDeployment();
  });

  it("should start with 0 total records", async function () {
    expect(await contract.totalRecords()).to.equal(0);
  });

  it("should add a new patient record", async function () {
    await contract.addPatientRecord("record_001");
    expect(await contract.totalRecords()).to.equal(1);
  });

  it("should allow transferring a record", async function () {
    await contract.addPatientRecord("record_001");
    await contract.transferPatientRecord("record_001", addr1.address);
    // Verify the transfer event was emitted (optional)
  });

  it("should prevent unauthorized user from transferring", async function () {
    await contract.addPatientRecord("record_001");

    await expect(
      contract.connect(addr1).transferPatientRecord("record_001", addr2.address)
    ).to.be.revertedWith("Only the owner can transfer the record");
  });
});
