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
import sxpReadFileMan
import itertools
import pandas as pd
import sxpTestSurveyAsOne
import sxpSurveyData
import sxpRunDocRank
import sxpRunTopkPredict
import re
import os
from sxpSurveyData import sxpNode
def makeidname(testnamelist, topknamelist,otherpairs=[]):
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

    return idname,testpair,testallcase,testcasedict


def BuildSurvey(topkmethodcase,testcase):
    #  BuildSurveyChapterByRankResult(eachtest['survgenmethod'],eachtest['testname'])
    print('--build for-------', topkmethodcase,testcase)
    if testcase == 'test_origin':#survgenmethod='origin_abs', testname='test_origin'
        #this functio will use origin references' abstraction as the text to compose the survey.
       sxpSurveyData.MakeChapterOriginRefAbs(survgenmethod='origin_abs', testname='test_origin')
        #this funciton is to use the result of the above function to prepare a survey generation dict
       sxpSurveyData.MakeSurveyByOriginResult(topkmethodcase, testcase)
    else:
      sxpSurveyData.MakeSurveyByRankTopkResult(topkmethodcase, testcase)
    sxpSurveyData.TraverseMakeSurvey(topkmethodcase, testcase)
def buildsurveytestset(idname,testpair):
    for  testcase,topkmethodcase in testpair:
        print(testcase,topkmethodcase)
        BuildSurvey(topkmethodcase,testcase)

def RunTest(idname,testallcase,testcasedict):
    cmd = ['rank', 'score', ]
    sxpTestSurveyAsOne.RunGenRouge(idname,testallcase,testcasedict,cmd)

def maketestcase():
    # testname = ['worddistv6ks_dual_sentscore_prefix',
    #             'worddistv6ks_dual_sentscore',  #'wordquery_allv6ks_dual_sentrank',
    #             'tfidf_BM25',
    #             'dtfipf_all_stop',
    #             ]
    # testname = ['worddistv6ks_directed_dual_sentscore',
    #             'worddistv6ks_dual_sentscore_prefix',
    #             #'worddistv6ks_dual_sentscore',  note that we did not use this test in predict topk test
    #             'wordquery_allv6ks_dual_sentrank', #instead, we use this testname with LR, TP, MS
    #             'tfidf_BM25',
    #             'dtfipf_all_stop',
    #             ]
    testname = [
        'dtfipf_all_stop'
    ]
    topkname = ['orig',
                'LR',
                'TP',
                'maxseg',
                ]
    # topkname = [
    #             'LRTP']
    # for each in zip(testname,topkname):
    otherpairs = [
        ['test_origin','origin_abs']
    ]
    idname, testpair,testallcase,testcasedict = makeidname(testname, topkname,otherpairs)
    return idname,testpair,testallcase,testcasedict
def testcombasonebuild():
    idname,testpair,testallcase,testcasedict =maketestcase()
    buildsurveytestset(idname, testpair)
def testcombasonesurvey():
    idname, testpair,testallcase,testcasedict  = maketestcase()
    print(idname)
    print('-----runing test')
    print(testcasedict)
    RunTest(idname,testallcase,testcasedict)
def testshowsurv():
    testname = ['worddistv6ks_dual_sentscore_prefix',
                'worddistv6ks_dual_sentscore',  #'wordquery_allv6ks_dual_sentrank',
                'tfidf_BM25',
                'dtfipf_all_stop',
                ]
    topkname = ['LR',
                'TP',
                'maxseg',
                ]
    otherpairs = [

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
def ParseScore(ftline):
    rs = 0.0

    rn0 = 0
    rn1 = 0
    rn05 = 0
    cs = 0.0

    cn0 = 0
    cn1 = 0
    cn05 = 0
    currentsection = []
    sectionlist = {}
    n = 0
    for t in ftline:
        pt = r".+(0|1|0\.5)\s+(0|1|0\.5)$"

        g = re.match(pt,t.strip())
        if g:
            relscore= g.groups()[0]

          #  print(score, t)
            rns = float(relscore)
            rs += rns
            if rns == 0:
                rn0 += 1
            if rns == 1:
                rn1 +=1
            if rns == 0.5:
                rn05 += 1
            #currentsection.append(rns)

            cohscore = g.groups()[1]

            #  print(score, t)
            cns = float(cohscore)
            cs += cns
            if cns == 0:
                cn0 += 1
            if cns == 1:
                cn1 += 1
            if cns == 0.5:
                cn05 += 1
            currentsection.append([rns,cns])

        else:
           # print(t)
           # print('-----no score')
           titledict = extracttile(t)
           if titledict:
               if currentsection:
                   sectionlist[sectionid]=currentsection
                   currentsection = []
                   sectionid = titledict['chid']
               else:
                   currentsection = []
                   sectionid = titledict['chid']
           pass
        n = n + 1.0
    tresult = {}
    tresult['rs/n']=rs/n
    tresult['n'] = n
    tresult['#of0rel']=rn0
    tresult['#of1rel']=rn1
    tresult['#of0.5rel']=rn05
    tresult['pof0rel']=rn0/n
    tresult['pof1rel'] = rn1 / n
    tresult['pof0.5rel'] = rn05 / n

    tresult['cs/n'] = cs / n
    tresult['#of0coh']=cn0
    tresult['#of1coh']=cn1
    tresult['#of0.5coh']=cn05
    tresult['pof0coh']=cn0/n
    tresult['pof1coh'] = cn1 / n
    tresult['pof0.5coh'] = cn05 / n
    sectionresult = []
    for k,v in sectionlist.items():
        sn = len(v)
        rs = 0.0
        rn = 0.0
        rn0 = 0
        rn1 = 0
        rn05 = 0
        cs = 0.0
        cn = 0.0
        cn0 = 0
        cn1 = 0
        cn05 = 0
        for ns in v:
            rs += ns[0]
            if ns[0] == 0:
                rn0 += 1
            if ns[0] == 1:
                rn1 +=1
            if ns[0] == 0.5:
                rn05 += 1
            cs += ns[1]
            if ns[1] == 0:
                cn0 += 1
            if ns[1] == 1:
                cn1 +=1
            if ns[1] == 0.5:
                cn05 += 1
        result = {}
        result['rs/n']=rs/sn
        result['n'] =sn
        result['#of0rel']=rn0
        result['#of1rel']=rn1
        result['#of0.5rel']=rn05
        result['pof0rel']=rn0/sn
        result['pof1rel'] = rn1 / sn
        result['pof0.5rel'] = rn05 / sn

        result['cs/n']=cs/sn
        result['#of0']=cn0
        result['#of1']=cn1
        result['#of0.5']=cn05
        result['pof0']=cn0/sn
        result['pof1'] = cn1 / sn
        result['pof0.5'] = cn05 / sn
        result['section']=k
        sectionresult.append(result)
    return tresult,sectionresult
def extracttile(txt):
    cht = re.split('\-t', txt)
    title_dict ={}
    if len(cht) >= 2:
        title_dict['chid'] = cht[0]
        title_dict['title'] = cht[1]
    else:
        title_dict = None
    return title_dict
def gettitle(linelist):
    for txt in linelist:
        titledict=extracttile(txt)
        if titledict:
            print(titledict)

def ManualScore():
    fdir = r'E:\pythonworknew\code\textsum\surveygen\experiment\surveygen\manualscorev2'
    f1= fdir + os.path.sep+ r'manualscore_gen_survey_wordquery_allv6ks_dual_sentrank_orig.txt'
    ftline1 = sxpReadFileMan.ReadTxtLines(f1)
    print('manualscore_gen_survey_wordquery_allv6ks_dual_sentrank_orig')
    result={}
    score,sectionlist1=ParseScore(ftline1)
    result['fecd']=score
    fname = fdir + os.path.sep+ 'sectionscorelist_fecd.csv'
    sdffecd = pd.DataFrame(sectionlist1)
    sdffecd.to_csv(fname)


    f2 = fdir + os.path.sep+ 'manualscore_gen_survey_tfidf_BM25_orig.txt'
    ftline2 = sxpReadFileMan.ReadTxtLines(f2)
    print('manualscore_gen_survey_tfidf_BM25_orig')
    score,sectionlist2=ParseScore(ftline2)
    result['bm25']=score
    fname = fdir + os.path.sep+ 'sectionscorelist_bm25.csv'
    sdfbm25 = pd.DataFrame(sectionlist2)
    sdfbm25.to_csv(fname)


    f3 = fdir + os.path.sep+ 'manualscore_gen_survey_dtfipf_all_stop_orig.txt'
    ftline3 = sxpReadFileMan.ReadTxtLines(f3)
    print('manualscore_gen_survey_dtfipf_all_stop_orig')
    score,sectionlist3=ParseScore(ftline3)
    result['dtfipf'] = score
    fname = fdir + os.path.sep+ 'sectionscorelist_dtfipf.csv'
    sdfdtfipf = pd.DataFrame(sectionlist3)
    sdfdtfipf.to_csv(fname)

    df = pd.DataFrame(result)
    fname = fdir + os.path.sep+ 'score.csv'
    df.to_csv(fname)

    df = pd.DataFrame()
    df['Rel_FECD'] = sdffecd[r'rs/n']
    df['Rel_BM25'] = sdfbm25[r'rs/n']
    df['Rel_DTFIPF'] = sdfdtfipf[r'rs/n']
    df['Coh_FECD'] = sdffecd[r'cs/n']
    df['Coh_BM25'] = sdfbm25[r'cs/n']
    df['Coh_DTFIPF'] = sdfdtfipf[r'cs/n']
    fname = fdir + os.path.sep+ 'allsectionratiorscore.csv'
    df.to_csv(fname)

    print(result)
   # gettitle(ftline1)
def main():
    #  cmd = ['testcombasonebuild','testcombasonesurvey','close']

   #  cmd = ['testcombasonebuild']
    # cmd = ['testcombasonebuild', 'testcombasonesurvey']
    cmd = ['ManualScore']
  #  cmd = ['testcombasonebuild', 'testshow']
  #  cmd =['PredictTopk','testcombasonebuild','testcombasonesurvey','close']
  #  cmd = ['testshow']
    if 'RankDocSentMainTest' in cmd:
        sxpRunDocRank.maintest() #note that this is the first experiment to rank doc and sentences
    if 'PredictTopk' in cmd:
        sxpRunTopkPredict.main() #this is th second experiment to predict top-k
    if 'testcombasonebuild' in cmd:
        testcombasonebuild()     #this is to compose survey sentence
    if 'testcombasonesurvey' in cmd:
        testcombasonesurvey()    #this is compose test cases for runing ROUGE
    if 'testshow' in cmd:
        testshowsurv()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
    if 'ManualScore' in cmd:
        ManualScore()
if __name__ == '__main__':
    main()
