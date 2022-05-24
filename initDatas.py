import sh
import os
import json

# 下载abi文件
def getAbi():
	# 创建文件夹
	# 先删除
	sh.rm("-rf","contracts")
	# 再创建
	sh.mkdir("contracts")
	sh.mkdir("contracts/abis")
	sh.mkdir("contracts/client")
	sh.mkdir("contracts/multiCall")
	sh.mkdir("contracts/packet")
	sh.mkdir("contracts/proxy")
	sh.mkdir("contracts/eToken")
	sh.mkdir("contracts/transfer")
	sh.mkdir("contracts/tpTransfer")

	# 下载合约代码
	sh.git("clone","git@github.com:teleport-network/xibc-contracts.git")

	# 编译
	print("开始编译evm……")
	sh.cd("xibc-contracts/evm/")
	sh.yarn()
	sh.yarn("compile")

	# 写文件
	print("开始写入abi文件……")
	# TestToken.sol
	with open("artifacts/contracts/test/TestToken.sol/testToken.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/token.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# Transfer.sol
	with open("artifacts/contracts/apps/transfer/Transfer.sol/Transfer.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/transfer.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# Proxy.sol
	with open("artifacts/contracts/apps/agent/Proxy.sol/Proxy.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/proxy.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# MultiCall.sol
	with open("artifacts/contracts/apps/multicall/MultiCall.sol/MultiCall.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/multiCall.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)
		
	# ClientManager.sol
	with open("artifacts/contracts/core/client/ClientManager.sol/ClientManager.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/clientManager.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# Packet.sol
	with open("artifacts/contracts/core/packet/Packet.sol/Packet.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/packet.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# abigen
	print("开始生产go文件……")
	sh.cd("../../contracts/abis")
	sh.abigen("--abi=token.abi","--pkg=eToken","--out=../eToken/token.go")
	sh.abigen("--abi=transfer.abi","--pkg=transfer","--out=../transfer/transfer.go")
	sh.abigen("--abi=proxy.abi","--pkg=proxy","--out=../proxy/proxy.go")
	sh.abigen("--abi=multiCall.abi","--pkg=multiCall","--out=../multiCall/multiCall.go")
	sh.abigen("--abi=clientManager.abi","--pkg=client","--out=../client/client.go")
	sh.abigen("--abi=packet.abi","--pkg=packet","--out=../packet/packet.go")

	# 编译teleport
	print("开始编译teleport……")
	sh.cd("../../xibc-contracts/teleport/")
	sh.yarn()
	sh.yarn("compile")

	# 写文件
	print("开始写入abi文件……")
	# Transfer.sol
	with open("artifacts/contracts/apps/transfer/Transfer.sol/Transfer.json", "r") as f:
		data = json.load(f)
	with open("../../contracts/abis/tpTransfer.abi","w",encoding="utf-8") as f:
		json.dump(data["abi"], f, indent=4, ensure_ascii=False)

	# abigen
	print("开始生产go文件……")
	sh.cd("../../contracts/abis")
	sh.abigen("--abi=tpTransfer.abi","--pkg=tpTransfer","--out=../tpTransfer/transfer.go")

	# 删除
	sh.cd("../../")
	sh.rm("-rf","xibc-contracts")

# 获取 address
def getAddress():
	# 待获取数据的字典
	kMap = {
		"export CHAIN_NAME":"chain_name",
		"export ETH_CHAIN_ID":"chain_id",
		"export ETH_CHAIN_URL":"chain_url",
		"export GNOSIS_SAFE_ADDRESS":"gnosis_safe",
		"export CLIENT_MANAGER_ADDRESS":"client_manager",
		"export PACKET_ADDRESS":"packet",
		"export TRANSFER_ADDRESS":"transfer",
		"export MULTICALl_ADDRESS":"multiCall",
		"export PROXY_ADDRESS":"proxy",

		"export ARBITRUM_USDT":"usdt",
		"export ARBITRUM_ETH":"eth",
		"export ARBITRUM_QATELE":"tele",
		"export ARBITRUM_TELE":"tele",

		"export RINKEBY_USDT":"usdt",
		"export RINKEBY_ETH":"eth",
		"export RINKEBY_QATELE":"tele",
		"export RINKEBY_TELE":"tele",

		"export QA_USDT":"usdt",
		"export QA_ETH":"eth",
		"export TELEPORT_USDT":"usdt",
		"export TELEPORT_ETH":"eth",

		"export BSC_USDT":"usdt",
		"export BSC_ETH":"eth",
		"export BSC_QATELE":"tele",
		"export BSC_TELE":"tele",
	}
	explorerMap = {
		"rinkeby":"https://rinkeby.etherscan.io",
		"bsctest":"https://testnet.bscscan.com",
		"qa":"https://blockscout.qa.davionlabs.com",
		"arbitrum":"https://rinkeby-explorer.arbitrum.io"
	}
	# 先删除
	sh.rm("-rf","datas")
	# 再创建
	sh.mkdir("datas")
	sh.mkdir("datas/qanet")
	sh.mkdir("datas/testnet")

	# 下载
	sh.git("clone", "git@github.com:teleport-network/Contracts.git", "cs")

	# 遍历文件，获取数据
	sh.cd("cs")
	
	sh.cd("Teleport_QA")
	chainMap = {}
	chainMap = getChainMessage(kMap, explorerMap)
	chainMap["teleport"]["chain_id"] = "7001"
	chainMap["teleport"]["chain_url"] = "https://teleport-localvalidator.qa.davionlabs.com/"
	
	# 写文件
	with open("../../datas/qanet/chains.json","w",encoding="utf-8") as f:
		json.dump(chainMap, f, indent=4, ensure_ascii=False)	

	sh.cd("../Teleport_Testnet")
	chainMap = {}
	chainMap = getChainMessage(kMap, explorerMap)
	chainMap["teleport"]["chain_id"] = "8001"
	chainMap["teleport"]["chain_url"] = "https://dataseed.testnet.teleport.network"

	# 写文件
	with open("../../datas/testnet/chains.json","w",encoding="utf-8") as f:
		json.dump(chainMap, f, indent=4, ensure_ascii=False)

	# 删除
	sh.cd("../../")
	sh.rm("-rf", "cs")

def getChainMessage(kMap, explorerMap):
	chainMap = {}

	file = "contracts/Arbitrum.md"
	if not os.path.exists(file):
		file = "Contract/arbitrum.md"
	with open(file, "r") as f:
		chain = {}
		for line in f.readlines():
			if "=" in line and line.split("=")[0] in kMap.keys():
				k = kMap[line.split("=")[0]]
				chain[k] = line.split("=")[1].replace("\n","")
		chain["explorer"] = explorerMap[chain["chain_name"]]
		chain["eth"] = "0x0000000000000000000000000000000000000000"
		chainMap[chain["chain_name"]] = chain

	file = "contracts/BSC.md"
	if not os.path.exists(file):
		file = "Contract/bsc.md"
	with open(file, "r") as f:
		chain = {}
		for line in f.readlines():
			if "=" in line and line.split("=")[0] in kMap.keys():
				k = kMap[line.split("=")[0]]
				chain[k] = line.split("=")[1].replace("\n","")
		chain["explorer"] = explorerMap[chain["chain_name"]]
		chain["eth"] = "0xd66c6b4f0be8ce5b39d52e0fd1344c389929b378"
		chainMap[chain["chain_name"]] = chain

	file = "contracts/QA.md"
	if not os.path.exists(file):
		file = "Contract/teleport.md"
	with open(file, "r") as f:
		chain = {}
		for line in f.readlines():
			if "=" in line and line.split("=")[0] in kMap.keys():
				k = kMap[line.split("=")[0]]
				chain[k] = line.split("=")[1].replace("\n","")
		chain["chain_name"] = "qa"
		chain["explorer"] = explorerMap[chain["chain_name"]]
		chain["chain_name"] = "teleport"
		chain["tele"] = "0x0000000000000000000000000000000000000000"
		chainMap[chain["chain_name"]] = chain

	file = "contracts/Rinkeby.md"
	if not os.path.exists(file):
		file = "Contract/rinkeby.md"
	with open(file, "r") as f:
		chain = {}
		for line in f.readlines():
			if "=" in line and line.split("=")[0] in kMap.keys():
				k = kMap[line.split("=")[0]]
				chain[k] = line.split("=")[1].replace("\n","")
		chain["explorer"] = explorerMap[chain["chain_name"]]
		chain["eth"] = "0x0000000000000000000000000000000000000000"
		chainMap[chain["chain_name"]] = chain

	return chainMap

if __name__ == "__main__":
	# getAbi()
	getAddress()
