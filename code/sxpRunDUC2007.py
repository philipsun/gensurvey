#coding=utf-8
#-------------------------------------------------------------------------------
# Name:        ****
# Purpose:
#
# Author:      Sun Xiaoping
#
# Created:     03/10/2020
# Copyright:   (c) sunxp 971994252@qq.com 2020
# Licence:     <mit licence>
#-------------------------------------------------------------------------------
import sxpDUC2007main
import sxpTestDUC2007MultSum
import sxpReadFileMan
def MakeRankDUC2007():
    testname = 'MakeSumByModel'
    summethod_list = [
         # 'bymodel0',
         # 'head1',
         # 'head2',
         # 'onefromsrc',
         # 'diffsimgraph',
         # 'diffgraph',
         # 'simgraph',
         # 'simdiffskip',
         # 'wordclosetopic',
         # 'wordclosetopicone',
         # 'wordclosesim',
         # 'duc2007s15',
         'worddirectedclose',
        'worddirectedcloseone',
    ]
    for summethod in summethod_list:
        sxpDUC2007main.main(testname,summethod)
def RunRouge():
    test =[
        # 'wordclosetopicone',
        # 'wordclosesim',
        # 'tfidf',
        # 'dtfipf',
        # 'BM25Okapi',
        # 'tfidfone',
        # 'dtfipfone',
        # 'BM25Okapione',
        'worddirectedclose',
        'worddirectedcloseone',
    ]
    sxpTestDUC2007MultSum.TestDemo(test)
def main():
  #  cmd = ['MakeRankDUC2007','RunRouge','close']
  #  cmd = ['MakeRankDUC2007', 'RunRouge']
    cmd = ['RunRouge']
    if 'MakeRankDUC2007' in cmd:
        MakeRankDUC2007()
    if 'RunRouge' in cmd:
        RunRouge()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()


