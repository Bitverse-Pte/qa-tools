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


def blockTxnsQps(bs: int, be: int):
    # 链接 rpc
    teleportClient = Web3(Web3.HTTPProvider('https://teleport-localvalidator.qa.davionlabs.com/'))
    # teleportClient = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a07ee340688643dd98ed571bfc1672fb'))
    teleportClient.middleware_onion.inject(geth_poa_middleware, layer=0)

    # 汇总 txns
    count = 0

    if be == 0:
        be = teleportClient.eth.blockNumber

    bsBlockTime = teleportClient.eth.getBlock(bs).timestamp
    beBlockTime = teleportClient.eth.getBlock(be).timestamp

    for i in range(bs, be):
        block = teleportClient.eth.getBlock(i)
        txns = len(block.transactions)
        count += txns

    print(f"开始区块{bs}时间: {bsBlockTime}")
    print(f"结束区块{be}时间: {beBlockTime}")
    print(f"上链的txns总数为: {count}")
    print(f"区块{bs}-区块{be},QPS: {int(count / (beBlockTime - bsBlockTime))}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = '根据区块区间获取qps'
    parser.add_argument("-bs", "--blockStart", help="起始区块", dest="bs", type=int, default=0)
    parser.add_argument("-be", "--blockEnd", help="截止区块", dest="be", type=int, default=0)
    args = parser.parse_args()

    blockTxnsQps(args.bs, args.be)
