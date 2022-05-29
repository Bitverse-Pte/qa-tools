from analyse_block.q_block import QBlock
from utils.File_Helper import FHelper

if __name__ == "__main__":
    fHelp = FHelper("./logs/nonce.log")

    fs = fHelp.read_lins()

    rpcList = ["http://10.41.20.51:8545", "http://10.42.20.51:8545", "http://10.43.20.51:8545"]

    res = fHelp.find_all("one,")
    listS = [[]]
    for r in res:
        for rpc in rpcList:
            if rpc in r:
                if "last one" in r:
                    strList = [[], [], [], [], [], [], []]
                    strList[0] = rpc
                    strList[1] = "last one"
                    strS = r.split(",")
                    for a in strS:
                        if "线程" in a:
                            strList[2] = a
                        if "requestNoce" in a:
                            strList[3] = a.split(":")[1]
                        if "returnNoce" in a:
                            strList[4] = a.split(":")[1]
                        if "address:" in a:
                            strList[5] = a.split(":")[1]
                        if "Hash:" in a:
                            strList[6] = a.split(":")[1]
                else:
                    if "one" in r:
                        strList = [[], [], [], [], [], [], []]
                    strList[0] = rpc
                    strList[1] = "one"
                    strS = r.split(",")
                    for a in strS:
                        if "线程" in a:
                            strList[2] = a
                        if "requestNoce" in a:
                            strList[3] = a.split(":")[1]
                        if "returnNoce" in a:
                            strList[4] = a.split(":")[1]
                        if "address:" in a:
                            strList[5] = a.split(":")[1]
                        if "Hash:" in a:
                            strList[6] = a.split(":")[1]
                listS.append(strList)

    fHelp.write_csv("stressNonce.csv", ["prcUrl", "type", "number", "requestNoce", "returnNoce", "address", "Hash"],
                    listS)
