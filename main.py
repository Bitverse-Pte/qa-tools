from analyse_block.q_block import QBlock
from utils.File_Helper import FHelper


fHelp = FHelper("./logs/25-16-20.log")
fs = fHelp.read_lins()
res = fHelp.find_all(",tx sent: ")
hs = [r.split(",tx sent: ")[1].split(",")[0] for r in res]

qBlock = QBlock()
res = qBlock.get_none_blockeNum_hashs(hs, 304500, 304650)
# res = qBlock.get_none_blockeNum_hashs(hs, 304850, 305000)

fHelp.write_csv("in_block.csv",["txn","blockNum"],res[0])

print(len(res[1]))
res_tmp = [[r] for r in res[1]]
fHelp.write_csv("non_block.csv",["txn"],res_tmp)
