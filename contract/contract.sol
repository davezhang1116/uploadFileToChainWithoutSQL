pragma solidity = 0.8;
contract Storage{

    mapping (uint=>bytes32[]) public storageList;

    function random() private view returns (uint) {
        uint randomHash = uint(keccak256(abi.encodePacked(block.difficulty, block.timestamp, msg.sender)));
        return randomHash;
    } 

    function assign(bytes32[] memory byteList) public returns(uint) {
        uint hash = random();
        storageList[hash] = byteList;
        return hash;
    }

    function read(uint hash) public view returns(bytes32[] memory) {
       return storageList[hash];
    }
}

