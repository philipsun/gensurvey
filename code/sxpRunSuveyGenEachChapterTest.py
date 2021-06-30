# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/2/21 15:51
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
import sxpReadFileMan
import itertools
import pandas as pd
import sxpTestSurveyAsOne
import sxpTestSurveyAllChapter
import sxpSurveyData
from sxpSurveyData import sxpNode
def makeidname(testnamelist, topknamelist,otherpairs):
    testpair = []
    idname = {}
    i = 0
    testallcase = []
    testallcasename = []
    testcasedict = {}
    for testcase, topkmethodcase  in itertools.product(testnamelist, topknamelist):
        print(testcase, topkmethodcase)
        test_name = testcase + '_' + topkmethodcase
        ids = "{:0>2d}".format(i)
        print(test_name, ids)
        idname[test_name] = ids
        testpair.append([testcase,topkmethodcase])
        # testidname = eachtest[0]
        # testcasename = eachtest[1]
        # topkname = eachtest[2]
        testallcase.append(test_name)
        testcasedict[test_name]=[testcase,topkmethodcase,ids]
        i += 1
    for testcase, topkmethodcase in otherpairs:
        print(testcase, topkmethodcase)
        if len(topkmethodcase)>0:
            test_name = testcase + '_' + topkmethodcase
        else:
            test_name = testcase
        ids = "{:0>2d}".format(i)
        print(test_name, ids)
        idname[test_name] = ids
        testpair.append([testcase,topkmethodcase])
        # testidname = eachtest[0]
        # testcasename = eachtest[1]
        # topkname = eachtest[2]
        testallcase.append(test_name)
        testcasedict[test_name]=[testcase,topkmethodcase,ids]
        i += 1

    return idname,testpair,testallcase,testcasedict


def BuildSurvey(topkmethodcase,testcase):
    #  BuildSurveyChapterByRankResult(eachtest['survgenmethod'],eachtest['testname'])
    print('--build for-------', topkmethodcase,testcase)
    if testcase == 'test_origin':
       sxpSurveyData.MakeSurveyByOriginResult(topkmethodcase, testcase)
    else:
       sxpSurveyData.MakeSurveyByRankTopkResult(topkmethodcase, testcase)
    sxpSurveyData.TraverseMakeSurvey(topkmethodcase, testcase)
def buildsurvey(idname,testpair):
    for  testcase,topkmethodcase in testpair:
        print(testcase,topkmethodcase)
        BuildSurvey(topkmethodcase,testcase)

def runtest(idname,testallcase,testcasedict):
    cmd = ['rank', 'score']
    sxpTestSurveyAllChapter.RunGenRouge(idname,testallcase,testcasedict)

def maketestcase():
    testname = ['wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_all_stop']
    testname = ['worddistv6ks_directed_dual_sentscore',
                'worddistv6ks_dual_sentscore_prefix',
                #'worddistv6ks_dual_sentscore',  note that we did not use this test in predict topk test
                'wordquery_allv6ks_dual_sentrank', #instead, we use this testname with LR, TP, MS
                'tfidf_BM25',
                'dtfipf_all_stop',
                ]
    testname = [
                 'worddistv6ks_dual_sentscore_prefix',
                'worddistv6ks_directed_dual_sentscore',
                'wordquery_allv6ks_dual_sentrank',
                'dtfipf_all_stop',
                'tfidf_BM25',
                ]
    topkname = ['LR',
                'TP',
                'maxseg',
                'orig'
                ]
    # topkname= [
    #     'topk300',
    #     'topk500',
    #     'topk800',
    #     'topk1000',
    # ]
    otherpairs = [
        ['test_origin','origin_abs']
    ]
   # otherpairs = []
    idname, testpair,testallcase,testcasedict = makeidname(testname, topkname,otherpairs)
    return idname,testpair,testallcase,testcasedict
def maketopktestcase():
    testname = ['wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_all_stop']
    testname = ['worddistv6ks_directed_dual_sentscore',
                'worddistv6ks_dual_sentscore_prefix',
                #'worddistv6ks_dual_sentscore',  note that we did not use this test in predict topk test
                'wordquery_allv6ks_dual_sentrank', #instead, we use this testname with LR, TP, MS
                'tfidf_BM25',
                'dtfipf_all_stop',
                ]
    testname = [
                 'worddistv6ks_dual_sentscore_prefix',
                'worddistv6ks_directed_dual_sentscore',
                'wordquery_allv6ks_dual_sentrank',
                'dtfipf_all_stop',
                'tfidf_BM25',
                ]
    # topkname = ['LR',
    #             'TP',
    #             'maxseg',
    #             'orig'
    #             ]
    topkname= [
        'topk300',
        'topk500',
        'topk800',
        'topk1000',
    ]
#    otherpairs = [
#        ['test_origin','origin_abs']
#    ]
    otherpairs = []
    idname, testpair,testallcase,testcasedict = makeidname(testname, topkname,otherpairs)
    return idname,testpair,testallcase,testcasedict
def testcomblrbuild():
    idname,testpair,testallcase,testcasedict =maketestcase()
    buildsurvey(idname, testpair)
def testcomtopkbuild():
    idname,testpair,testallcase,testcasedict =maketopktestcase()
    buildsurvey(idname, testpair)

def testcomblrsurvey():
    idname, testpair,testallcase,testcasedict  = maketestcase()
    print(idname)
    print('-----runing test')
    print(testcasedict)
    runtest(idname,testallcase,testcasedict)
def testcombtopksurvey():
    idname, testpair,testallcase,testcasedict  = maketopktestcase()
    print(idname)
    print('-----runing maketopktestcase test')
    print(testcasedict)
    runtest(idname,testallcase,testcasedict)

def testshowsurv():
    testname = ['wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_all_stop']
    topkname = ['LR',
                'TP',
                'maxseg',
                ]
    otherpairs = [
        ['test_abs','origin_abs']
    ]
    idname, testpair, testallcase, testcasedict = makeidname(testname, topkname,otherpairs)

    print(idname)
    testcasename = 'wordquery_allv6ks_dual_sentrank'
    topkname = 'LR'
    chpater  = '4'
    sxpSurveyData.ShowTopkChid(testcasename, topkname, chpater)
    topkname = 'TP'
    chpater = '4'
    sxpSurveyData.ShowTopkChid(testcasename, topkname, chpater)
    #sxpSurveyData.TraverseShowSurvey(topkname,testcasename)
def main():

    #cmd = ['testcombasonebuild','testcombasonesurvey']
    #  cmd = ['testcombasonebuild', 'testshow']
    #cmd =['testcombasonesurvey','close']
    #cmd = ['testcomblrbuild','testcomblrsurvey'] # in general, you don;t have to run build because we have run buid in
    cmd = ['topkbuild', 'topksurvey']  # in general, you don;t have to run build because we have run buid in
    # sxpRunSurveyGenTest.py,
    # an important difference in this chapeter-chapter evaluation
    # cmd = ['testcombasonesurvey']
    if 'testcomblrbuild' in cmd:
        testcomblrbuild()
    if 'testcomblrsurvey' in cmd:
        testcomblrsurvey()
    if 'topkbuild' in cmd:
        testcomtopkbuild()
    if 'topksurvey' in cmd:
        testcombtopksurvey()
    if 'testshow' in cmd:
        testshowsurv()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()
def main():
    pass;


if __name__ == '__main__':
    main()
