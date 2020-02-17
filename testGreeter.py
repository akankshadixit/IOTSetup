import json
from eth_account import Account
from web3 import Web3
import time
from time import sleep

# Set up web3 connection with Ganache
ganache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
private_key = '578fae8a6f8ba0012f26efb58f9d47c95a8313c0aafc92af6fc2a5d9786026f3'

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"newGreeting","type":"string"}],"name":"ChangeGreeting","type":"event"},{"constant":true,"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
bytecode = '608060405234801561001057600080fd5b506040518060400160405280600e81526020017f48656c6c6f20416b616e6b7368610000000000000000000000000000000000008152506000908051906020019061005c929190610062565b50610107565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a357805160ff19168380011785556100d1565b828001600101855582156100d1579182015b828111156100d05782518255916020019190600101906100b5565b5b5090506100de91906100e2565b5090565b61010491905b808211156101005760008160009055506001016100e8565b5090565b90565b6104d7806101166000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c8063a413686214610046578063cfae321714610101578063ef690cc014610184575b600080fd5b6100ff6004803603602081101561005c57600080fd5b810190808035906020019064010000000081111561007957600080fd5b82018360208201111561008b57600080fd5b803590602001918460018302840111640100000000831117156100ad57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610207565b005b6101096102bd565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561014957808201518184015260208101905061012e565b50505050905090810190601f1680156101765780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b61018c61035f565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101cc5780820151818401526020810190506101b1565b50505050905090810190601f1680156101f95780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b806000908051906020019061021d9291906103fd565b507f5a631da45d24474bc287bf525da939b3c3ab2882fca8bef6721c8d513f4571af816040518080602001828103825283818151815260200191508051906020019080838360005b83811015610280578082015181840152602081019050610265565b50505050905090810190601f1680156102ad5780820380516001836020036101000a031916815260200191505b509250505060405180910390a150565b606060008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156103555780601f1061032a57610100808354040283529160200191610355565b820191906000526020600020905b81548152906001019060200180831161033857829003601f168201915b5050505050905090565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156103f55780601f106103ca576101008083540402835291602001916103f5565b820191906000526020600020905b8154815290600101906020018083116103d857829003601f168201915b505050505081565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061043e57805160ff191683800117855561046c565b8280016001018555821561046c579182015b8281111561046b578251825591602001919060010190610450565b5b509050610479919061047d565b5090565b61049f91905b8082111561049b576000816000905550600101610483565b5090565b9056fea265627a7a723158207e29f6988824cc2407f7e41db353af2d8c89c56e4a07a207c5122bfda8555b8664736f6c634300050d0032'

Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = Greeter.constructor().transact()

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

greeter = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
my_filter = greeter.events.ChangeGreeting.createFilter(fromBlock=0,toBlock='latest')
eventlist = my_filter.get_all_entries()


greeter.functions.greet().call()
tx_hash = greeter.functions.setGreeting('Nihao').transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tx_hash = greeter.functions.setGreeting('Dixit').transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
greeter.functions.greet().call()

tx_hash = greeter.functions.setGreeting('Akanksha').buildTransaction({
    'gas': 70000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'from': w3.eth.accounts[0],
    'nonce': w3.eth.getTransactionCount(w3.eth.defaultAccount)
})

signed  = w3.eth.account.signTransaction(tx_hash, private_key)
w3.eth.sendRawTransaction(signed.rawTransaction)

print(my_filter.get_all_entries())
'''for event in greeter_filter.get_new_entries():
    print ('change greeting event  is fired from contract')
time.sleep(2)
'''