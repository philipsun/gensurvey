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
import pandas
import sxpMultiPaperData

#sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='tfidf')
#sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='tfief')
#sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='dtfipf')
#sxpMultiPaperData.BuildBM25('BM25Okapi')
#sxpMultiPaperData.BuildBM25('BM25L')
#sxpMultiPaperData.BuildBM25('BM25Plus')
# sxpMultiPaperData.BuildPaperSentenceBM25(bmmodel='BM25Okapi')
# sxpMultiPaperData.BuildPaperSentenceBM25(bmmodel='BM25L')
# sxpMultiPaperData.BuildPaperSentenceBM25(bmmodel='BM25Plus')
def wdtest():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdoc_wd.obj')
    s = RunWordDist()
    a.append(s)
    s = RunWordDistV2()
    a.append(s)
    s = RunWordDistV4()
    a.append(s)
    s = RunWordDistV6()
    a.append(s)
    s = RunWordDistV66KS()
    a.append(s)
    s = RunWordDistV6Top2()
    a.append(s)
    s = RunWordDistBV7()
    a.append(s)
    s = RunWordDistStop()
    a.append(s)
    s = RunPrefixWordDist()
    a.append(s)
    s = RunPrefixWordDistStop()
    a.append(s)

    sxpReadFileMan.SaveObject(a,r'.\test\rankdoc_wd.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdoc_wd.csv')
def Build(cmd= 'BM25'):
    if cmd == 'BM25':
        sxpMultiPaperData.BuildBM25('BM25Okapi')
        sxpMultiPaperData.BuildBM25('BM25L')
        sxpMultiPaperData.BuildBM25('BM25Plus')
        sxpMultiPaperData.BuildPaperSentenceBM25('BM25Okapi')
        sxpMultiPaperData.BuildPaperSentenceBM25('BM25L')
        sxpMultiPaperData.BuildPaperSentenceBM25('BM25Plus')
    if cmd =='BuildGlobalTFIDF':
        sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='tfidf')
        sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='tfief')
        sxpMultiPaperData.BuildGlobalTFIDF(tfidfmode='dtfipf')
def moretest():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = RunWordDistV6KS_DualSentRank()
    a.append(s)  # best-20200205

    s = RunWordDistV6KS_DualSentRankNoExclusion()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankMeanClose()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankV1()
    a.append(s)

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
    #sxpReadFileMan.shutdown()
def moretest1():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = RunWordDistV6KS_DualSentRankNoExclusion()
    a.append(s)  # best-20200205

    s = RunWordDistV6KS_DualSentRankPrefixNoDens()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankPrefixNoEven()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankV1()
    a.append(s)

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
    #sxpReadFileMan.shutdown()
def more2():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = RunWordDistV6KS_DualSentRankNoDensReci()
    a.append(s)  # best-20200205
    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
def evenclose():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
   # s = RunWordDistV6KS_DualSentRankNoEven()
   # s = dual_v6_exclusion_meannormclose_v2_reci()
    #  s = RunWordDistV6KS_DualSentRank()
    # s = dual_v6_exclusion_meannormclose_v2_covr()
    # a.append(s)  # best-20200205
    #
    # s = dual_v6_exclusion_meannormclose_v2_reci()
    # a.append(s)  # best-20200205
    #
    # s = dual_v6_exclusion_meannormclose_v2_covr_nodense()
    # a.append(s)  # best-20200205
    #
    # s = dual_v6_exclusion_meannormclose_v2_reci_nodense()
    # a.append(s)  # best-20200205
    #
    # s = dual_v6_exclusion_meannormclose_v2_covr_onlyclose()
    # a.append(s)  # best-20200205
    #
    # s = dual_v6_exclusion_meannormclose_v2_reci_onlyclose()
    # a.append(s)  # best-20200205

    s = dual_v6_exclusion_meannormclose_v2_covr_onlyself()
    a.append(s)  # best-20200205

    s = dual_v6_exclusion_meannormclose_v2_reci_onlyself()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')

    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')

def more3():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = RunWordDistV6KS_DualSentRankDCD()
    a.append(s)  # best-20200205

    s = RunWordDistV6KS_DualSentRankFCD()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
def morev2():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = dual_v6_exclusion_meannormclose_v2_reci()
    #s = RunWordDistV6KS_DualSentRankNoDensReci()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a, r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')

def more4():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = Runwordquery_allv4()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
def moredtfipf():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []
    s = RunDTFIPFStop()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')
def revisitbm25dtfipf():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdocmore.obj')
    #  a = []

    s = RUNBM25()
    a.append(s)

    s = RunDTFIPFStop()
    a.append(s)  # best-20200205

    sxpReadFileMan.SaveObject(a,r'.\test\rankdocmore.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdocmore.csv')

def maintest():
    a = sxpReadFileMan.LoadObject(r'.\test\rankdoc.obj')
    #a = []

    s = RUNBM25()
    a.append(s)


    s = RUNBM25L()
    a.append(s)

    s = RUNBM25Plus()
    a.append(s)

    s = RunTFIDF()
    a.append(s)
    s = RunTFIDFStop()
    a.append(s)


    s = RunTFIEFStop()
    a.append(s)

    s = RunDTFIPFStop()
    a.append(s)

    s = RunWordDistV6KS_DualSentRank()
    a.append(s) #best-20200205

    s = RunWordDistV6KS_DualSentRankNoExclusion()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankMeanClose()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankPrefix()
    a.append(s) #best-20200205

    s = RunWordDistV6KS_DualSentRankPrefixNoEven()
    a.append(s) #best-20200205

    s = RunWordDistV6KS_DualSentRankPrefixNoDens()
    a.append(s) #best-20200205
    s = RunWordDistV6KS_DualSentRankDirected()
    a.append(s)

    s = RunWordDistV6KS_DualSentRankBackDirected()
    a.append(s) #best-20200205

    s = RunDensSpanDenseEven()
    a.append(s)

    s = RunDensSpanCover()
    a.append(s)
    s = RunDensSpanDenscover()
    a.append(s)
    s = RunDensSpanEven()
    a.append(s)

    sxpReadFileMan.SaveObject(a,r'.\test\rankdoc.obj')
    df = pd.DataFrame(a)
    print(df)
    df.to_csv(r'.\test\rankdoc.csv')
    #sxpReadFileMan.shutdown()
def main():
   # wdtest()
   #  RunWordDistV4()
    #cmd = ['Build','maintest']
    #cmd = ['wdtest','maintest', 'moredist']


    #cmd = ['revisitbm25dtfipf']
    cmd = ['evenclose']
    if 'Build' in cmd:
        Build('BM25')
        Build('BuildGlobalTFIDF','close')
    if 'wdtest' in cmd:
        wdtest()
    if 'maintest' in cmd:
        maintest()
    if 'moredist' in cmd:
        moretest1()
    if 'more2' in cmd:
        more2()
    if 'more3' in cmd:
        more3()
    if 'more4' in cmd:
        more4()
    if 'morev2' in cmd:
        morev2()
    if 'moredtfipf' in cmd:
        moredtfipf()
    if 'revisitbm25dtfipf' in cmd:
        revisitbm25dtfipf()
    if 'evenclose' in cmd:
        evenclose()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()
