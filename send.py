import json, hashlib, os
from web3 import Web3
from eth_account import Account
import string
import random
from random import randint
from compressData import compressData
import gzip
from hashlib import blake2b
import shutil

contract_addr = "0x57b9b949bcABa68fEcbBEB843ee3f6E906F9a0d0"
abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "bytes32[]",
                "name": "byteList",
                "type": "bytes32[]"
            },
            {
                "internalType": "uint256",
                "name": "hash",
                "type": "uint256"
            }
        ],
        "name": "assign",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "nameList",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "hash",
                "type": "uint256"
            }
        ],
        "name": "read",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "hash",
                "type": "uint256"
            }
        ],
        "name": "readName",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "storageList",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider("https://network.ambrosus.io"))
web3 = w3
contract = web3.eth.contract(address = contract_addr , abi = abi)

def upload_file(filename):

    chunk_len = 290000
    f = open("./files/"+filename, "rb")
    file_data = f.read()
    f.close()
    os.remove("./files/"+filename)
    hashList= []
    dirName = blake2b(str(randint(100000000000000000000000000000000000000000000000000000000000,	999999999999999999999999999999999999999999999999999999999999)).encode()).hexdigest()
    if len(file_data) > chunk_len:
        hash = randint(100000000000000000000000000000000000000000000000000000000000,
                       999999999999999999999999999999999999999999999999999999999999)
        compressData(file_data).split_file(chunk_len, dirName)
        part_count = 0
        fileList = os.listdir(dirName)
        fileList.sort()
        for file_name in fileList:
            acct = Account.create(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
            address = acct.address
            private_key=acct.privateKey.hex()
            nonce = 0
            f = open("./"+dirName+"/"+file_name, "rb")
            data = f.read()
            f.close()
            transaction =({
                    "chainId":"0x414e",
                    "from":address,
                    "nonce":nonce,
                    "to":address,
                    "value": 0,
                    "gas":20000000,
                    "gasPrice": 0,
                    "data": data
            })
            signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print("{}: {}".format(part_count, tx_hash.hex()))
            hashList.append(tx_hash.hex())
            part_count = part_count + 1
        shutil.rmtree(dirName, ignore_errors=True)
        acct = Account.create(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        address = acct.address
        private_key=acct.privateKey.hex()
        contractTx = contract.functions.assign(filename, hashList, hash).buildTransaction({
            "chainId":"0x414e",
            "from": address,
            "nonce": 0,
            "value": 0,
            "gasPrice": 0
        })
        ContractSignedTx = w3.eth.account.sign_transaction(contractTx, private_key=private_key)
        ContractTxHash = w3.eth.send_raw_transaction(ContractSignedTx.rawTransaction)

        print("contractTx: {}".format(ContractTxHash.hex()))
        return hash
    else:
        hash = randint(1000000000000000000000000000000000000000000000000000000000000,
                       9999999999999999999999999999999999999999999999999999999999999)

        acct = Account.create(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        address=acct.address
        private_key=acct.privateKey.hex()
        nonce = w3.eth.getTransactionCount(address)
        transaction =({
                "chainId":"0x414e",
                "from":address,
                "nonce":nonce,
                "to":address,
                "value": 0,
                "gas":21000000,
                "gasPrice": 0,
                "data": file_data
        })
        signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        contractTx = contract.functions.assign(filename, [tx_hash.hex()], hash).buildTransaction({
            "chainId":"0x414e",
            "from":address,
            "nonce": nonce+1,
            "value": 0,
            "gas":4000000,
            "gasPrice": 0
        })
        ContractSignedTx = w3.eth.account.sign_transaction(contractTx, private_key=private_key)
        ContractTxHash = w3.eth.send_raw_transaction(ContractSignedTx.rawTransaction)
        print("contractTx: {}".format(ContractTxHash.hex()))
        print("txHash: {}".format(tx_hash.hex()))
        return hash

def download_file(hash):
    hash = int(hash)
    w3 = Web3(Web3.HTTPProvider("https://network.ambrosus.io"))
    filename = contract.functions.readName(hash).call()
    hash_list = contract.functions.read(hash).call()
    print(filename, hash_list)
    data_all = b""
    try:
        os.mkdir("downloaded_files") 
    except:
        pass
    for hash in hash_list:
        print(hash.hex())
        data = bytes.fromhex(w3.eth.getTransaction(hash.hex())['input'][2:])
        data_all = data_all+data
    try:
        data = gzip.decompress(data_all)
    except:
        data = data_all
    return data, filename
