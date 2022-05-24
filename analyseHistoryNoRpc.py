
import time
import requests
import argparse
from requests.exceptions import HTTPError
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from web3 import Web3
from web3.middleware import geth_poa_middleware

class AH:
    def __init__(self, env: str):
        self.timeOut = 120

        # 链接 rpc
        self.aC = Web3(Web3.HTTPProvider('https://rinkeby.arbitrum.io/rpc', request_kwargs={'timeout': self.timeOut}))
        self.aC.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.bC = Web3(Web3.HTTPProvider('https://data-seed-prebsc-2-s2.binance.org:8545', request_kwargs={'timeout': self.timeOut}))
        self.bC.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.qC = Web3(Web3.HTTPProvider('https://teleport-localvalidator.qa.davionlabs.com/', request_kwargs={'timeout': self.timeOut}))
        self.qC.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.rC = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/a07ee340688643dd98ed571bfc1672fb', request_kwargs={'timeout': self.timeOut}))
        self.rC.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.tC = Web3(Web3.HTTPProvider('https://evm-rpc.testnet.teleport.network', request_kwargs={'timeout': self.timeOut}))
        self.tC.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.env = env


    def getData(self, senders: list, pageSize: int) -> list:
        envDict = {
            "q": "https://bridge.qa.davionlabs.com",
            "t": "https://bridge.testnet.teleport.network",
        }

        # 資料
        my_data = {
            "senders": senders,
            "pagination":{"current_page":1,"page_size":pageSize}
        }
        headers = {'content-type' : 'application/json'}
        url = f"{envDict[self.env]}/bridge/packet/history"

        try:
            response = requests.post(url, headers=headers, json = my_data)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        
        return response.json()["data"]["history"]

    def getBlockTimestamp(self, chainName: str, blockNum: int):
        if chainName == "arbitrum":
            block = self.aC.eth.getBlock(blockNum)
            timestamp = block.timestamp

        elif chainName == "bsctest":
            block = self.bC.eth.getBlock(blockNum)
            timestamp = block.timestamp

        elif chainName == "rinkeby":
            block = self.rC.eth.getBlock(blockNum)
            timestamp = block.timestamp

        elif chainName == "teleport" and self.env == "q":
            block = self.qC.eth.getBlock(blockNum)
            timestamp = block.timestamp

        elif chainName == "teleport" and self.env == "t":
            block = self.tC.eth.getBlock(blockNum)
            timestamp = block.timestamp

        return timestamp

    def getConsumingTimes(self, dataD):

        # 查询源链区块时间
        srcTimestamp = dataD['send_tx_time']
        send_tx_time = int(time.mktime(time.strptime(srcTimestamp, "%Y-%m-%dT%H:%M:%SZ")))
        # 查询目标链区块时间
        destTimestamp = dataD['receive_tx_time']
        receive_tx_time = int(time.mktime(time.strptime(destTimestamp, "%Y-%m-%dT%H:%M:%SZ")))

        return receive_tx_time - send_tx_time

    def analyseData(self, ds: list):
        failS = []
        pendingS = []
        successS = []
        refundS = []
        for d in ds:
            if d["status"] == 3:
                failS.append(d)
            elif d["status"] == 1:
                pendingS.append(d)
            elif d["status"] == 2:
                successS.append(d)
            elif d["status"] == 4:
                refundS.append(d)
            else:
                print(d)

        # 遍历 successS 获取点位信息
        raS = []
        rbS = []
        rtS = []
        abS = []
        arS = []
        atS = []
        baS = []
        brS = []
        btS = []
        taS = []
        tbS = []
        trS = []

        for s in successS:
            # time.sleep(1)

            consumingTimes = self.getConsumingTimes(s)

            if s["src_chain"] == "rinkeby" and s["dest_chain"] == "arbitrum":
                raS.append(consumingTimes)
            elif s["src_chain"] == "rinkeby" and s["dest_chain"] == "bsctest":
                rbS.append(consumingTimes)
            elif s["src_chain"] == "rinkeby" and s["dest_chain"] == "teleport":
                rtS.append(consumingTimes)

            elif s["src_chain"] == "arbitrum" and s["dest_chain"] == "bsctest":
                abS.append(consumingTimes)
            elif s["src_chain"] == "arbitrum" and s["dest_chain"] == "rinkeby":
                arS.append(consumingTimes)
            elif s["src_chain"] == "arbitrum" and s["dest_chain"] == "teleport":
                atS.append(consumingTimes)

            elif s["src_chain"] == "bsctest" and s["dest_chain"] == "arbitrum":
                baS.append(consumingTimes)
            elif s["src_chain"] == "bsctest" and s["dest_chain"] == "rinkeby":
                brS.append(consumingTimes)
            elif s["src_chain"] == "bsctest" and s["dest_chain"] == "teleport":
                btS.append(consumingTimes)

            elif s["src_chain"] == "teleport" and s["dest_chain"] == "arbitrum":
                taS.append(consumingTimes)
            elif s["src_chain"] == "teleport" and s["dest_chain"] == "bsctest":
                tbS.append(consumingTimes)
            elif s["src_chain"] == "teleport" and s["dest_chain"] == "rinkeby":
                trS.append(consumingTimes)

        return [atS, taS, tbS, trS, rtS, btS, raS, arS, rbS, brS, abS, baS]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='查询交易历史，并绘制耗时点位图'
    parser.add_argument("-s", "--senders", help="查询的钱包地址，支持多个", dest="s", type=str, default="")
    parser.add_argument("-e", "--env", help="查询的环境:q(qanet),t(testnet), 默认值为: qanet", dest="e", type=str, default="q")
    parser.add_argument("-ps", "--pageSize", help="查询数据的条数, 默认值为: 1000", dest="ps", type=int, default=1000)
    args = parser.parse_args()

    senders = args.s.split(",")

    ah = AH(args.e)
    dataS = ah.getData(senders, args.ps)

    # lS = [
    #     [194, 194, 192, 194, 207, 195, 206, 191, 205, 199, 200, 190], 
    #     [-4, 12, -23, 4, 7, 13, 7, -4, -7, -8, -18, -20], 
    #     [20, 20, 22, 19, 23, 21, 21, 18], 
    #     [39, 44, 32, 33, 44, 35, 5498, 7326, 29, 29, 32, 38, 40, 31], 
    #     [166, 169, 154, 165, 167, 164, 177, 168, 170, 171, 725, 178, 144, 174, 151, 174, 155, 150], 
    #     [46, 47, 53, 45, 32, 32, 48], [135, 153, 152, 180, 151, 150, 165, 135, 120, 165], 
    #     [255, 285, 225, 5687, 7478, 227, 241, 226, 240, 240, 240, 225], 
    #     [166, 177, 177, 179, 200, 192, 202, 202, 173, 164, 173], 
    #     [71, 89, 7381, 54617, 70], 
    #     [226, 218, 218, 218, 237, 223, 229, 208, 211, 230, 230, 218], 
    #     [14, 60, 67, 51, 54]
    # ]
    
    lS = ah.analyseData(dataS)

    # 删除大于20分钟的数据
    for i in range(len(lS)):
        lS[i] = [k for k in lS[i] if k <= 900]

    # fig, axs = plt.subplots(3, 4, sharex=True, sharey=True)
    fig, axs = plt.subplots(3, 4, sharex=True)

    keyS = ['atS', 'taS', 'tbS', 'trS', 'rtS', 'btS', 'raS', 'arS', 'rbS', 'brS', 'abS', 'baS']
    k = 0
    for i in range(3):
        for j in range(4):
            # axs[i,j].plot([i for i in range(len(lS[k]))], lS[k], '--')
            sns.regplot(ax=axs[i, j], x=[i for i in range(len(lS[k]))], y=lS[k])
            axs[i,j].set_title(keyS[k])
            k += 1
    
    # Set common labels
    fig.supxlabel('simple count')
    fig.supylabel('consuming times by block timestamp(cross chain)')

    plt.tight_layout()
    plt.show()
