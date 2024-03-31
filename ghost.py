import json
import math
from statistics import mean
import time
from typing import Dict
from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_abi import encode
from eth_abi.packed import encode_packed
import requests
import random
from datetime import datetime
import config
import fun
from fun import ZERO_ADDRESS, log, log_error, log_ok, save_wallet_to


class Ghost:
    def __init__(self, private_key: str) -> None:
        self.private_key = private_key
        self.chain = "polygon"
        self.explorer = fun.address[self.chain]["scan"]

        self.w3 = Web3(Web3.HTTPProvider(fun.address[self.chain]['rpc'], request_kwargs=config.request_kwargs))
        self.account = self.w3.eth.account.from_key(private_key)
        self.wallet = self.address = self.account.address
        

    def get_contract(self, chain = "eth"):
        try:
            self.chain = chain
            self.explorer = fun.address[self.chain]["scan"]
            self.w3 = Web3(Web3.HTTPProvider(fun.address[self.chain]['rpc'], request_kwargs=config.request_kwargs))
            
            dapp_address = self.w3.to_checksum_address(fun.address[chain]["ghost_contract"])
            self.dapp_contract = self.w3.eth.contract(address=dapp_address, abi=fun.ghost_abi)          
            return self.dapp_contract
        except Exception as error:
            fun.log_error(f"Ошибка подключения к RPC {fun.address[chain]['rpc']}: {error}")
            return False        

    def get_balance_nfts_amount(self):
        return self.dapp_contract.functions.balanceOf(Web3.to_checksum_address(self.wallet)).call()

    def have_any_nft(self):
        for network_from in config.networks_from:
            try:
                if self.get_contract(network_from):
                    if self.get_balance_nfts_amount():
                        return True
            except Exception as error:
                continue
           
            
        return False

    def get_balance_nfts_id(self, i=0):
        self.token_id = self.dapp_contract.functions.tokenOfOwnerByIndex(Web3.to_checksum_address(self.wallet), i).call()
        return self.token_id


    def get_balance(self) -> Dict:
        balance = self.w3.eth.get_balance(self.wallet)
        balance_decimal = float(Web3.from_wei(balance, 'ether'))
        balance_USD = Web3.from_wei(balance*config.prices[fun.address[self.chain]['native']] , "ether")

        return balance, balance_decimal, balance_USD

    def get_tx_mint(self):
        gasPrice = self.w3.eth.gas_price
        fee = self.dapp_contract.functions.mintFee().call()
        transaction = self.dapp_contract.functions.mint().build_transaction({
                'from': self.wallet,
                'value': fee,
                'gasPrice': gasPrice,
                'nonce': self.w3.eth.get_transaction_count(self.wallet),
            })

        return transaction

    def estimateSendFee(
            self,
            toDstLzChainId: int,
            adapterParams: bytes
        ) -> (int, int):
        try:
            result = self.dapp_contract.functions.estimateSendFee(
                toDstLzChainId,
                self.address,
                self.token_id,
                False,
                adapterParams
            ).call()
        except Exception as error:
            log_error(":estimateSendFee: {error}")
            return False
        return result

    def get_tx_bridge(self, network_to):
        
        # minDstGas = self.dapp_contract.functions.minDstGasLookup(fun.address[network_to]['lzChainId'], 1).call()
        # adapterParams = encode_packed(
        #     ["uint16", "uint256"],
        #     [1, minDstGas] # lzVersion, gasLimit - extra for minting
        # )        
        
        adapterParams = "0x00010000000000000000000000000000000000000000000000000000000000030d40"

        nativeFee, _ = self.estimateSendFee(
            fun.address[network_to]['lzChainId'],
            adapterParams
        )

        gasPrice = self.w3.eth.gas_price
        
        transaction = self.dapp_contract.functions.sendFrom(
            self.address,
            fun.address[network_to]['lzChainId'],
            self.address,
            self.token_id,
            self.address,
            self.address,
            adapterParams
        ).build_transaction(
            {
                "from": self.address,
                "value": nativeFee,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                'gasPrice': gasPrice,
            }
        )        
        

        return transaction


    def get_full_fee_mint(self):
        fee = self.dapp_contract.functions.mintFee().call()
        gasPrice = self.w3.eth.gas_price
        transaction = self.get_tx_mint()
        gasLimit = int(self.w3.eth.estimate_gas(transaction)* config.gas_kef)
        komissiya = gasLimit * gasPrice
        full_fee = (komissiya+fee)
        full_fee_USD = Web3.from_wei(full_fee*config.prices[fun.address[self.chain]['native']] , "ether")
        
        return full_fee, full_fee_USD

    def get_full_fee_bridge(self, network_to):
        minDstGas = self.dapp_contract.functions.minDstGasLookup(fun.address[network_to]['lzChainId'], 1).call()
        adapterParams = encode_packed(
            ["uint16", "uint256"],
            [1, minDstGas] # lzVersion, gasLimit - extra for minting
        )        
        
        fee, _ = self.estimateSendFee(
            fun.address[network_to]['lzChainId'],
            adapterParams
        )
        gasPrice = self.w3.eth.gas_price
        transaction = self.get_tx_bridge(network_to)
        gasLimit = int(self.w3.eth.estimate_gas(transaction)* config.gas_kef)
        komissiya = gasLimit * gasPrice
        full_fee = (komissiya+fee)
        full_fee_USD = Web3.from_wei(full_fee*config.prices[fun.address[self.chain]['native']] , "ether")
        
        return full_fee, full_fee_USD


    def mint(self):
        transaction = self.get_tx_mint()
        signed_txn = self.sign(transaction)
        txn_hash = self.send_raw_transaction(signed_txn)
        return self.wait_until_tx_finished(txn_hash)
      
    def bridge(self, networks_to):
        transaction = self.get_tx_bridge(networks_to)
        signed_txn = self.sign(transaction)
        txn_hash = self.send_raw_transaction(signed_txn)
        return self.wait_until_tx_finished(txn_hash)

        
         




    def wait_until_tx_finished(self, hash: str, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    log_ok(f"  [{self.address}] {self.explorer}/{hash} successfully!")
                    return True
                elif status is None:
                    time.sleep(0.3)
                else:
                    log_error(f"  [{self.address}] {self.explorer}/{hash} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    log_error(f'FAILED TX: {self.explorer}/{hash}')
                    return False
                time.sleep(3)

    def sign(self, transaction):
        gas = self.w3.eth.estimate_gas(transaction)
        gas = int(gas * config.gas_kef)

        transaction.update({"gas": gas})
        if fun.address[self.chain]['type']:
            maxPriorityFeePerGas = self.w3.eth.max_priority_fee
            fee_history = self.w3.eth.fee_history(10, 'latest', [10, 90])
            baseFee=round(mean(fee_history['baseFeePerGas']))
            maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)

            del transaction['gasPrice']
            transaction['maxFeePerGas'] = maxFeePerGas
            transaction['maxPriorityFeePerGas'] = maxPriorityFeePerGas

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        return signed_txn

    def send_raw_transaction(self, signed_txn):
        txn_hash = self.w3.to_hex(self.w3.eth.send_raw_transaction(signed_txn.rawTransaction))

        return txn_hash
            