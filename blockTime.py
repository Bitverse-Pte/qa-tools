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

def blockTxns(bs: int, be: int, gap: int = 100, xStep: int = 10,yStep: int = 60):

    # 链接 rpc
    teleportClient = Web3(Web3.HTTPProvider('https://teleport-localvalidator.qa.davionlabs.com/'))
    teleportClient.middleware_onion.inject(geth_poa_middleware, layer=0)
    # block-txns 的二维数组
    data = [[],[],[],[]]

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

    ax.set_title('time per block')
    ax.set_xlabel('blockNums')
    ax.set_ylabel('time', fontdict={"family": "Times New Roman", "size": 25})
    xticks= np.arange(data[0][0], data[0][-1] + xStep, xStep)
    for x in xticks:
        data[2].append(str(x))
    ax.set_xticks(xticks, data[2])
    yticks= np.arange(data[1][0], data[1][-1] + yStep, yStep)
    for ytime in yticks:
        x = time.localtime(ytime)
        timeStr=time.strftime('%H:%M:%S',x)
        data[3].append(timeStr)
    ax.set_yticks(yticks, data[3])
    fig.autofmt_xdate()

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='支持定义blockNum,或者获取最新区块'
    parser.add_argument("-bs", "--blockStart", help="起始区块", dest="bs", type=int, default=0)
    parser.add_argument("-be", "--blockEnd", help="截止区块", dest="be", type=int, default=0)
    parser.add_argument("-g", "--gap", help="区块间隔,用于自动获取起始区块", dest="g", type=int, default=100)
    parser.add_argument("-xs", "--xStep", help="x轴间隔（区块）", dest="xs", type=int, default=10)
    parser.add_argument("-ys", "--yStep", help="y轴间隔（时间秒）", dest="ys", type=int, default=60)
    args = parser.parse_args()

    blockTxns(args.bs,args.be,args.g,args.xs,args.ys)

