pragma solidity = 0.8;
contract Storage{

    mapping (uint=>bytes32[]) public storageList;
    mapping (uint=>string) public nameList;

    function assign(string memory name ,bytes32[] memory byteList, uint hash) public  {
        storageList[hash] = byteList;
        nameList[hash] = name;
    }

    function read(uint hash) public view returns(bytes32[] memory) {
       return storageList[hash] ;
    }
    function readName(uint hash) public view returns(string memory){
        return nameList[hash];
    }
}
