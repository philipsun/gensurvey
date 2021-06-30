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
from sxpTestWordDistQuerySurvey import *
import sxpReadFileMan
import itertools

# -----closeness ranking sent study
def test1():
    testname = 'wordquery_allv6ks_dual_sentrank'  # the best one for all 20201111 study
    topkmethod = 'LR'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test2():
    testname = 'tfidf_BM25'
    topkmethod = 'LR'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test3():
    testname = 'dtfipf_stopword'
    topkmethod = 'LR'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test4():
    testname = 'wordquery_allv4'
    topkmethod = 'LR'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict

def test5():
    testname = 'wordquery_allv6ks_dual_sentrank'  # the best one for all 20201111 study
    topkmethod = 'maxseg'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test6():
    testname = 'tfidf_BM25'  # the best one for all 20201111 study
    topkmethod = 'maxseg'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict

def test7():
    testname = 'dtfipf_stopword'  # the best one for all 20201111 study
    topkmethod = 'maxseg'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test8():
    testname = 'wordquery_allv4'  # the best one for all 20201111 study
    topkmethod = 'maxseg'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test9():
    testname = 'wordquery_allv6ks_dual_sentrank'  # the best one for all 20201111 study
    topkmethod = 'TP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test10():
    testname = 'tfidf_BM25'
    topkmethod = 'TP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict

def test11():
    testname = 'dtfipf_stopword'
    topkmethod = 'TP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test12():
    testname = 'wordquery_allv4'  # the best one for all 20201111 study
    topkmethod = 'TP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test13():
    testname = 'wordquery_allv6ks_dual_sentrank'  # the best one for all 20201111 study
    topkmethod = 'LRTP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test14():
    testname = 'tfidf_BM25'  # the best one for all 20201111 study
    topkmethod = 'LRTP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test15():
    testname = 'dtfipf_stopword'  # the best one for all 20201111 study
    topkmethod = 'LRTP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def test16():
    testname = 'wordquery_allv4'  # the best one for all 20201111 study
    topkmethod = 'LRTP'
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict
def runtest(testname, topkmethod):
    scoredict = BuilAllTopk(testname, topkmethod, compress_factor=0.01)
    scoredict['method']= testname + '_'+ topkmethod
    return scoredict

def testlr():
    print(test13())
    print(test14())
def testcomb():
    testnamelist = ['wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_stopword',
                'worddistv4',
                'worddistv6ks_dual_sentscore_prefix',
                'worddistv6ks_directed_dual_sentscore',
                    ]
    testnamelist = [
        'dtfipf_stopword',
        'tfidf_BM25'
    ]
    topknamelist = ['orig',
                    'LR',
                'TP',
                'maxseg',
                'avg_max_gap',
                'LRTP']
    # topknamelist = ['avg_max_gap'
    #                ]
   # for each in zip(testname,topkname):
    a = sxpReadFileMan.LoadObject(r'.\test\predicttopk.obj')
    if a is None:
        a = []
    #a = []
    for topkmethod,testname  in itertools.product(topknamelist,testnamelist):
        print(testname, topkmethod)
    for topkmethod,testname  in itertools.product(topknamelist,testnamelist):
        print(testname, topkmethod)
        score = runtest(testname, topkmethod)
        a.append(score)

    sxpReadFileMan.SaveObject(a, r'.\test\predicttopk.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\predicttopk.csv')
def testtopk():
    testnamelist =  ['wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_stopword',
                'wordquery_allv4',
                'worddistv6ks_dual_sentscore_prefix',
                'worddistv6ks_directed_dual_sentscore',
                    ]
    topknamelist = ['orig',
                'TOP1',
                'TOP2',
                'TOP5',
                'TOP10',
                'TOP15',
                ]
    # topkname = [
    #             'LRTP']
   # for each in zip(testname,topkname):
    # for each in zip(testname,topkname):
    a = sxpReadFileMan.LoadObject(r'.\test\predicttopk1_5.obj')
    for topkmethod,testname  in itertools.product(topknamelist,testnamelist):
        print(testname, topkmethod)

    for topkmethod, testname in itertools.product(topknamelist, testnamelist):
        print(testname, topkmethod)
        score = runtest(testname, topkmethod)
        a.append(score)

    sxpReadFileMan.SaveObject(a, r'.\test\predicttopk1_5.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\predicttopk1_5.csv')
def maintest():
    a = []
    a.append(test1())
    a .append(test2())
    a.append(test3())
    a .append(test4())
    a.append(test5())
    a .append(test6())
    a.append(test7())
    a.append(test8())
    a.append(test9())
    a.append(test10())
    a.append(test11())
    a.append(test12())
    sxpReadFileMan.SaveObject(a, r'.\test\predicttopk.obj')

    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\predicttopk.csv')
def detecttopk(rankmethod):
    pt = '([A-Za-z]+)(\d+)$'
    m = re.match(pt,rankmethod)
    if m:
        print(m.groups()[0])
        return m.groups()[0],m.groups()[1]
    else:
        return None
def main():
   # wdtest()
    print(detecttopk('top10'))
    cmd = ['testcomb']
    if 'run' in cmd:
        maintest()
    if 'topk' in cmd:
        testtopk()
    if 'testLR' in cmd:
        testlr()
    if 'testcomb'in cmd:
        testcomb()

    if 'showdata' in cmd:
        a = sxpReadFileMan.LoadObject(r'.\test\predicttopk.obj')
        df = pd.DataFrame(a)
        print(df)
        df.to_csv(r'.\test\predicttopk.csv')
    #sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()
