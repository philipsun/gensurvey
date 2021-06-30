# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/3/3 16:33
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
import sxpACLSumData
import sxpReadFileMan
import sxpWordDist
import sxpMetricScore
import re
import pandas as pd
import matplotlib as plt
import sxpJudgeCharacter
import sxpTfidfBM25
import time
output_dir = r'./test/acl2014/rank'
sxpReadFileMan.CheckMkEachLevelSub(output_dir)
runmodel = True
def RankACL():
    testname ='acl_rank'
    ranker = 'worddistv6ks_dual_sentscore_prefix'
    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname, ranker=ranker)
    testscore['model'] = 'worddistv6ks_dual_sentscore_prefix'
    return testscore
def RankACLNoPrefix():
    testname ='acl_rank'
    ranker = 'worddistv6ks_dual_sentscore'

    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname, ranker=ranker)
    testscore['model'] = 'worddistv6ks_dual_sentscore'
    return testscore
def RankACLWithPrefix():
    testname ='acl_rank'
    ranker = 'worddistv6ks_dual_sentscore_prefix'

    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname, ranker=ranker)
    testscore['model'] = 'worddistv6ks_dual_sentscore'
    return testscore

def RankACLBM25():
    testname ='acl_rank'
    ranker = 'BM25Okapi'

    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname, ranker=ranker)
    testscore['model'] = 'BM25Okapi'
    return testscore
def RankACLDTFIPF():
    testname ='acl_rank'
    ranker = 'dtfipf_stopword'

    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname,ranker=ranker)
    testscore['model'] = 'dtfipf_stopword'
    return testscore
def Ranktfidf():
    testname ='acl_rank'
    ranker = 'tfidf_stopword'
    if runmodel:
        RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname,ranker=ranker)
    testscore['model'] = 'dtfipf_stopword'
    return testscore

def correctitle(ch):
    g = re.split('thanks',ch)
    return removemark(g[0])
def removemark(ch):
    nch = re.sub(",",' ', ch)
    nch = re.sub("\'", ' ', nch)
    nch = re.sub("\?", ' ', nch)
    nch = re.sub("\:", ' ', nch)
    nch = re.sub("\?", ' ', nch)
    nch = re.sub("’", ' ', nch)
    nch = nch.replace("’",' ')
    return nch

def RunAllCh(testname = 'wordquery_all',ranker='worddistv6ks_dual_sentscore_prefix'):
    #chapter_dict = sxpACLSumData.LoadGraphMatrixSentence()
    # doc_dict['sentence_data_dict'] = sentence_data_dict
    # doc_dict['title'] = fname_dict['title']
    # doc_dict['fid'] = fname_dict['fid']
    # doc_dict['graph_dict'] = graph_dict
    # doc_dict['matrix_dict'] = matrix_dict
    print('-----load all paper -----------')
    graph_fname_list = sxpACLSumData.LoadDocModelSentence(incabs='inc')
    print('-----process their titles-----------')
    chapter_dict = {}
    for doc in graph_fname_list:
        fid = doc['fid']
        a = ''
        for c in doc['title']:
            #if not sxpJudgeCharacter.is_charspace(c):
            if c in ['\'', '’',',', ':', '!', '?', '.', '“','”', '(', ')']:
                continue
            else:
                if c in ['-']:
                    c = ' '
                a = a + c
        title = correctitle(a)
        if title in ['t']:
            continue
        doc['title']=title
        sel_ch = {}
        sel_ch['fid']=fid
        sel_ch['title']=doc['title']
        sel_ch['chname'] = doc['title']
        sel_ch['fulltxt_fid']  = [fid]
        print(fid,title)
        chapter_dict[fid]=sel_ch

    allscore = {}
    allresult = {}
    for ch,sel_ch in chapter_dict.items():
       # testinfo = RunTest(testname,ch,ranker)
      # sel_ch =
        testinfo = RunTest(testname,sel_ch,graph_fname_list,ranker=ranker)
        if testinfo:
            allscore[ch]=testinfo['result']
            allresult[ch]=testinfo
        print(testname,ranker)
    fname = output_dir + '/'+testname +'_'+ranker+'_wd_top_len.result.dict'
    sxpReadFileMan.SaveObject(allresult,fname)
    fname = output_dir + '/' + testname  +'_'+ranker + '_wd_top_len.allscore.dict'
    sxpReadFileMan.SaveObject(allscore, fname)
def LoadCorpuse():
    graph_fname_list = sxpACLSumData.LoadDocModelSentence(incabs='inc')
    corpus = []
    for fname_dict in graph_fname_list:
        fulltxt = " ".join(fname_dict['sentence_textset'])
        corpus.append(fulltxt)
    return corpus
def BuildBM25(bmmodel='BM25Okapi'):
    testname = 'rank_acl'
    all_corpus = LoadCorpuse()
    bm25 = sxpTfidfBM25.BuildBM25(all_corpus, testname, bmmodel=bmmodel, rebuild=False)
    fname =output_dir +'/'+testname +'_'+bmmodel+'.object'
    sxpReadFileMan.SaveObject(bm25,fname)
def BuildTFIDF(tfidfmode='tfidf'):
    testname = 'rank_acl'
    all_corpus = LoadCorpuse()
    tfidf = sxpTfidfBM25.BuildTFIDF(all_corpus,testname,tfidfmode=tfidfmode,rebuild=False)
    fname =output_dir +'/'+testname +'_'+tfidfmode+'.object'
    sxpReadFileMan.SaveObject(tfidf,fname)
def LoadTfidfBM(testname,modename = 'tfidf'):
    fname =output_dir +'/'+testname +'_'+modename+'.object'
    return sxpReadFileMan.LoadObject(fname)
bm25 = LoadTfidfBM('rank_acl','BM25Okapi')
tfidf = LoadTfidfBM('rank_acl','tfidf')
dtfipf = LoadTfidfBM('rank_acl','dtfipf')
def RunTest(test_name,sel_ch,graph_fname_list,ranker='worddist'):
    #graph_fname_list = sxpReferMan.GetAllChapterDict()
   # chname = '2'
    chname = sel_ch['chname']
    ch_title = sel_ch['title']
    fid = sel_ch['fid']
    fulltxt_fid_list = sel_ch['fulltxt_fid']
    if len(fulltxt_fid_list)==0:
        print('no full txt paper')
        return None
    truthid= []
    for fulltext_fid in fulltxt_fid_list:
        truthid.append(fulltext_fid)
    print(chname,ch_title,fulltxt_fid_list)
   # test_name = testname+'_'+fid
    keywords = ch_title.split('\s')
    topk = '1'
    sent_rank_result = None
    if ranker == 'worddist':
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords,prefix=[], fidlist=[],removestop=False,version='v1')
    if ranker == 'worddist_stop':
        version = 'v1'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords,prefix=[], fidlist=[],removestop=True,version=version)
    if ranker == 'worddistv2':
        version = 'v2'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=False,version=version)
    if ranker == 'worddistv4':
        version = 'v4'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=False,version=version)
    if ranker == 'worddistv6':
        version = 'v6'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=False,version=version)
    if ranker == 'worddistv6ks':
        version = 'v6'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=True,version=version)

    if ranker == 'worddistv6ks_dual_sentscore':
        version = 'dual_v6'
        Prefix = []
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDistOnDocList(test_name,
                                                                                keywords,
                                                                                graph_fname_list,
                                                                                output_dir,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version='dual_v6')
    if ranker == 'worddistv6ks_dual_sentscore_prefix':
        version = 'dual_v6'
        Prefix = ['in this|we|our|this']
        # rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
        #                                                                            prefix=Prefix,
        #                                                                            fidlist=[],
        #                                                                            removestop=True,
        #                                                                            version=version)
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDistOnDocList(test_name,
                                                                                keywords,
                                                                                graph_fname_list,
                                                                                output_dir,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version='dual_v6')
    if ranker == 'worddistv6ks_dual_sentscore_prefixnoeven':
        version = 'dual_v6_noeven'
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_dual_sentscore_prefixnodens':
        version = 'dual_v6_nodens'
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)

    if ranker == 'worddistv6ks_directed_dual_sentscore':
        version = 'dual_v6_directed'
       # Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name,
                                                                                   keywords,
                                                                                   prefix=[],
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_backdirected_sentscore_prefix':
        version = 'dual_v6_backdirected'
        Prefix = ['we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name,
                                                                                   keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)

    if ranker == 'worddistv6top2':
        version = 'v6'
        topk = '2'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=False,version=version)
    if ranker == 'worddistbv7':
        version = 'bv7'
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=[], fidlist=[], removestop=False,
                                                          version=version)

    if ranker == 'ourprefix':
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=Prefix, fidlist=[])
    if ranker == 'ourprefix_stop':
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.KeywordRankCloseWordDist(test_name, keywords, prefix=Prefix, fidlist=[],removestop=True)
    if ranker == 'tfidf':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,
                                                                     graph_fname_list,
                                                                     output_dir,
                                                                     tfidfmode='tfidf',
                                                                     tfidfbm = tfidf)
    if ranker == 'tfidf_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name,
                                                                     keywords,
                                                                     graph_fname_list,
                                                                     output_dir,
                                                                     removestop=True,
                                                                     tfidfmode='tfidf',
                                                                     tfidfbm = tfidf)

    if ranker == 'dtfipf_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,graph_fname_list,
                                                                     output_dir,
                                                                     removestop=True,
                                                                     tfidfmode='dtfipf',
                                                                     tfidfbm = dtfipf)
    if ranker == 'tfief_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,
                                                                     graph_fname_list,
                                                                     output_dir,
                                                                     removestop=True,
                                                                     tfidfmode='tfief',
                                                                     tfidfbm = None)

    if ranker == 'worddist_dens':
        version = 'dens'
        rankresult,sent_rank_result = sxpWordDist.densquery(test_name,keywords,removestop = True, version = version)
    if ranker == 'worddist_denscover':
        version = 'denscover'
        rankresult,sent_rank_result = sxpWordDist.densquery(test_name,keywords,removestop = True, version = version)
    if ranker == 'worddist_cover':
        version = 'cover'
        rankresult,sent_rank_result = sxpWordDist.densquery(test_name,keywords,removestop = True, version = version)
    if ranker == 'worddist_denseeven':
        version = 'denseven'
        rankresult,sent_rank_result = sxpWordDist.densquery(test_name,keywords,removestop = True, version = version)
    if ranker == 'worddist_even':
        version = 'even'
        rankresult,sent_rank_result = sxpWordDist.densquery(test_name,keywords,removestop = True, version = version)

    if ranker == 'BM25Okapi':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,
                                                                     graph_fname_list,
                                                                     output_dir,
                                                                     removestop=True,
                                                                     tfidfmode='BM25Okapi',
                                                                     tfidfbm = bm25)
    if ranker == 'BM25L':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,graph_fname_list, output_dir,removestop=True,
                                                              tfidfmode='BM25L')
    if ranker == 'BM25Plus':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquerydoclist(test_name, keywords,graph_fname_list, output_dir,removestop=True,
                                                              tfidfmode='BM25Plus')
    if ranker == 'mmr_maxdf':
        version = 'mmr_maxdf'
        rankresult,sent_rank_result,maxdf_doc = sxpWordDist.mmrmaxdf(test_name,keywords,removestop = True, version = version)

    predict = []
    for (id,fid, score, title) in rankresult:
        predict.append(fid)
    #    print(id,fid, score, title)
    if topk == '1':
        topk  = len(truthid)
    if topk == '2':
        topk = 2*len(truthid)
    result = sxpMetricScore.precisionat_topk(predict,truthid,topk=topk)
    print(chname,ch_title,result)
    outsubdir = output_dir + '/' + test_name+ '/' + ranker
    fname = outsubdir + '/' + ranker + chname + 'wd_top_len.result.dict'
    sxpReadFileMan.CheckMkEachLevelSub(outsubdir)
    #fname = outsubdir + '/'+ranker+chname +'wd_top_len.result.dict'
    print('save to',fname)
    testinfo={}
    testinfo['chname']=chname
    testinfo['title'] = ch_title
    testinfo['truth'] = fulltxt_fid_list
    testinfo['result']= result
    testinfo['rankresult']=rankresult
    testinfo['sent_rank_result']=sent_rank_result
  #  sxpReadFileMan.SaveObject(testinfo,fname)
    return testinfo
def ShowResult(testname='wordquery_all',ranker='worddistv6ks_backdirected_sentscore_prefix',plot=False):
    # fname = output_dir + '/'+testname +'_'+ranker+'_wd_top_len.result.dict'
    # sxpReadFileMan.SaveObject(allresult,fname)
    # fname = output_dir + '/' + testname  +'_'+ranker + '_wd_top_len.allscore.dict'
    # sxpReadFileMan.SaveObject(allscore, fname)

    fname = output_dir + '/' + testname + '_'+ranker + '_wd_top_len.allscore.dict'
    allscore=sxpReadFileMan.LoadObject(fname)

    df =pd.DataFrame(allscore).T
    csvname = fname + '.csv'
    df.to_csv(csvname)
    # result['precision']=precision
    # result['recall'] = recall
    # result['fscore'] = fscore
    # result['jaccard'] = jaccard
    print('------average precision', df["precision"].mean())
    print('------average recall',df['recall'].mean())
    print('------average fscore', df['fscore'].mean())
    print('------average jaccard', df['jaccard'].mean())
    testscore={}
    testscore['precision']=df["precision"].mean()
    testscore['recall'] = df["precision"].mean()
    testscore['fscore'] = df["fscore"].mean()
    testscore['test'] = testname
    df = pd.DataFrame([testscore]).T
    csvname = fname + 'prec_recall_fscore.csv'
    df.to_csv(csvname)
    print(df.head())
    if plot:
        plt.figure()
        df.plot.bar()
        jfname = fname + '.jpg'
        plt.savefig(jfname)
        plt.show()
    return testscore
def main():
   # wdtest()
   #  RunWordDistV4()
    #cmd = ['Build','maintest']
    cmd = ['RankACLWithPrefix',
            'Ranktfidf',
           'RankACL',
           'RankACLNoPrefix',
           'RankACLDTFIPF',
           'RankACLBM25',
           ]
    time_record = {}


    fname = output_dir + '/' + 'time_record.dict'
    time_record = sxpReadFileMan.LoadObject(fname)
    if time_record is None:
        time_record = {}

    fname = output_dir + '/' + 'result_list.obj'
    result_list = sxpReadFileMan.LoadObject(fname)
    if result_list is None:
        result_list = []
    if 'BuildTFIDF' in cmd:
      #  BuildBM25(bmmodel='BM25Okapi')
      #  BuildTFIDF(tfidfmode='tfidf')
        BuildTFIDF(tfidfmode='dtfipf')
    if 'Ranktfidf' in cmd:
        start_time = time.process_time()
        prf=Ranktfidf()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['Ranktfidf'] = end_time - start_time
    if 'RankACL' in cmd:
        start_time = time.process_time()
        prf = RankACL()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['RankACL'] = end_time - start_time
    if 'RankACLWithPrefix' in cmd:
        start_time = time.process_time()
        prf = RankACLWithPrefix()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['RankACLWithPrefix'] = end_time - start_time
    if 'RankACLNoPrefix' in cmd:
        start_time = time.process_time()
        prf = RankACLNoPrefix()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['RankACLNoPrefix'] = end_time - start_time
    if 'RankACLDTFIPF' in cmd:
        start_time = time.process_time()
        prf = RankACLDTFIPF()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['RankACLDTFIPF'] = end_time - start_time

    if 'RankACLBM25' in cmd:
        start_time = time.process_time()
        prf = RankACLBM25()
        result_list.append(prf)
        end_time = time.process_time()
        time_record['RankACLBM25'] = end_time - start_time
    fname = output_dir +'/' + 'time_record.dict'
    sxpReadFileMan.SaveObject(time_record,fname)
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
    fname = output_dir +'/' + 'time_record.csv'
    df = pd.DataFrame([time_record])
    df.to_csv((fname))

    fname = output_dir +'/' +'result_list.obj'
    sxpReadFileMan.SaveObject(result_list,fname)
    fname = output_dir +'/' +'result_list.csv'
    df = pd.DataFrame(result_list)
    df.to_csv(fname)
if __name__ == '__main__':
    main()
