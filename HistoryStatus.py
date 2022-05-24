
import time
import json
import requests
import argparse
from requests.exceptions import HTTPError
import pandas as pds


class AH:
    def __init__(self, env: str):
        self.env = env


    def getData(self, senders: list, pageNo: int, pageSize: int) -> list:
        envDict = {
            "q": "https://bridge.qa.davionlabs.com",
            "t": "https://bridge.testnet.teleport.network",
        }

        # 資料
        my_data = {
            "senders": senders,
            "pagination":{"current_page":pageNo,"page_size":pageSize}
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

    def getConsumingTimes(self, dataD):

        if dataD['send_tx_time'] == "0001-01-01T00:00:00Z" or dataD['receive_tx_time'] == "0001-01-01T00:00:00Z":
            return 0
        # 查询源链区块时间
        srcTimestamp = dataD['send_tx_time']
        send_tx_time = int(time.mktime(time.strptime(srcTimestamp, "%Y-%m-%dT%H:%M:%SZ")))
        # 查询目标链区块时间
        destTimestamp = dataD['receive_tx_time']
        receive_tx_time = int(time.mktime(time.strptime(destTimestamp, "%Y-%m-%dT%H:%M:%SZ")))

        return receive_tx_time - send_tx_time

    def getToken(self, src_chain: str, tokenAddress: str) -> str:
        filePath = {
            "q": "datas/qanet/chains.json",
            "t": "datas/testnet/chains.json"
        }

        chains = json.load(open(filePath[self.env],'r',encoding="utf-8"))

        for k, info in chains[src_chain].items():
            if info == tokenAddress:
                return k
        
        return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description='查询交易历史，并绘制耗时点位图'
    parser.add_argument("-s", "--senders", help="查询的钱包地址，支持多个", dest="s", type=str, default="")
    parser.add_argument("-e", "--env", help="查询的环境:q(qanet),t(testnet), 默认值为: qanet", dest="e", type=str, default="q")
    parser.add_argument("-pn", "--pageNo", help="查询数据的页码, 默认值为: 1", dest="pn", type=int, default=1)
    parser.add_argument("-ps", "--pageSize", help="查询数据的条数, 默认值为: 1000", dest="ps", type=int, default=1000)
    args = parser.parse_args()

    senders = args.s.split(",")

    ah = AH(args.e)
    dataS = ah.getData(senders, args.pn, args.ps)

    TELE = []
    USDT = []

    for data in dataS:
        tokenName = ah.getToken(data['src_chain'],data['send_token_address'])
        direction = f"{data['src_chain']} -> {data['dest_chain']}"
        status = data['status']
        send_tx_hash = data['send_tx_hash']
        receive_tx_hash = data['receive_tx_hash']
        amount = data['amount']
        sequence = data['sequence']
        duration = ah.getConsumingTimes(data)

        res = [tokenName, direction, status, duration, amount, sequence, send_tx_hash, receive_tx_hash]
        if res[0] == "usdt":
            USDT.append(res)
        elif res[0] == "tele":
            TELE.append(res)
    
    result = []
    [result.append(u) for u in USDT]
    [result.append(t) for t in TELE]

    df = pds.DataFrame(result)
    df.columns = ["tokenName", "direction", "status", "duration", "amount", "sequence", "send_tx_hash", "receive_tx_hash"]
    df.to_csv('result.xlsx')