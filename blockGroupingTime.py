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
from utils.split_time_ranges import split_time_ranges


def blockGroupingTime(bs: int, be: int, xStep: int = 10, timeStep: int = 10):
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
    splitTime = split_time_ranges
    stat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bsBlockTime))
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(beBlockTime))
    frequency = 60 * timeStep
    print(stat + "!!" + end+"frequency:"+str(frequency))
    time_ranges = splitTime.split_time_rangesStr(stat, end, frequency)
    print(time_ranges)
    for timeList in time_ranges:
        data = [[], [], []]
        for i in range(bs, be):
            block = teleportClient.eth.getBlock(i)
            if block.timestamp >= int(time.mktime(time.strptime(timeList[0], "%Y-%m-%d %H:%M:%S"))) \
                    & block.timestamp <= int(time.mktime(time.strptime(timeList[1], "%Y-%m-%d %H:%M:%S"))):
                txns = len(block.transactions)
                count += txns
                data[0].append(i)
                data[1].append(txns)

        print(data)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # ax.plot_date(k[0],k[1],'go--')
        ax.plot(data[0], data[1], 'go--')
        ax.set_title("Txns per block(" + str(timeList[1]) + "——" + str(timeList[1]) + ")")
        ax.set_xlabel('blockNums')
        ax.set_ylabel('Txns', fontdict={"family": "Times New Roman", "size": 25})
        xticks = np.arange(data[0][0], data[0][-1] + xStep, xStep)
        for x in xticks:
            data[2].append(str(x))
        ax.set_xticks(xticks, data[2])
        fig.autofmt_xdate()
        plt.savefig("./img/" + str(timeList[0]) + "_" + str(timeList[1]))
        print("去/img/目录查看")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = '根据区块区间获取qps'
    parser.add_argument("-bs", "--blockStart", help="起始区块", dest="bs", type=int, default=0)
    parser.add_argument("-be", "--blockEnd", help="截止区块", dest="be", type=int, default=0)
    parser.add_argument("-ts", "--timeStep", help="时间间隔", dest="ts", type=int, default=10)
    parser.add_argument("-xs", "--xStep", help="x轴间隔（区块）", dest="xs", type=int, default=10)
    args = parser.parse_args()

    blockGroupingTime(args.bs, args.be, args.xs, args.ts)
