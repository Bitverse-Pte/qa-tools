from cProfile import label
from pprint import pprint
from web3 import Web3
from web3.auto import w3
import json
from web3.middleware import geth_poa_middleware
import time
import matplotlib.pyplot as plt
import numpy as np
import argparse

class QBlock:
    def __init__(self, rpc = "https://teleport-localvalidator.qa.davionlabs.com/"):
        self.client = Web3(Web3.HTTPProvider(rpc))
        self.client.middleware_onion.inject(geth_poa_middleware, layer=0)

    def get_none_blockeNum_hashs(self, hs: list, bs: int, be: int) -> list:
        
        res = [[],[]]
        for i in range(bs, be):
            block = self.client.eth.getBlock(i)

            for txn in block.transactions:
                txnStr = txn.hex()

                if txnStr in hs:
                    res[0].append((txnStr, i))
                # else:
                #     res[1].append(txnStr)
                    hs.remove(txnStr)
        
        res[1] = hs

        return res

