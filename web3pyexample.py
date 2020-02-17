#!/usr/bin/env python
import sys
import time
import pprint


from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


w3 = Web3(EthereumTesterProvider())

contract_source_path = ('/home/skii/pythonVirtualEnv/IoTSC/IoTSmartContract.sol')
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))