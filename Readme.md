## commands
### 遍历区块信息，绘制交易数的折线图 e网路 默人qa
- `python blockTxns.py -bs 1000552 -be 1000581 -g 100 -xs 30 -e e`
- `python blockTxnsTime.py -bs 1000552 -be 1000581 -g 100 -xs 30`
- `python blockTime.py -bs 1000552 -be 1000581 -g 100 -xs 30 -ys 120 -e e`
### 遍历区块信息，绘制成功交易的耗时图
- `python analyseHistory.py -s 0x387F83710c848Ead3047B2cDF85Ad87127309A49 -ps 150 -e t`
### 遍历history信息，输出表格
- `python HistoryStatus.py -s 0x387F83710c848Ead3047B2cDF85Ad87127309A49 -e t -ps 24`
### 计算指定区块之间的qps
- python blockTxnsQps.py -bs 304537 -be 304630
### 根据区块间隔，按照指定间隔时间分割绘制图，存储在img文件夹，没有新增文件夹，默认间隔10分钟
- python blockGroupingTime.py -bs 329647 -be 329667 -xs 1 -ts 10
