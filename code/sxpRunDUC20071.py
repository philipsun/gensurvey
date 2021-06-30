# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/2/26 17:38
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
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

import sxpDUC2007main
import sxpTestDUC2007MultSum
import sxpReadFileMan
def MakeRankDUC2007():
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
        'tfidf',
        'dtfipf',
        'BM25Okapi',
    ]

    for summethod in summethod_list:
        sxpDUC2007main.main(testname,summethod)
def Prepare():
    cmdlist = ['sgml', 'makemodel', 'PrepareTargetTopicSourceFile'
        , 'loadalltopicsrc', 'MakeSumByModel']
    cmdlist = ['MakeSumByModel']
    summethod_list = [
        # 'wordclosetopic',
        # 'wordclosetopicone',
        # # 'wordclosesim',
        # 'tfidf',
        # 'dtfipf',
        # 'BM25Okapi',
        # 'tfidfone',
        # 'dtfipfone',
        # 'BM25Okapione',
        'worddirectedclose',
        'worddirectedcloseone',
    ]
    sxpDUC2007main.main(cmdlist, summethod_list)
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
         'tfidfone',
         'dtfipfone',
         'BM25Okapione',
    ]
    model_test = [
         'wordclosetopic',
         'wordclosetopicone',
         'wordclosesim',
         'tfidf',
         'dtfipf',
         'BM25Okapi',
         'tfidfone',
         'dtfipfone',
         'BM25Okapione',
    ]
    model_test = [
         'wordclosetopic',
         'wordclosetopicone',
        # 'wordclosesim',
         'tfidf',
         'dtfipf',
         'BM25Okapi',
         'tfidfone',
         'dtfipfone',
         'BM25Okapione',
        'worddirectedclose',
        'worddirectedcloseone',
    ]
    cmd = ['rank','score']
    sxpTestDUC2007MultSum.TestDemo(model_test,cmd)
def main():
    runtype = 'rank and rouge'
    if runtype == 'runandclose':
        cmd = ['MakeRankDUC2007','RunRouge','close']
   # cmd = ['MakeRankDUC2007', 'RunRouge']
    if runtype == 'rank and rouge':
        cmd = [ 'MakeRankDUC2007','RunRouge']
    if runtype == 'rouge':
        cmd = [ 'RunRouge']
    usetry = False;
    if usetry:
        try:
            if 'MakeRankDUC2007' in cmd:
                #MakeRankDUC2007()
                Prepare()
            if 'RunRouge' in cmd:
                RunRouge()
            if 'close' in cmd:
                sxpReadFileMan.shutdown()
        except Exception:
            print(Exception)
            pass
    if 'MakeRankDUC2007' in cmd:
        #MakeRankDUC2007()
        Prepare()
    if 'RunRouge' in cmd:
        RunRouge()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()


