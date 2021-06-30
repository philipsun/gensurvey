# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/2/23 17:37
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
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
import sxpDUC2006main
import sxpTestDUC2006MultSum
import sxpReadFileMan
def MakeRankDUC2006():
    testname = 'MakeSumByModel'
    summethod_list = [
         'bymodel0',
         'head1',
         'head2',
         'onefromsrc',
         'diffsimgraph',
         'diffgraph',
         'simgraph',
         'simdiffskip',
         'wordclosetopic',
         'wordclosetopicone',
         'wordclosesim',

    ]
    summethod_list = [
          'wordclosetopic',
         'wordclosetopicone',
         'wordclosesim',
    ]
    summethod_list = [
        'wordclosetopic',
        'tfidf',
        'dtfipf',
        'BM25Okapi',
        'wordclosetopicone',
        'tfidfone',
        'dtfipfone',
        'BM25Okapione',
    ]

    for summethod in summethod_list:
        sxpDUC2006main.main(testname,summethod)
def Prepare():
    cmdlist = ['sgml', 'makemodel', 'PrepareTargetTopicSourceFile'
        , 'loadalltopicsrc', 'MakeSumByModel']
    cmdlist = ['MakeSumByModel']
    summethod_list = [
        #'wordclosetopic',
        # # 'wordclosetopicone',
        # # 'wordclosesim',
        # 'tfidf',
        # 'dtfipf',
        # 'BM25Okapi',
        # 'wordclosetopicone',
        # 'tfidfone',
        # 'dtfipfone',
        # 'BM25Okapione',
        #'wordclosetopiconev1',
        #'even',
        'worddirectedclose'
    ]
    sxpDUC2006main.main(cmdlist, summethod_list)
def RunRouge():
    model_test = [
         'bymodel0',
         'head1',
         'head2',
         'onefromsrc',
         'diffsimgraph',
     #    'diffgraph',
         'simgraph',
         'simdiffskip',
         'wordclosetopic',
         'wordclosetopicone',
         'wordclosesim',
    ]
    model_test = [
        'tfidf',
        'dtfipf',
        'BM25Okapi',
        'wordclosetopicone',
        'tfidfone',
        'dtfipfone',
        'BM25Okapione',
        'wordclosetopiconev1',
        'even',
        'worddirectedclose'
    ]
    cmd = ['rank','score']
    sxpTestDUC2006MultSum.TestDemo(model_test,cmd)
def main():
    runtype = 'rank and rouge'
    if runtype == 'runandclose':
        cmd = ['MakeRankDUC2006', 'RunRouge', 'close']
    # cmd = ['MakeRankDUC2007', 'RunRouge']
    if runtype == 'rank and rouge':
        cmd = ['MakeRankDUC2006', 'RunRouge']
    if runtype == 'rouge':
        cmd = ['RunRouge']
    usetry = False;
    if usetry:
        try:
            if 'MakeRankDUC2006' in cmd:
                #MakeRankDUC2006()
                Prepare()
            if 'RunRouge' in cmd:
                RunRouge()
            if 'close' in cmd:
                sxpReadFileMan.shutdown()
        except Exception:
            print(Exception)
            pass
    if 'MakeRankDUC2006' in cmd:
        #MakeRankDUC2006()
        Prepare()
    if 'RunRouge' in cmd:
        RunRouge()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()


