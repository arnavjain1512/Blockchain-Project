// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientRecordContract {
    uint public totalRecords;

    struct PatientRecord {
        address provider;
        string data;
    }

    mapping(uint => PatientRecord) public records;

    event RecordAdded(uint recordId, address indexed provider, string data);
    event RecordTransferred(uint recordId, address indexed from, address indexed to);

    // Add a new patient record
    function addRecord(string memory data) public {
        records[totalRecords] = PatientRecord(msg.sender, data);
        emit RecordAdded(totalRecords, msg.sender, data);
        totalRecords++;
    }

    // Transfer a record to a different healthcare provider
    function transferRecord(uint recordId, address newProvider) public {
        require(recordId < totalRecords, "Invalid record ID");
        require(msg.sender == records[recordId].provider, "Not the owner");

        address oldProvider = records[recordId].provider;
        records[recordId].provider = newProvider;

        emit RecordTransferred(recordId, oldProvider, newProvider);
    }

    // Get a patient record (for frontend/web3.py convenience)
    function getRecord(uint recordId) public view returns (address, string memory) {
        require(recordId < totalRecords, "Invalid record ID");
        PatientRecord memory record = records[recordId];
        return (record.provider, record.data);
    }
}
