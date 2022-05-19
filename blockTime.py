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

def blockTxns(bs: int, be: int, gap: int = 100, xStep: int = 10):

    # 链接 rpc
    teleportClient = Web3(Web3.HTTPProvider('https://teleport-localvalidator.qa.davionlabs.com/'))
    teleportClient.middleware_onion.inject(geth_poa_middleware, layer=0)
    # block-txns 的二维数组
    data = [[],[]]

    if be == 0:
        be = teleportClient.eth.blockNumber
    if bs == 0 or gap != 100:
        bs = be - gap

    for i in range(bs, be):
        block = teleportClient.eth.getBlock(i)

        pprint([block.number,block.timestamp])

        data[0].append(i)
        data[1].append(block.timestamp)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.plot_date(k[0],k[1],'go--')
    ax.plot(data[0],data[1],'go--')

    ax.set_title('Txns per block')
    ax.set_xlabel('blockNums')
    ax.set_ylabel('Txns', fontdict={"family": "Times New Roman", "size": 25})

    ax.set_xticks(np.arange(data[0][0], data[0][-1] + xStep, xStep))
    fig.autofmt_xdate()

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='支持定义blockNum,或者获取最新区块'
    parser.add_argument("-bs", "--blockStart", help="起始区块", dest="bs", type=int, default=0)
    parser.add_argument("-be", "--blockEnd", help="截止区块", dest="be", type=int, default=0)
    parser.add_argument("-g", "--gap", help="区块间隔,用于自动获取起始区块", dest="g", type=int, default=100)
    args = parser.parse_args()

    blockTxns(args.bs,args.be,args.g)

