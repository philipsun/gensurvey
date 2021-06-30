#coding=UTF-8
import sxpWordDist
import sxpReferMan
import sxpReadFileMan
import sxpMetricScore
import pandas as pd
from numpy import linalg as LA
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import sxpOptimizeDocRank
import sxpLinearReg
from sxpMultiPaperData import sxpNode
import sxpMultiPaperData
import sxpSurveyData
import sxpExtractText

output_dir = r'./test/multipaper/test/out/keywordquery'
sxpReadFileMan.CheckMkDir(output_dir)

def RunTest(testname,chname,ranker='worddist'):
    chapter_dict = sxpReferMan.GetAllChapterDict()
   # chname = '2'
    sel_ch =chapter_dict[chname]
    ch_title = sel_ch['title']
    fulltxt_fid_list = sel_ch['fulltxt_fid']
    if len(fulltxt_fid_list)==0:
        print('no full txt paper')
        return None
    truthid= []
    for (refid, ref,fulltext_fid) in fulltxt_fid_list:
        truthid.append(fulltext_fid)
    print(chname,ch_title,fulltxt_fid_list)
    test_name = testname+'_'+chname
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
    if ranker == 'worddistv3':
        version = 'v3'
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
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'wordistv6_dcd_sentscore':
        version = 'dual_v6_dcd'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'wordistv6_fcd_sentscore':
        version = 'dual_v6_fcd'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'worddistv6ks_dual_sentscore_noexclusion':
        version = 'dual_v6_noexclusion'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'worddistv6ks_dual_sentscore_meanclose':
        version = 'dual_v6_exclusion_meanclose'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'worddistv6ks_dual_sentscore_v1':
        version = 'dual_v6_exclusion_meanclose_v1'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'dual_v6_exclusion_meannormclose_v2_reci':
        version = 'dual_v6_exclusion_meannormclose_v2_reci'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)

    if ranker == 'dual_v6_exclusion_meannormclose_v2_covr':
        version = 'dual_v6_exclusion_meannormclose_v2_covr'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'dual_v6_exclusion_meannormclose_v2_covr_nodense':
        version = 'dual_v6_exclusion_meannormclose_v2_covr_nodense'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)
    if ranker == 'dual_v6_exclusion_meannormclose_v2_reci_nodense':
        version = 'dual_v6_exclusion_meannormclose_v2_reci_nodense'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)

    if ranker == 'dual_v6_exclusion_meannormclose_v2_reci_onlyself':
        version = 'dual_v6_exclusion_meannormclose_v2_reci_onlyself'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)

    if ranker == 'dual_v6_exclusion_meannormclose_v2_covr_onlyself':
        version = 'dual_v6_exclusion_meannormclose_v2_covr_onlyself'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                prefix=Prefix,
                                                                                fidlist=[],
                                                                                removestop=True,
                                                                                version=version)

    if ranker == 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose':
        version = 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                    prefix=Prefix,
                                                                                    fidlist=[],
                                                                                    removestop=True,
                                                                                    version=version)

    if ranker == 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose':
        version = 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose'
        Prefix = []
        rankresult, sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                    prefix=Prefix,
                                                                                    fidlist=[],
                                                                                    removestop=True,
                                                                                    version=version)
    if ranker == 'worddistv6ks_dual_sentscore_prefix':
        version = 'dual_v6'
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_dual_sentscore_prefixnoeven':
        version = 'dual_v6_noeven'
        Prefix = ['in this|we|our|this']
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_dual_sentscore_noeven':
        version = 'dual_v6_noeven'
        Prefix = []
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
    if ranker == 'worddistv6ks_dual_sentscore_nodens_reci':
        version = 'dual_v6_nodens_reci'
        Prefix = []
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name, keywords,
                                                                                   prefix=Prefix,
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_directed_dual_sentscore':
        version = 'dual_v6_directed'
        prefix=[]
        rankresult,sent_rank_result = sxpWordDist.DualKeywordSentRankCloseWordDist(test_name,
                                                                                   keywords,
                                                                                   prefix=[],
                                                                                   fidlist=[],
                                                                                   removestop=True,
                                                                                   version=version)
    if ranker == 'worddistv6ks_backdirected_sentscore_prefix':
        version = 'dual_v6_backdirected'
        Prefix = ['in this|we|our|this']
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
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords)
    if ranker == 'tfidf_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True)

    if ranker == 'dtfipf_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True,tfidfmode='dtfipf')
    if ranker == 'tfief_stopword':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True,tfidfmode='tfief')

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
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True,
                                                              tfidfmode='BM25Okapi')
    if ranker == 'BM25L':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True,
                                                              tfidfmode='BM25L')
    if ranker == 'BM25Plus':
        rankresult,sent_rank_result  = sxpWordDist.tfidfquery(test_name, keywords,removestop=True,
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
    fname = output_dir + '/'+ranker+chname +'wd_top_len.result.dict'
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

def RunAllCh(testname = 'wordquery_all',ranker='worddist'):
    chapter_dict = sxpReferMan.GetAllChapterDict()
    allscore = {}
    allresult = {}
    for ch,chapter_dict_info in chapter_dict.items():
        testinfo = RunTest(testname,ch,ranker)
        if testinfo:
            allscore[ch]=testinfo['result']
            allresult[ch]=testinfo
        print(testname,ranker)
    fname = output_dir + '/'+testname + '_wd_top_len.result.dict'
    sxpReadFileMan.SaveObject(allresult,fname)
    fname = output_dir + '/' + testname + '_wd_top_len.allscore.dict'
    sxpReadFileMan.SaveObject(allscore, fname)
def ShowResult(testname='wordquery_all',plot=False):
    fname = output_dir + '/' + testname + '_wd_top_len.allscore.dict'
    allscore=sxpReadFileMan.LoadObject(fname)

    df =pd.DataFrame(allscore).T
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
    csvname = fname + '.csv'
    df.to_csv(csvname)
    print(df.head())
    if plot:
        plt.figure()
        df.plot.bar()
        jfname = fname + '.jpg'
        plt.savefig(jfname)
        plt.show()
    return testscore
def ShowRankResult(testname='wordquery_all'):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    for ch, testinfo in allresult.items():
        print(ch,testinfo['title'])
        print(testinfo)
    allresult[ch]=testinfo
# testname = 'wordquery_allv6'
# ranker = 'worddistv6'
# chapter = u'4.21'
# chapter = u'8'
def LoadChapterRankResult(testname,chaptertitle):
    s = re.split(r'\-t',chaptertitle)
    chapter = s[0]
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    if chapter not in allresult.keys():
        return None
    testinfo = allresult[chapter]
    # {'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}
    return testinfo
def ShowAllChapter(testname):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    for chpater,testinfo in allresult.items():
        print(chpater, testinfo['title'])
        ShowChapterRankResult(testname, chpater)
def ShowAllChapterTitle(testname):
    fname = output_dir + '/' + testname + '_wd_top_len.result.dict'
    allresult = sxpReadFileMan.LoadObject(fname)
    for chpater, testinfo in allresult.items():
        print('-----')
        print(chpater, testinfo['title'])
        print(len(testinfo['truth']))
    suverypaper = sxpSurveyData.GetSuveryChapterSent()
    chapter_list =suverypaper['chapter_list']
    for doc_dict in chapter_list:
        print(doc_dict['fid'], doc_dict['title'])
def GetChapterTestInfo(testname,chid):
    fname = output_dir + '/' + testname + '_wd_top_len.result.dict'
    allresult = sxpReadFileMan.LoadObject(fname)
    testinfo = allresult[chid]
    return testinfo
def detecttopk(rankmethod):
    pt = '([A-Za-z]+)(\d+)$'
    m = re.match(pt, rankmethod)
    if m:
        print(m.groups()[0], m.groups()[1])
        return m.groups()[0], m.groups()[1]
    else:
        return None
def ShowGenSurv(testname,topkmethod):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    for chpater,testinfo in allresult.items():
        print('------load this chatper', chpater, testinfo['title'])
        topk = LoadDualTopkResult(testname, topkmethod, chpater)
        print("topk['true_citedoc_num']",topk['true_citedoc_num'])
        print("topk['survey_chapter_wd_len']", topk['survey_chapter_wd_len'])
        print("topk['survey_chapter_sent_len']", topk['survey_chapter_sent_len'])
        print("chapter_survey_sent_list",len(topk['chapter_survey_sent_list']))
        print("topk['chapter_gensum_topknum']", topk['chapter_gensum_topknum'])
        print("topk['chapter_gensum_sentnum']", topk['chapter_gensum_sentnum'])
        print("topk['chapter_gensum_word_len'",topk['chapter_gensum_word_len'])

        # surveydoc_numlist.append(topk['true_citedoc_num'])
        # sumdoc_numlist.append(topk['chapter_gensum_topknum'])
        # surveysent_numlist.append(topk['survey_chapter_sent_len'])
        # sumsent_numlist.append(topk['chapter_gensum_sentnum'])
        # surveyword_numlist.append(topk['survey_chapter_wd_len'])
        # sumdocratio_numlist.append(topk['seldocratio']) #seldocratio=topk*1.0/totalnumdoc
        chapter_survey_sent_list=topk['chapter_survey_sent_list']
        for i,s in enumerate(chapter_survey_sent_list):
            print(i,s)

def GetSurveyChapterText():
    chaptersent_dict=sxpSurveyData.GetSuveryChapterSent()
    chapter_list=chaptersent_dict['chapter_list']
    all_chapter_dict = {}
    for chapter_dict in chapter_list:
        print('GetSurveyChapterText',chapter_dict['title'])
        ss = chapter_dict['sent']
        allsent_list =[]
        for s in ss:
            sent_list = sxpExtractText.MySenteceInReuter(s)
            for ns in sent_list:
                allsent_list.append(ns)
        print('sent len',len(allsent_list))
        t = 0
        for st in allsent_list:
            t = t + len(st)
        chapter_dict['wordlen']=t
        chapter_dict['sentlen']=len(allsent_list)
        chapter_dict['sent_list']=allsent_list
        print(chapter_dict['fid'])
        if chapter_dict['fid']=='0054':
            br = 1;
        rs = re.split(r'\-t',chapter_dict['title'])
        if len(rs)>=2:
            chid = rs[0].strip()
            if len(chid)>0:
                print(chid,'word len',t)
                all_chapter_dict[chid]=chapter_dict
    fname = output_dir + '/' + 'allchapter_survey_sent.dict'
    sxpReadFileMan.SaveObject(all_chapter_dict,fname)

def BuilAllTopk(testname,topkmethod='opt',compress_factor=0.05,plotchapter=False):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)

    fname = output_dir + '/'+ 'allchapter_survey_sent.dict'
    all_chapter_dict=sxpReadFileMan.LoadObject(fname)
    # chapter_dict = {}
    # chapter_dict['fid'] = '{:0=4}'.format(i)
    # chapter_fid_dict[chapter_dict['fid']] = chapter_sent_dict[chapter]
    # chapter_dict['title'] = chapter;
    # chapter_dict['sent'] = chapter_sent_dict[chapter]

    chapter_refid_dict = sxpReferMan.GetRefFid()

    doc_sent_num_dict = sxpMultiPaperData.LoadAllPaperSentNum()
    stlen_dict= doc_sent_num_dict['sent_dict']
    all_paper_sent_len = 0
    all_paper_word_len =0
    for fid,[sl, wl] in stlen_dict.items():
        all_paper_sent_len = all_paper_sent_len + sl
        all_paper_word_len = all_paper_word_len + wl

    allsurveyword_num = 0
    allsurveysent_num = 0
    for chpater,testinfo in allresult.items():
        print('--------BuilAllTopk count raw data truth----------')
        print(chpater, testinfo['title'])
        if chpater in all_chapter_dict.keys():
            # print('words in this chapter',all_chapter_dict[chpater]['wordlen'])
            # print("chapter_dict['fid']",all_chapter_dict[chpater]['fid'],all_chapter_dict[chpater]['title'])
            allsurveyword_num = allsurveyword_num + all_chapter_dict[chpater]['wordlen']

            allsurveysent_num =  allsurveysent_num + all_chapter_dict[chpater]['sentlen']

            doc_dict = all_chapter_dict[chpater]
            modelchapter = doc_dict['sent']
            src = ".".join(modelchapter)
            wordnum = len(src)
            sentlen = len(modelchapter)
            print('wordnum compare',doc_dict['wordlen'],wordnum)
            print('sentlen compare', doc_dict['sentlen'], sentlen)
        else:
            print('no sentence len data here')
        print("testinfo[title']", testinfo['title'])
        print("testinfo['truth']", testinfo['truth'])
        print("testinfo['result']", testinfo['result'])
        #=sent_rank_result contains a dict with fid as key and for each paper
        #it contains another dict  with sent_score, ranked idx, and ranked sent
        print("testinfo['sent_rank_result']", len(testinfo['sent_rank_result']))
    leninfo = {}
    leninfo['all_paper_sent_len']= all_paper_sent_len
    leninfo['all_paper_word_len'] = all_paper_word_len
    leninfo['allsurveyword_num'] = allsurveyword_num #the word num in servey for this chapter
    leninfo['allsurveysent_num'] = allsurveysent_num #the sent num in survey for this cpahter
    leninfo['survey_compressor']= allsurveyword_num*1.0/all_paper_word_len
    print('leninfo',leninfo)
    topk_list=[]
    topk_dict= {}
    surveydoc_numlist=[]
    sumdoc_numlist = []
    surveysent_numlist =[]
    sumsent_numlist =[]
    surveyword_numlist=[]
    sumdocratio_numlist = []
    sumword_numlist =[]
    predict_score_list = []


    for chpater,testinfo in allresult.items():
        print('processing chapter:-------->',chpater)
        if chpater == '1':
            br = 1
        print('num of words in this chapter', all_chapter_dict[chpater]['wordlen'])
        print("num of sents in this chapter",  all_chapter_dict[chpater]['sentlen'])

        leninfo['survey_chapter_sent_len'] = all_chapter_dict[chpater]['sentlen']
        leninfo['survey_chapter_wd_len'] = all_chapter_dict[chpater]['wordlen']
        #compress_factor = 0.1;
        if topkmethod == 'TP':
            topk = BuildTopKChapterRankResult(allresult, testname,
                                              chpater,
                                              leninfo,
                                              doc_sent_num_dict['sent_dict'],
                                              compress_factor,
                                              topkmethod)
        #compress_factor = 0.1;
        if topkmethod == 'maxseg':

            topk = BuildTopKChapterRankResult(allresult, testname,
                                              chpater,
                                              leninfo,
                                              doc_sent_num_dict['sent_dict'],
                                              compress_factor,
                                              topkmethod)
        #compress_factor = 0.1;

        if topkmethod == 'LRTP':
            topk = BuildTopKChapterRankResult(allresult, testname,
                                              chpater,
                                              leninfo,
                                              doc_sent_num_dict['sent_dict'],
                                              compress_factor,
                                              topkmethod)

        if topkmethod == 'LR':

            topk = BuildTopKChapterRankResult(allresult, testname,
                                              chpater,
                                              leninfo,
                                              doc_sent_num_dict['sent_dict'],
                                              compress_factor,
                                              topkmethod)
        if topkmethod == 'opt':
            topk=BuildTopKChapterRankResult(allresult,testname,
                                        chpater,
                                        leninfo,
                                        doc_sent_num_dict['sent_dict'],
                                        compress_factor,
                                            topkmethod)
        if topkmethod == 'opt_num':
            topk=BuildTopkBySurveyLen(allresult,testname,
                                        chpater,
                                        leninfo,
                                        doc_sent_num_dict['sent_dict'],
                                        compress_factor)
        if topkmethod == 'opt_var':
            topk=BuildTopKChapterRankResult(allresult, testname,
                                        chpater,
                                        leninfo,
                                        doc_sent_num_dict['sent_dict'],
                                        compress_factor,
                                            topkmethod)
        if topkmethod == 'avg_max_gap':
            topk=BuildTopKChapterRankResult(allresult, testname,
                                        chpater,
                                        leninfo,
                                        doc_sent_num_dict['sent_dict'],
                                        compress_factor,
                                            topkmethod)
        if topkmethod == 'orig':
            topk = BuildTopKChapterRankResult(allresult, testname,
                                        chpater,
                                        leninfo,
                                        doc_sent_num_dict['sent_dict'],
                                        compress_factor,
                                            topkmethod)
        topkrun= detecttopk(topkmethod)
        print('topkrun',topkrun)
        if topkrun:
            topk = BuildTopKChapterRankResult(allresult, testname,
                                          chpater,
                                          leninfo,
                                          doc_sent_num_dict['sent_dict'],
                                          compress_factor,
                                          topkmethod)

        topk['survey_chapter_sent_len'] = all_chapter_dict[chpater]['sentlen']
        topk['survey_chapter_wd_len'] = all_chapter_dict[chpater]['wordlen']



        print("topk['chapter_gensum_topk']=topkdoc is a list contains the select paper's inform: num",
              len(topk['chapter_gensum_topk']))
        # print('''
        #     for i in range(topk):
        # d = {}
        # d['fid']=docfid_list[i]
        # d['title']=rankresult[i][3]
        # d['raw_doc_len'] = paper_len_dict[docfid_list[i]]
        # d['sum_sent_len']=selsentnum*p[i,0]
        # d['rank']=i
        # d['score']=s[i,0]
        # d['percent']=p[i,0]
        # topkdoc.append(d)
        # ''')
        sent_rank_result = testinfo['sent_rank_result']
        # sent_rank_dict['score']=dual_sent_score
        # sent_rank_dict['ranked_sent'] = ranked_sent
        # sent_rank_dict['idx_sent'] = idx_sent
        # sent_rank_result[fname_dict['fid']]=sent_rank_dict
        truth_fid =[]
        for each in testinfo['truth']:
            truth_fid.append(each[2])
        chapter_survey_sent_list=[]
        
        refpaperwordlen = 0
        predict_topk = []

        for eachpaper in topk['chapter_gensum_topk']:
            [sl, wl] = stlen_dict[eachpaper['fid']]
            refpaperwordlen = refpaperwordlen + wl
            predict_topk.append(eachpaper['fid'])
        predict_score=sxpMetricScore.precisionat_topk(predict_topk, truth_fid, topk=-1)
        chapter_gensum_word_len = 0
        for eachpaper in topk['chapter_gensum_topk']: #here store every paper in topk
            sent_dict = sent_rank_result[eachpaper['fid']]
            if eachpaper['fid'] in chapter_refid_dict.keys():
                refdict=chapter_refid_dict[eachpaper['fid']]
                refname = refdict['refname']
            else:
                refname = eachpaper['fid']

            percent = eachpaper['percent']
            print('percent',percent, eachpaper['score'])

            sum_word_len =eachpaper['sum_word_len']
            sum_sent_len = eachpaper['sum_sent_len']
            t = 0
            refsent = 'In ({0}):'.format(refname)
            chapter_survey_sent_list.append(refsent)
            w = 0;
            for s in sent_dict['ranked_sent']:
                # if t>sum_sent_len:
                #    break
                chapter_survey_sent_list.append(s)
                t = t + 1
                chapter_gensum_word_len = chapter_gensum_word_len + len(s)
                w = w + len(s)
                if w > sum_word_len and t>2:
                     break

            eachpaper['sum_sent_len']=t

        topk['chapter_survey_sent_list']=chapter_survey_sent_list
        topk['chapter_gensum_word_len'] = chapter_gensum_word_len
        topk['chapter']=chpater
        topk['predict_score'] = predict_score
        predict_score_list.append(predict_score)
        topk_list.append(topk)
        topk_dict[chpater]=topk

        print('true chapter ref num',topk['true_citedoc_num'])
        print('gensum chapter ref num', topk['chapter_gensum_topknum'])
        print('true chapter sent num',topk['survey_chapter_sent_len'])
        print('gensum chapter sent num', topk['chapter_gensum_sentnum'])
        print('true chapter word num',topk['survey_chapter_wd_len'])
        print('gensum chapter word num', topk['chapter_gensum_word_len'])

        print('orgin chapter word num',leninfo['survey_chapter_wd_len'])
        print('gen survy word num', chapter_gensum_word_len)
      #  fname = 'topk_'+ chpater + '.dict'
        topkfname = 'topk_' + testname + '_' + topkmethod + '_' + chpater + '.dict'
        print('save topk to ',topkfname)
        sxpReadFileMan.SaveObject(topk,topkfname,output_dir)
        # chapter_topk_dict['chapter_gensum_topknum'] = topk
        # chapter_topk_dict['chapter_gensum_sentnum'] = selsentnum
        surveydoc_numlist.append(topk['true_citedoc_num'])
        sumdoc_numlist.append(topk['chapter_gensum_topknum'])
        surveysent_numlist.append(topk['survey_chapter_sent_len'])
        sumsent_numlist.append(topk['chapter_gensum_sentnum'])
        surveyword_numlist.append(topk['survey_chapter_wd_len'])
        sumdocratio_numlist.append(topk['seldocratio']) #seldocratio=topk*1.0/totalnumdoc
        sumword_numlist.append(chapter_gensum_word_len)
       # sumword_numlist.append()
    result_dict = {}
    result_dict['chapter_topk'] = topk_dict
    result_dict['allsurveysent_num'] = allsurveysent_num
    result_dict['allsurveyword_num'] = allsurveyword_num
    result_dict['all_paper_sent_len'] = all_paper_sent_len
    result_dict['all_paper_word_len'] = all_paper_word_len

    result_dict['surveydoc_numlist'] = surveydoc_numlist
    result_dict['surveysent_numlist'] = surveysent_numlist
    result_dict['surveyword_numlist'] = surveyword_numlist
    result_dict['sumdoc_numlist'] = sumdoc_numlist
    result_dict['sumdocratio_numlist'] = sumdocratio_numlist
    result_dict['sumword_numlist'] = sumword_numlist
    fname = output_dir + '/'+ testname + '_'+topkmethod + '_wd_topk_leninfo.result.dict'
    sxpReadFileMan.SaveObject(result_dict,fname)

    fname1 = fname +'.sumsurvey.jpg'
    t1='true_citedoc_num'
    t2 = 'chapter_gensum_topknum'
    dsurveydoc_numlist = np.array(surveydoc_numlist).reshape(-1,1)
    dsumdoc_numlist = np.array(sumdoc_numlist).reshape(-1, 1)
    if plotchapter:
        sxpPlotBar.plotlinelist([dsurveydoc_numlist,dsumdoc_numlist], [t1,t2], title='sum doc len'
                            , fname=fname1)


    fname2 = fname +'.sumsurveyword.jpg'
    t1='survey_word_len'
    t2 = 'gen_sum_word_len'
    dsurveyword_numlist = np.array(surveyword_numlist).reshape(-1,1)
    dsumword_numlist = np.array(sumword_numlist).reshape(-1, 1)
    if plotchapter:
        sxpPlotBar.plotlinelist([dsurveyword_numlist,dsumword_numlist], [t1,t2], title='sum sent len'
                            , fname=fname2)

    fname3 = fname +'.sumsurveysent.jpg'
    t1='survey_sent_len'
    t2 = 'gen_sum_sent_len'
    dsurveysent_numlist = np.array(surveysent_numlist).reshape(-1,1)
    dsumsent_numlist = np.array(sumsent_numlist).reshape(-1, 1)
    if plotchapter:
        sxpPlotBar.plotlinelist([dsurveysent_numlist, dsumsent_numlist], [t1,t2], title='sum word len'
                            , fname=fname3)

    # diff_dict['avg'] = np.mean(diff, 0)
    # diff_dict['va'] = np.std(diff, 0)
    # diff_dict['aavg'] = np.mean(absdiff, 0)
    # diff_dict['ava'] = np.std(absdiff, 0)
    df = pd.DataFrame(predict_score_list)
    dfname = fname +'.predicttopk_score.csv'
    df.to_csv(dfname)
    scoredict ={}
    scoredict['predict_precision']=df['precision'].mean()
    scoredict['predict_recall'] = df['recall'].mean()
    scoredict['predict_fscore'] = df['fscore'].mean()

    doc_dist = computediff(dsurveydoc_numlist,dsumdoc_numlist)
    print('doc num distance',doc_dist)
    sxpReadFileMan.copydict(scoredict,doc_dist,'doc_')
    sent_dist = computediff(dsurveysent_numlist,dsumsent_numlist)
    print('sent num distance',sent_dist)
    sxpReadFileMan.copydict(scoredict, sent_dist, 'sent_')
    word_dist = computediff(dsurveyword_numlist,dsumword_numlist)
    print('word num distance',word_dist)
    sxpReadFileMan.copydict(scoredict, word_dist, 'word_')

    distdf = pd.DataFrame({"tr_doc":surveydoc_numlist,
                           "pr_doc":sumdoc_numlist,
                           "tr_sent":surveysent_numlist,
                           "pr_sent":sumsent_numlist,
                           "tr_word":surveyword_numlist,
                           "pr_word":sumword_numlist})
    alldf = pd.concat([distdf,df],axis=1)
    scoreweight = computeweightscore(alldf)
    scoredict['wp']= scoreweight['wps']
    scoredict['wr'] = scoreweight['wrs']
    scoredict['wf'] = scoreweight['wfs']
    scoredict['truen'] = scoreweight['truen']
    scoredict['predn'] = scoreweight['predn']
    scoredict['nr'] = scoreweight['nr']
    pathfilename =fname +'.num_dist.csv'
    alldf.to_csv(pathfilename)
    pathfilename = fname + 'predict_topk.dict'
    sxpReadFileMan.SaveObject(scoredict,pathfilename)
    return scoredict
def computeweightscore(alldf):
    true_allnum = alldf['tr_doc'].sum()
    pred_allnum = alldf['pr_doc'].sum()
    if pred_allnum>=true_allnum:
        nr = true_allnum/pred_allnum
    else:
        nr = pred_allnum/true_allnum
    alldf['weight'] = alldf['tr_doc']/true_allnum
    alldf['wp'] = alldf['precision']*alldf['weight']
    alldf['wr'] = alldf['recall'] * alldf['weight']
    alldf['wf'] = alldf['fscore'] * alldf['weight']
    wps = alldf['wp'].sum()*nr
    wrs = alldf['wr'].sum() * nr
    wfs = 2*wps*wrs/(wrs+wps)
    score={}
    score['wps']= wps
    score['wrs'] = wrs
    score['wfs'] = wfs
    score['truen']=true_allnum
    score['predn']=pred_allnum
    score['nr'] = nr
    return score
def ShowTopkChid(testname,topkmethod,chpater):
    topkfname = 'topk_' + testname + '_' + topkmethod + '_' + chpater + '.dict'
    print('show topk name ', topkfname)
    topk = sxpReadFileMan.LoadObject(topkfname,output_dir)
    print('chapter_gensum_sentnum',topk['chapter_gensum_sentnum'])
    print('chapter_gensum_word_len',topk['chapter_gensum_word_len'])
    topsent = LoadDualRankSent(testname, topkmethod, chpater)
    print('topsent',len(topsent))
from scipy.spatial.distance import  *
def computediff(nd1,nd2):
    d1 = np.array(nd1).reshape((-1,1))
    d2 = np.array(nd2).reshape((-1, 1))
    diff = d1 - d2
    diff_dict={}
    absdiff = np.abs(d1 - d2)
    diff_dict['avg'] = np.mean(diff, 0)[0]
    diff_dict['va'] = np.std(diff, 0)[0]
    diff_dict['aavg'] = np.mean(absdiff, 0)[0]
    diff_dict['ava'] = np.std(absdiff, 0)[0]
    diff_dict['cos'] = cosine(d1,d2)
    diff_dict['euclidean'] = euclidean(d1, d2)
    diff_dict['minkowski'] = minkowski(d1, d2,2)
   # diff_dict['mahalanobis'] = mahalanobis(d1, d2)
    return diff_dict
def LoadDualRankSent(testname,topkmethod,chid):
    # fname = output_dir + '/'+ testname + '_'+topkmethod + '_wd_topk_leninfo.result.dict'
    # result_dict=sxpReadFileMan.LoadObject(fname)
    # topk_dict = result_dict['chapter_topk']
    # topk= topk_dict[chid]
    topkfname = 'topk_' + testname + '_'+topkmethod +'_'+chid+'.dict'
    topk = sxpReadFileMan.LoadObject(topkfname,output_dir)
    chapter_survey_sent_list=topk['chapter_survey_sent_list']
    return chapter_survey_sent_list
def LoadDualRankTopk(testname,topkmethod,chid):
    topkfname = 'topk_'+ testname + '_'+topkmethod +'_'+chid+'.dict'
    topk = sxpReadFileMan.LoadObject(topkfname,output_dir)
    return topk
def LoadDualTopkResult(testname,topkmethod,chid):
    fname = output_dir + '/'+ testname + '_'+topkmethod + '_wd_topk_leninfo.result.dict'
    result_dict=sxpReadFileMan.LoadObject(fname)
    topk_dict = result_dict['chapter_topk']
    topk= topk_dict[chid]
    return topk
def GetAllTopK(testname,topkmethod='opt'):
    fname = output_dir + '/'+ testname + '_'+topkmethod + '_wd_topk_leninfo.result.dict'
    topk_dict= sxpReadFileMan.LoadObject(fname)
    return topk_dict
def ShowChapterRankResult(testname,chpater):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    testinfo = allresult[chpater]
    print('----------chapter-------',testinfo['title'],chpater)
    print('----------truth----------')
    for each in testinfo['truth']:
        print(each)#(u'CR11', u'Bairi et-al. 2015', '0088')
    print('----------rankresult----------')
    #(id,fid, score, title) in rankresult
    # for each in testinfo['rankresult']:
    #     print(each)
    #chapter = testinfo['title']
    labelnamelist=[chpater]
    fname = testname + '_'+ chpater +'_scorelist.jpg'
    fullname = os.path.join(output_dir,fname)
    print(fullname)
   # PlotRankResult(testinfo['rankresult'],labelnamelist,fullname)
    fname =testname + '_'+ chpater +'_dfscorelist.jpg'
    fullname = os.path.join(output_dir,fname)
#    SelectTopK(testinfo['rankresult'],labelnamelist,fullname)
def BuildTopkBySurveyLen(allresult,testname,chpater,leninfo,paper_len_dict,compress_factor):
    # fname = output_dir + '/' + testname + '_wd_top_len.result.dict'
    # allresult = sxpReadFileMan.LoadObject(fname)
    testinfo = allresult[chpater]
    print('------build for chapter-------')
    print(testinfo['title'], chpater)
    print('----------truth----------')
    refpapernuminchapter = 0
    refpapersentnuminchapter = 0
    refpaperwordnuminchapter = 0
    for each in testinfo['truth']:
        print(each)
        # (u'CR11', u'Bairi et-al. 2015', '0088')
        refpapernuminchapter = refpapernuminchapter + 1;
        sl, wl = paper_len_dict[each[2]]
        refpapersentnuminchapter = refpapersentnuminchapter + sl
        refpaperwordnuminchapter = refpaperwordnuminchapter + wl
    print('survey chapter ref doc num, sentnum, wordnum',refpapernuminchapter,refpapersentnuminchapter,refpaperwordnuminchapter )
    leninfo['true_doc_num']=refpapernuminchapter
    print('----------determine topk for this ----------')
    # for each in testinfo['rankresult']:
    #     print(each)
    # chapter = testinfo['title']
    labelnamelist = [chpater]
    fname = testname + '_' + chpater + '_scorelist.jpg'
    fullname = os.path.join(output_dir, fname)
    # print(fullname)
    # PlotRankResult(testinfo['rankresult'],labelnamelist,fullname)
    fname = testname + '_' + chpater + '_dfscorelist.jpg'
    fullname = os.path.join(output_dir, fname)

    doctopk = SelectTopKbySurv(testinfo['rankresult'],
                         labelnamelist,
                         fullname,
                         paper_len_dict,
                         leninfo,
                         compress_factor)
    doctopk['true_citedoc_sent_num'] = refpapersentnuminchapter
    doctopk['true_wd_len'] = refpaperwordnuminchapter
    doctopk['true_citedoc_num'] = refpapernuminchapter

    return doctopk
def BuildOriginalTopke(allresult,testname,chpater,leninfo,paper_len_dict,compress_factor,topk='orig'):
    # fname = output_dir + '/' + testname + '_wd_top_len.result.dict'
    # allresult = sxpReadFileMan.LoadObject(fname)

    testinfo = allresult[chpater]
    print('------build for chapter-------')
    print(testinfo['title'], chpater)
    print('----------truth----------')
    refpapernuminchapter = 0
    refpapersentnuminchapter = 0
    refpaperwordnuminchapter = 0
    for each in testinfo['truth']:
        print(each)
        # (u'CR11', u'Bairi et-al. 2015', '0088')
        refpapernuminchapter = refpapernuminchapter + 1;
        sl, wl = paper_len_dict[each[2]]
        refpapersentnuminchapter = refpapersentnuminchapter + sl
        refpaperwordnuminchapter = refpaperwordnuminchapter + wl
    print('----------determine topk for this ----------')
    # for each in testinfo['rankresult']:
    #     print(each)
    # chapter = testinfo['title']
    labelnamelist = [chpater]
    fname = testname + '_' + chpater + '_scorelist.jpg'
    fullname = os.path.join(output_dir, fname)
    # print(fullname)
    # PlotRankResult(testinfo['rankresult'],labelnamelist,fullname)
    fname = testname + '_' + chpater + '_dfscorelist.jpg'
    fullname = os.path.join(output_dir, fname)
    leninfo['refpapernuminchapter'] = refpapernuminchapter
    leninfo['true_doc_num'] = refpapernuminchapter
    doctopk = SelectTopKbySurv(testinfo['rankresult'],
                         labelnamelist,
                         fullname,
                         paper_len_dict,
                         leninfo,
                         compress_factor,
                         topk)
    doctopk['true_citedoc_sent_num'] = refpapersentnuminchapter
    doctopk['true_wd_len'] = refpaperwordnuminchapter
    doctopk['true_citedoc_num'] = refpapernuminchapter

    return doctopk
def BuildTopKChapterRankResult(allresult,testname,chpater,leninfo,paper_len_dict,compress_factor,topk='opt'):
    # fname = output_dir + '/' + testname + '_wd_top_len.result.dict'
    # allresult = sxpReadFileMan.LoadObject(fname)

    testinfo = allresult[chpater]
    print('------build for chapter-------')
    print(testinfo['title'], chpater)
    print('----------truth----------')
    refpapernuminchapter = 0
    refpapersentnuminchapter = 0
    refpaperwordnuminchapter = 0

    for each in testinfo['truth']:
        print(each)

        # (u'CR11', u'Bairi et-al. 2015', '0088')
        refpapernuminchapter = refpapernuminchapter + 1;
        sl, wl = paper_len_dict[each[2]]
        refpapersentnuminchapter = refpapersentnuminchapter + sl
        refpaperwordnuminchapter = refpaperwordnuminchapter + wl
    print('survey chapter ref doc num, sentnum, wordnum',refpapernuminchapter,refpapersentnuminchapter,refpaperwordnuminchapter )
    leninfo['true_doc_num']=refpapernuminchapter
    print('----------determine topk for this ----------')
    # for each in testinfo['rankresult']:
    #     print(each)
    #chapter = testinfo['title']
    labelnamelist=[chpater]
    fname = testname + '_'+ chpater +'_scorelist.jpg'
    fullname = os.path.join(output_dir,fname)
   # print(fullname)
   # PlotRankResult(testinfo['rankresult'],labelnamelist,fullname)
    fname =testname + '_'+ chpater +'_dfscorelist.jpg'
    fullname = os.path.join(output_dir,fname)
    leninfo['refpapernuminchapter']=refpapernuminchapter
    leninfo['refpapersentnuminchapter']=refpapersentnuminchapter
    doctopk=SelectTopK(testinfo['rankresult'],
                       labelnamelist,
                       fullname,
                       paper_len_dict,
                       leninfo,
                       compress_factor,
                       topk)

    doctopk['true_citedoc_sent_num']=refpapersentnuminchapter
    doctopk['true_wd_len'] = refpaperwordnuminchapter
    doctopk['true_citedoc_num'] = refpapernuminchapter

    return doctopk
import sxpPlotBar
def PlotRankResult(rankresult,chaptername,fname='line.jpg'):

    print('----------plot rankresult----------')
    scorelist=[]
    for each in rankresult:
        #(48, '0048', 0.3395702005053015, 'Improving the Estimation of Word Importance for News Multi-Document Summarization')
        #print(each)
        scorelist.append(each[2])
    sxpPlotBar.plotlinelist([scorelist],[chaptername],title='multiplelines',fname=fname)
def SelectTopKbySurv(rankresult,chaptername,fullname,paper_len_dict,leninfo,compress_factor,topkmode='opt'):
    scorelist = []
    docfid_list = []
    for each in rankresult:
        #  print(each)
        # (55, '0055', 0.0, 'Learning the parts of objects by non-negative matrix factorization')
        docfid_list.append(each[1])
        scorelist.append(each[2])
    s = np.array(scorelist).reshape((-1, 1))
    ds = Diff(s)
    fname = fullname + '.s_ds.jpg'
    t1 = chaptername[0] + 's'
    t2 = chaptername[0] + 'ds'
    #   sxpPlotBar.plotlinelist([s, ds], [t1, t2], title=chaptername[0], fname=fname)

    # print(ds)
    #  ed = EntropyCurve(ds)
    #  he = HistEntropyAtBin(ds)#HistEntropByBinVar(ds)
  #  bine, binravg, tot = sxpOptimizeDocRank.AvgRankRemoveEntropy(s)
  #  topk = sxpOptimizeDocRank.SelectTopk(tot)
    #  leninfo['survey_chapter_sent_len'] = all_chapter_dict[chpater]['sentlen']
    #  leninfo['survey_chapter_wd_len'] = all_chapter_dict[chpater]['wordlen']
    surv_topk = leninfo['true_doc_num']
    surv_sentlen = leninfo['survey_chapter_sent_len']
    surv_wordlen = leninfo['survey_chapter_wd_len']
    selsentnum = leninfo['survey_chapter_sent_len']
    topk = surv_topk
    print('survey chapter ref num, survey chapter sent num, wordnum of chapter', surv_topk, surv_sentlen,surv_wordlen)
    #    print('binentropy', bine)
    #    print('binravg',binravg)
    fname = fullname + '.entrop.jpg'
    #   chaptername.append('entropy')
    #   sxpPlotBar.plotlinelist([ds,ed],chaptername,title='multiplelines',fname=fullname)
    # t1 = chaptername[0] + 'decrrank'
    # t2 = chaptername[0] + 'increntropy'
    # t3 = chaptername[0] + 'sum'
    #   bine = standardization(bine)
    #   binravg  = standardization(binravg)
    #   sxpPlotBar.plotlinelist([bine,binravg,tot], [t1,t2,t3], title=chaptername[0], fname=fname)
    totalnumdoc = len(rankresult)
    seldocratio = topk * 1.0 / totalnumdoc
    allsent_num = leninfo['all_paper_sent_len']
    allword_num = leninfo['all_paper_word_len']
    # leninfo['all_paper_sent_len']= allsurveysent_num
    # leninfo['all_paper_word_len'] = allsurveyword_num
    # leninfo['allsurveyword_num'] = all_paper_sent_len
    # leninfo['allsurveysent_num'] = all_paper_word_len
   # selsentnum = seldocratio * allsent_num * compress_factor
   # selsentnum = leninfo['true_chapter_sent_num']
   # selwordnum = seldocratio * allword_num * compress_factor
    selwordnum = leninfo['survey_chapter_wd_len']
    p = np.ones((topk,1))*1.0/topk
    topkdoc = []
    chapter_topk_dict = {}
    for i in range(topk):
        d = {}
        d['fid'] = docfid_list[i]
        d['title'] = rankresult[i][3]
        d['raw_doc_len'] = paper_len_dict[docfid_list[i]]
        d['sum_sent_len'] = selsentnum * p[i, 0]
        d['sum_word_len']= selwordnum * p[i, 0]
        d['rank'] = i
        d['score'] = s[i, 0]
        d['percent'] = p[i, 0]
        topkdoc.append(d)
    chapter_topk_dict['chapter_gensum_topk'] = topkdoc
    chapter_topk_dict['chapter_gensum_topknum'] = topk
    chapter_topk_dict['chapter_gensum_sentnum'] = selsentnum
    chapter_topk_dict['chapter_gensum_word_len']= selwordnum
    chapter_topk_dict['allsent_num'] = allsent_num
    chapter_topk_dict['allword_num'] = allword_num
    chapter_topk_dict['seldocratio'] = seldocratio
    # print(topkdoc)
    return chapter_topk_dict

def SelectTopK(rankresult,chaptername,fullname,paper_len_dict,leninfo,compress_factor,topkmode='opt'):
    scorelist=[]
    docfid_list=[]
    for each in rankresult:
      #  print(each)
        #(55, '0055', 0.0, 'Learning the parts of objects by non-negative matrix factorization')
        docfid_list.append(each[1])
        scorelist.append(each[2])
    s = np.array(scorelist).reshape((-1,1))
    ds = Diff(s)
    fname = fullname + '.s_ds.jpg'
    t1=chaptername[0] + 's'
    t2 = chaptername[0] + 'ds'
    totalnumdoc = len(rankresult)
    allrefsent_num = leninfo['all_paper_sent_len']
    allrefword_num = leninfo['all_paper_word_len']
    surv_topk = leninfo['true_doc_num']
    survey_chapter_sent_len = leninfo['survey_chapter_sent_len']
    survey_chapter_word_len = leninfo['survey_chapter_wd_len']
    #   sxpPlotBar.plotlinelist([s, ds], [t1, t2], title=chaptername[0], fname=fname)

    #print(ds)
  #  ed = EntropyCurve(ds)
  #  he = HistEntropyAtBin(ds)#HistEntropByBinVar(ds)
 #   bine,binravg,tot = sxpOptimizeDocRank.AvgRankRemoveEntropy(s)
    #    print('he.shape',bine.shape,binravg.shape)
    #    print('binentropy', bine)
    #    print('binravg',binravg)
    #topk = sxpOptimizeDocRank.SelectTopk(tot)
    topkrun = detecttopk(topkmode)
    if topkrun:
        topkmethod = topkrun[0]
        fixedtopk = int(topkrun[1])
        print('select fixed topk ',fixedtopk)
        topk = fixedtopk
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)

    if topkmode == 'maxseg':
        topk = sxpLinearReg.MaxSegTopk(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'avg_max_gap':
        topk = sxpLinearReg.AvgGapMax(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)

    if topkmode == 'TP':
        topk = sxpLinearReg.InfelctionPointTopk(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'LR':
        topk = sxpLinearReg.LinearFitLeft(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'LRTP':
        topk = sxpLinearReg.LinearFitTP(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio*allrefsent_num*compress_factor
        selwordnum = seldocratio  * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'opt':
        topk = sxpOptimizeDocRank.SelectTopk(s)
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio * allrefsent_num * compress_factor
        selwordnum = seldocratio * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'opt_var':
        topk = sxpOptimizeDocRank.SelectTopkByScoreRank(s,mode = 'top')
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = seldocratio * allrefsent_num * compress_factor
        selwordnum = seldocratio * allrefword_num * compress_factor
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    if topkmode == 'orig':
        topk = surv_topk #leninfo['refpapernuminchapter'];
        seldocratio = topk * 1.0 / totalnumdoc
        selsentnum = survey_chapter_sent_len
        selwordnum = survey_chapter_word_len
        print('DocPercent(topk, s)', topk)
        p = DocPercent(topk, s)
        print(p)
    fname = fullname +'.entrop.jpg'

    t1=chaptername[0] + '_ds'
    t2 = chaptername[0] + '_s'
    plotline = False;
    if plotline:
        sxpPlotBar.plotlinelist([ds,s],[t1,t2],title='multiplelines',fname=fname
                            ,vline=[topk, leninfo['refpapernuminchapter']])
    sfname = fullname + 's.list'
    sxpReadFileMan.SaveObject([leninfo['refpapernuminchapter'],s],sfname)
    t1=chaptername[0] + 'decrrank'
    t2 = chaptername[0] + 'increntropy'
    t3 = chaptername[0] + 'sum'
 #   bine = standardization(bine)
 #   binravg  = standardization(binravg)
 #   sxpPlotBar.plotlinelist([bine,binravg,tot], [t1,t2,t3], title=chaptername[0], fname=fname)


    # leninfo['all_paper_sent_len']= allsurveysent_num
    # leninfo['all_paper_word_len'] = allsurveyword_num
    # leninfo['allsurveyword_num'] = all_paper_sent_len
    # leninfo['allsurveysent_num'] = all_paper_word_len


    topkdoc=[]
    chapter_topk_dict ={}
    for i in range(topk):
        d = {}
        d['fid']=docfid_list[i]
        d['title']=rankresult[i][3]
        d['raw_doc_len'] = paper_len_dict[docfid_list[i]]
        d['sum_sent_len']=selsentnum*p[i,0]
        d['sum_word_len']=selwordnum*p[i,0]
        d['rank']=i
        d['score']=s[i,0]
        d['percent']=p[i,0]
        topkdoc.append(d)
    chapter_topk_dict['chapter_gensum_topk'] = topkdoc
    chapter_topk_dict['chapter_gensum_topknum'] = topk
    chapter_topk_dict['chapter_gensum_sentnum'] = selsentnum
    chapter_topk_dict['chapter_gensum_word_len']= selwordnum
    chapter_topk_dict['allsent_num'] = allrefsent_num
    chapter_topk_dict['allword_num'] = allrefword_num
    chapter_topk_dict['seldocratio'] = seldocratio
   # print(topkdoc)
    return chapter_topk_dict
def DocPercent(topk,s):
    ds = s[0:topk,0]
    nms = normalization(ds,'01expsum')
    return nms
def ChapterSentNum(topk,s):
    nms = DocPercent(topk,s)


def Diff(s):
    ds = np.diff(s.ravel()).reshape(-1,1)*-1
    return ds
def EntropyCurve(ss):
    # std = standardization(ds)
    ts=[]
    for sm in ss.ravel():
     ts.append(sm)
    #ds = np.diff(ss,0).reshape((-1,1))
    ds = np.diff(ts).reshape(-1, 1)
    ds = normalization(ds,'01sum')
    nr,nc = ds.shape
    s = np.ones((nr,1))
    for i in range(0,nr):
        et = Entropy(ds[i:nr,0])
        s[i,0]=et
    s = s.ravel()
    print("EntropyCurve(s)",s)
    de = normalization(np.diff(s),'01sum')
    return de.reshape((-1,1))
def Entropy(p):
    nozero = p[p!=0]
    if len(nozero)==0:
        return 0
    e = np.multiply(nozero, np.log2(nozero))
  #  print(e,e.shape)
    s = np.sum(e)*-1
    return s;
def HistEntropByBinVar(ds):
    nd = normalization(ds)
    nr,nc = nd.shape

    # nb = np.log2(nc)
    # #bsize = int(np.ceil(nb+1))

    nb = nr *2/ 3;
    bsize = int(np.ceil(nb+1))
    s = np.ones((1,bsize))

    for i in range(bsize):
        bn = i+1
        hist, bin_edges = np.histogram(nd, bn, density=True)
        p=hist * np.diff(bin_edges,0)

        e = Entropy(p)
        s[i,0]=e


    return s;
def HistEntropyAtBin(ds):
    nd = normalization(ds)
    nr,nc = nd.shape

    # nb = np.log2(nc)
    # #bsize = int(np.ceil(nb+1))

    #nb = nc *2/ 4;
    #nb = np.log2(nc)
    nb = np.power(nr,0.5)
    bsize = int(np.ceil(nb+1))
    bn = bsize
    hist, bin_edges = np.histogram(nd, bn, density=True)
    p = hist * np.diff(bin_edges,0)

    ed = EntropyCurve(p.reshape((-1,1)))
    sed = SecondHist(ed)
    return sed.reshape((-1,1));
def SecondHist(ds):
    nd = normalization(ds)
    nr, nc = nd.shape

    # nb = np.log2(nc)
    # #bsize = int(np.ceil(nb+1))

    # nb = nc *2/ 4;
    # nb = np.log2(nc)
    nb = np.power(nr, 0.5)
    bsize = int(np.ceil(nb + 1))
    bn = bsize
    hist, bin_edges = np.histogram(nd, bn, density=True)
    p = hist * np.diff(bin_edges,0)

    ed = EntropyCurve(p.reshape((-1,1)))
    return ed.reshape((-1,1));
def HistRankOptimize(s):
    ds = np.diff(s,0)
  #  ds.reshape((-1,1))
    nr,nc = ds.shape
    nb = np.log2(nr)
    nb = np.power(nr,0.5)
    bsize = int(np.ceil(nb+1))
    eb,cb_avg = EntropCurvAtBin(s,ds, bsize)
    tot = eb + cb_avg
    return eb,cb_avg,tot
def EntropCurvAtBin(s,ds,nb):

    #  ds = np.diff(s)
    nd = normalization(ds)
    nr,nc = nd.shape

    # nb = np.log2(nc)
    # #bsize = int(np.ceil(nb+1))

    #nb = nc *2/ 4;
    #nb = np.log2(nc)
    #nb = np.power(nc,0.5)
    bsize = int(np.ceil(nb+1))
    bn = bsize

    cbin_prob, cbin_avg, bin_list = MakeBin(s, bn)

    avg_decr=AvgRankDecre(cbin_avg)
    eb = EntropyCurve(cbin_prob)
    return eb,avg_decr
def AvgRankDecre(r):
    n,c = r.shape;
    avglist=[]
    for i in range(1,n-1):
        c = r[0:i,0]
        avglist.append(np.mean(c,0))
    if len(avglist) <=1:
        avg = r;
    else:
        avg = normalization( np.array(avglist).reshape((-1,1)),'01sum')
    return avg
def normalization(data,norm='sum'):

    data = data.reshape(-1,1)
    n,r = data.shape;
    if n == 0:
        return data
    if norm=='max':
        _range = LA.norm(data,0)
    if norm == 'range':
        _range = np.max(data) - np.min(data)
    if norm == 'sum':
        _range=np.sum(data)
        data = data/_range
        return data
    if norm == '01sum':
        _range=np.sum(data - np.min(data))
    if norm == '01expsum':
        _range = np.sum(data - np.min(data))
        if np.abs(_range) <= 0.0000000000001:
            return np.ones((n,1))/n;
        r = (data - np.min(data)) /_range
        smooth = np.exp(r)
        print(smooth)
        return normalization(smooth,'sum')
    if _range == 0:
        _range = 1;
    r= (data - np.min(data)) / _range
    return r.reshape((-1,1))

# ord	norm for matrices	norm for vectors
# None	Frobenius norm	2-norm
# ‘fro’	Frobenius norm	–
# ‘nuc’	nuclear norm	–
# inf	max(sum(abs(x), axis=1))	max(abs(x))
# -inf	min(sum(abs(x), axis=1))	min(abs(x))
# 0	–	sum(x != 0)
# 1	max(sum(abs(x), axis=0))	as below
# -1	min(sum(abs(x), axis=0))	as below
# 2	2-norm (largest sing. value)	as below
# -2	smallest singular value	as below
# other	–	sum(abs(x)**ord)**(1./ord)
def MakeBin(s,binnum):
    s.reshape((-1, 1))
    s = normalization(s,'01sum')
    ds = np.diff(s,0)

    h = np.array(ds[0,0]).reshape(-1,1)
  #  ds = np.vstack((h,ds))
    n,c = ds.shape

    binsize = int(np.ceil(n / binnum))
    print("s.shape,n,c,binsize",s.shape,n,c,binsize)
    cbin = []
    cbin_avg = []
    bin_list = []
    bini = binsize
    cbin_count = []
    cbin_prob = []
    tot = np.sum(s,0)
    for i in range(int(n)):
        if i <= bini:
            cbin.append(i)
        else:
            cbin.append(i)
            if np.sum(s[cbin],0)[0]<=0.0:
                break;
            bini = bini + binsize
            bin_list.append(cbin)
            cbin_count.append(len(cbin))
            #cbin_prob.append(len(cbin)*1.0/n)
            cbin_prob.append(np.sum(s[cbin],0)[0]/tot)
            cbin_avg.append(np.mean(s[cbin],0))
            cbin = []
    if len(cbin)>0:
        bin_list.append(cbin)
      # print('cbin',cbin)
        #cbin_prob.append(len(cbin) * 1.0 / n)
        cbin_prob.append(np.sum(s[cbin], 0)[0] / tot)
        cbin_avg.append(np.mean(s[cbin], 0))
        cbin_count.append(len(cbin))
    cbin_prob = np.array(cbin_prob).ravel().reshape(-1,1)
    cbin_avg = np.array(cbin_avg).reshape(-1,1)
 #   print('cbin_prob','cbin_avg',cbin_prob,cbin_avg,cbin_prob.shape,cbin_avg.shape)
  #  bin_list = np.array(cbin_avg).reshape(-1,1)
    print('cbin_prob',cbin_prob.shape,cbin_prob)
    return cbin_prob,cbin_avg,bin_list
def standardization(data):
    data.reshape((-1,1))
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

def ShowChapter():
    # testname = 'tfidf_all'
    # testname = 'wordquery_all'
    #ShowResult(testname='wordquery_allv2')
    # chapter = u'8' #this is ok
    testname = 'wordquery_allv6ks'
    ranker = 'worddistv6ks'
    testname = 'wordquery_allv6ks'
    ranker = 'worddistv6ks'

    #   chapter = u'8'
    chapter = u'4.23.7'
    print('-------',testname,chapter)
    ShowChapterRankResult(testname,chapter)
 #   testname = 'wordquery_allv4'
 #   print('-------',testname,chapter)
 #   ShowChapterRankResult(testname,chapter)

def RunWordDist():
    testname ='worddist'
    ranker = 'worddist'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddist'
    return testscore
def RunWordDistV2():
    testname ='worddistv2'
    ranker = 'worddistv2'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv2'
    return testscore
def RunWordDistV3():
    testname ='worddistv3'
    ranker = 'worddistv3'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv2'
    return testscore
def RunWordDistV4():
    testname = 'worddistv4'
    ranker='worddistv4'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    return testscore
def RunWordDistV6():
    testname = 'worddistv6'
    ranker = 'worddistv6'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6'
    return testscore
def RunWordDistV66KS():
    testname = 'worddistv6ks'
    ranker = 'worddistv6ks'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks'
    return testscore

def RunWordDistV6Top2():
    testname = 'worddistv6top2'
    ranker = 'worddistv6top2'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6top2'
    return testscore
def RunWordDistBV7():
    testname = 'worddistbv7'
    ranker = 'worddistbv7'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistbv7'
    return testscore
def RunWordDistStop():
    testname ='worddist_stop'
    ranker = 'worddist_stop'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddist_stop'
    return testscore
def RunPrefixWordDist():
    testname ='ourprefix'
    ranker = 'ourprefix'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'ourprefix'
    return testscore

def RunPrefixWordDistStop():
    testname ='ourprefix_stop'
    ranker = 'ourprefix_stop'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'ourprefix_stop'
    return testscore

def RUNBM25():
    testname =  'BM25Okapi'
    ranker = 'BM25Okapi'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'BM25'
    return testscore

def RUNBM25L():
    testname = 'BM25L'
    ranker = 'BM25L'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'BM25L'
    return testscore

def RUNBM25Plus():
    testname = 'BM25Plus'
    ranker = 'BM25Plus'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'BM25P'
    return testscore

def RunTFIDF():
    testname ='tfidf'
    ranker = 'tfidf'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'tfidf'
    return testscore

def RunTFIDFStop():
    testname ='tfidf_stopword'
    ranker = 'tfidf_stopword'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'tfidf_stop'
    return testscore

def RunTFIEFStop():
    testname ='tfief_stopword'
    ranker = 'tfief_stopword'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'tfief'
    return testscore

def RunDTFIPFStop():
    testname ='dtfipf_stopword'
    ranker = 'dtfipf_stopword'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'DtfIpf'
    return testscore
def RunWordDistV6KS_DualSentRankDCD():
    testname = 'wordistv6_dcd_sentscore'
    ranker = 'wordistv6_dcd_sentscore'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'wordistv6_dcd_sentscore'
    return testscore
def dual_v6_exclusion_meannormclose_v2_reci():
    testname = 'dual_v6_exclusion_meannormclose_v2_reci'
    ranker = 'dual_v6_exclusion_meannormclose_v2_reci'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_reci'
    return testscore
def dual_v6_exclusion_meannormclose_v2_covr():
    testname = 'dual_v6_exclusion_meannormclose_v2_covr'
    ranker = 'dual_v6_exclusion_meannormclose_v2_covr'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_covr'
    return testscore
def dual_v6_exclusion_meannormclose_v2_covr_nodense():
    testname = 'dual_v6_exclusion_meannormclose_v2_covr_nodense'
    ranker = 'dual_v6_exclusion_meannormclose_v2_covr_nodense'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_covr_nodense'
    return testscore
def dual_v6_exclusion_meannormclose_v2_reci_nodense():
    testname = 'dual_v6_exclusion_meannormclose_v2_reci_nodense'
    ranker = 'dual_v6_exclusion_meannormclose_v2_reci_nodense'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_reci_nodense'
    return testscore
def dual_v6_exclusion_meannormclose_v2_reci_onlyclose():
    testname = 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose'
    ranker = 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose'
    return testscore
def dual_v6_exclusion_meannormclose_v2_covr_onlyclose():
    testname = 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose'
    ranker = 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose'
    return testscore
def dual_v6_exclusion_meannormclose_v2_reci_onlyself():
    testname = 'dual_v6_exclusion_meannormclose_v2_reci_onlyself'
    ranker = 'dual_v6_exclusion_meannormclose_v2_reci_onlyself'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_reci_onlyself'
    return testscore
def dual_v6_exclusion_meannormclose_v2_covr_onlyself():
    testname = 'dual_v6_exclusion_meannormclose_v2_covr_onlyself'
    ranker = 'dual_v6_exclusion_meannormclose_v2_covr_onlyself'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'dual_v6_exclusion_meannormclose_v2_covr_onlyself'
    return testscore
def RunWordDistV6KS_DualSentRankFCD():
    testname = 'wordistv6_fcd_sentscore'
    ranker = 'wordistv6_fcd_sentscore'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'wordistv6_fcd_sentscore'
    return testscore

def RunWordDistV6KS_DualSentRank(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore'
    ranker = 'worddistv6ks_dual_sentscore'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore'
    return testscore

def RunWordDistV6KS_DualSentRankNoExclusion(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_noexclusion'
    ranker = 'worddistv6ks_dual_sentscore_noexclusion'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore_noexclusion'
    return testscore
def RunWordDistV6KS_DualSentRankNoEven(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_noeven'
    ranker = 'worddistv6ks_dual_sentscore_noeven'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore_noeven'
    return testscore
def RunWordDistV6KS_DualSentRankNoDensReci(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_nodens_Reci'
    ranker = 'worddistv6ks_dual_sentscore_nodens_Reci'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore_nodens_Reci'
    return testscore

'''
        if version == 'dual_v6_noexclusion':
            cversion = 'sum'
            exclusion = 'no'
            d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,closetype='max',exclusion = exclusion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meanclose':
'''
def RunWordDistV6KS_DualSentRankMeanClose(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_meanclose'
    ranker = 'worddistv6ks_dual_sentscore_meanclose'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore_meanclose'
    return testscore
def RunWordDistV6KS_DualSentRankV1(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_v1'
    ranker = 'worddistv6ks_dual_sentscore_v1'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'worddistv6ks_dual_sentscore_v1'
    return testscore
def RunWordDistV6KS_DualSentRankPrefix(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_prefix'
    ranker = 'worddistv6ks_dual_sentscore_prefix'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdPrefix'
    return testscore
def RunWordDistV6KS_DualSentRankPrefixNoEven(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_prefixnoeven'
    ranker = 'worddistv6ks_dual_sentscore_prefixnoeven'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdNoEven'
    return testscore
def RunWordDistV6KS_DualSentRankPrefixNoDens(): #best-20200205
    testname = 'worddistv6ks_dual_sentscore_prefixnodens'
    ranker = 'worddistv6ks_dual_sentscore_prefixnodens'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdNoDens'
    return testscore
def RunWordDistV6KS_DualSentRankDirected():
    testname = 'worddistv6ks_directed_dual_sentscore'
    ranker = 'worddistv6ks_directed_dual_sentscore'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdDir'
    return testscore
def Runwordquery_allv4():
    testname = 'worddistv4'
    ranker = 'worddistv4'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdDir'
    return testscore

def RunWordDistV6KS_DualSentRankBackDirected(): #best-20200205
    testname = 'worddistv6ks_backdirected_sentscore_prefix'
    ranker = 'worddistv6ks_backdirected_sentscore_prefix'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdBackDir'
    return testscore

def RunDensSpanDenseEven():
    testname ='worddist_denseeven'
    #ranker = 'worddist_denscover'
    #ranker = 'worddist_cover'
    ranker = 'worddist_denseeven'
   # ranker = 'worddist_even'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdDensEven'
    return testscore
def RunDensSpanCover():
    testname = 'worddist_cover'
    # ranker = 'worddist_denscover'
    ranker = 'worddist_cover'
    # ranker = 'worddist_denseeven'
    # ranker = 'worddist_even'

    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdCover'
    return testscore
def RunDensSpanDenscover():
    testname = 'worddist_denscover'
    ranker = 'worddist_denscover'
    # ranker = 'worddist_cover'
    # ranker = 'worddist_denseeven'
    # ranker = 'worddist_even'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdDensEven'
    return testscore
def RunDensSpanEven():
    testname = 'worddist_even'
    #ranker = 'worddist_denscover'
    # ranker = 'worddist_cover'
    # ranker = 'worddist_denseeven'
    ranker = 'worddist_even'
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model'] = 'WdEven'
    return testscore

def RunMMR():
    testname = "mmr_maxdf"
    ranker = "mmr_maxdf"
    RunAllCh(testname=testname, ranker=ranker)
    testscore = ShowResult(testname=testname)
    testscore['model']='MMR'
    return testscore


def TestPlot():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("test.png")
    plt.show()
def RankAllChapterSentence(testname,survgenmethod):
    fname = output_dir + '/'+testname +'_wd_top_len.result.dict'
    allresult=sxpReadFileMan.LoadObject(fname)
    allchapter_sent_dict={}
    for ch, testinfo in allresult.items():
        print(ch,testinfo['title'])
     #   print(testinfo)
        sent_tops = RankChapterSentence(testname,testinfo, ch, survgenmethod)
        allchapter_sent_dict[ch]=sent_tops
    fname = output_dir + '/'+testname + '_'+survgenmethod+'_'+'allchapter_sent_dict.result.dict'
    sxpReadFileMan.SaveObject(allchapter_sent_dict,fname)

def RankChapterSentence(testname,testinfo,chpater,survgenmethod):


    # testinfo:
    # {'chname': '8.3', 'title': 'Asiya an evaluation toolkit\r', 'truth': [('CR6', 'Amigo et-al. 2005', '0074')], 'result': {'precision': 0.0, 'recall': 0.0, 'fscore': 0, 'jaccard': 0.0}, 'rankresult': [(59, '0059', 7.732764132345889, 'MEAD_ a platform for multidocument multilingual text summarization'), (44, '0044', 7.637370775510204, 'GraphSum: Discovering correlations among multiple terms for graph-based summarization'), (36, '0036', 7.482163455520166, 'Enhancing the Effectiveness of Clustering with Spectra Analysis'), (51, '0051', 7.480991840762236, 'Integrating importance, non-redundancy and coherence in graph-based extractive summarization'), (96, '0096', 7.434135479482766, 'Text summarization using a trainable summarizer and latent semantic analysis'), (31, '0031', 7.401016903103107, 'Document Summarization Based on Data Reconstruction'), (63, '0063', 7.389615629126119, 'Multi-document summarization based on two-level sparse representation model'), (41, '0041', 7.385117885951011, 'Fuzzy evolutionary optimization modeling and its applications to unsupervised categorization and extractive summarization'), (65, '0065', 7.366544230180594, 'Multi-document summarization exploiting frequent itemsets'), (16, '0016', 7.353331916250399, 'Automatic Detection of Opinion Bearing Words and Sentences'), (5, '0005', 7.33608024691358, 'A new sentence similarity measure and sentence based extractive technique for automatic text summarization'), (32, '0032', 7.319186179981635, 'Document summarization using conditional random fields'), (69, '0069', 7.292663262563827, 'NewsGist: A Multilingual Statistical News Summarizer'), (34, '0034', 7.279853379778249, 'Enhancing sentence-level clustering with ranking-based clustering framework for theme-based summarization'), (39, '0039', 7.265493119363532, 'FoDoSu: Multi-document summarization exploiting semantic analysis based on social Folksonomy'), (50, '0050', 7.263078512396694, 'Integrating clustering and multi-document summarization by bi-mixture probabilistic latent semantic analysis (PLSA) with sentence bases'), (106, '0106', 7.256840741583655, 'Using External Resources and Joint Learning for Bigram Weightingin ILP-Based Multi-Document Summarization'), (33, '0033', 7.250927194359985, 'Document summarization via guided sentence compression'), (73, '0073', 7.246243806276306, 'Predicting Salient Updates for Disaster Summarization'), (90, '0090', 7.244313743164474, 'Summarizing Email Conversations with Clue Words'), (110, '0110', 7.232675386444709, 'Weighted consensus multi-document summarization'), (107, '0107', 7.202208556503339, 'Using query expansion in graph-based approach for query-focused multi-document summarization'), (97, '0097', 7.160397907954664, 'TextRank_ bringing order into texts'), (42, '0042', 6.784758567810059, 'GA, MR, FFNN, PNN and GMM based models for automatic text summarization'), (14, '0014', 6.769455017301038, 'Assessing sentence scoring techniques for extractive text summarization'), (102, '0102', 6.68776397135337, 'Topic aspect-oriented summarization via group selection'), (68, '0068', 6.661811976809715, 'Multiple documents summarization based on evolutionary optimization algorithm'), (58, '0058', 6.643201410003675, 'MCMR: Maximum coverage and minimum redundant text summarization model'), (28, '0028', 6.63272679096454, 'Differential Evolution - A Simple and Efﬁcient Heuristic for Global Optimization over Continuous Spaces'), (71, '0071', 6.623505823546202, 'Opinion Mining and Sentiment Analysis'), (35, '0035', 6.6145224045968725, 'Enhancing the Effectiveness of Clustering with Spectra Analysi'), (38, '0038', 6.61011440339672, 'Fast and Robust Compressive Summarization with Dual Decomposition and Multi-Task Learning'), (7, '0007', 6.605081153161042, 'A text summarizer for Arabic'), (3, '0003', 6.56511080994898, 'A multi-document summarization system based on statistics and linguistic treatment'), (80, '0080', 6.555276920438957, 'ROUGE_ a package for automatic evaluation of summaries'), (0, '0000', 6.544226733780253, 'A complex network approach to text summarization'), (6, '0006', 6.5346093120129, 'A Survey of Text Summarization Extractive Techniques'), (2, '0002', 6.530537201953461, 'A language independent approach to multilingual text summarization'), (109, '0109', 6.522656323905023, 'WebInEssence_ a personalized web-based multidocument summarization and recommendation system'), (1, '0001', 6.501606596303195, 'A framework for multi-document abstractive summarization based on semantic role labelling'), (27, '0027', 6.499395833276237, 'Determinantal Point Processes for Machine Learning'), (104, '0104', 6.496924296982168, 'Topic Themes for Multi-Document Summarization'), (45, '0045', 6.494506640253359, 'Hybrid Algorithm for Multilingual Summarization of Hindi and Punjabi Documents'), (62, '0062', 6.4672666518155495, 'Multi-document abstractive summarization using ILP based multi-sentence compression.'), (94, '0094', 6.463662689448597, 'Syntactic Trimming of Extracted Sentences for Improving Extractive Multi-document Summarization'), (88, '0088', 6.461010179004967, 'Summarization of Multi-Document Topic Hierarchies using Submodular Mixtures'), (47, '0047', 6.456054854485141, 'Implementation and evaluation of evolutionary connectionist approaches to automated text summarization'), (66, '0066', 6.455924036281179, 'Multi-document summarization via budgeted maximization of submodular functions'), (4, '0004', 6.451603971361893, 'A neural attention model for abstractive sentence summarization'), (74, '0074', 6.4397378105390315, 'QARLA:A Framework for the Evaluation of Text Summarization Systems'), (72, '0072', 6.439102738184838, 'Opinosis: A Graph-Based Approach to Abstractive Summarization of Highly Redundant Opinions'), (21, '0021', 6.431331888019606, 'Building an Entity-Centric Stream Filtering Test Collection for TREC 2012'), (23, '0023', 6.421153630229971, 'Centroid-based summarization of multiple documents'), (64, '0064', 6.416658721229572, 'Multi-Document Summarization By Sentence Extraction'), (60, '0060', 6.405188590729969, 'Modeling Document Summarization as Multi-objective Optimization'), (43, '0043', 6.402147709840017, 'GistSumm_ a summarization tool based on a new extractive method'), (93, '0093', 6.401857638888889, 'SuPor: An Environment for AS of Texts in Brazilian Portuguese'), (67, '0067', 6.396924793849587, 'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs'), (75, '0075', 6.376974482294494, 'QCS: A system for querying, clustering and summarizing documents'), (26, '0026', 6.375707205824305, 'Deriving concept hierarchies from text'), (95, '0095', 6.371048032208732, 'System Combination for Multi-document Summarization'), (85, '0085', 6.3710163392503585, 'Sentence extraction system asssembling multiple evidence'), (87, '0087', 6.362447970863684, 'Single-Document Summarization as a Tree Knapsack Problem'), (29, '0029', 6.361295776136093, 'Document clustering and text summarization'), (86, '0086', 6.360962524404375, 'Single-document and multi-document summarization techniques for email threads using sentence compression'), (56, '0056', 6.3486879561099325, 'Learning with Unlabeled Data for Text Categorization Using Bootstrapping and Feature Projection Techniques'), (99, '0099', 6.340772312129467, 'The anatomy of a large-scale hypertextual Web search engine'), (46, '0046', 6.340578803611267, 'Image collection summarization via dictionary learning for sparse representation'), (12, '0012', 6.340078125, 'Applying regression models to query-focused multi-document Summarization'), (8, '0008', 6.332982882340332, 'Abstractive Multi-Document Summarization via Phrase Selection and Merging'), (91, '0091', 6.332799286995087, 'Summarizing Emails with Conversational Cohesion and Subjectivity'), (70, '0070', 6.32318002676978, 'One Story, One Flow: Hidden Markov Story Models for Multilingual Multidocument Summarization'), (57, '0057', 6.322943286614498, 'Long story short - Global unsupervised models for keyphrase based meeting summarization'), (37, '0037', 6.320845582000113, 'Event graphs for information retrieval and multi-document summarization'), (15, '0015', 6.319254412056316, 'Automated Summarization Evaluation with Basic Elements'), (52, '0052', 6.314685547688463, 'Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression'), (78, '0078', 6.314384765624999, 'Reader-aware multi-document summarization via sparse coding'), (53, '0053', 6.310630341880342, 'Large-margin learning of submodular summarization models'), (108, '0108', 6.307430844114923, 'Using Topic Themes for Multi-Document Summarization'), (17, '0017', 6.307106025819564, 'Automatic generic document summarization based on non-negative matrix factorization, Information Processing and Management'), (98, '0098', 6.290157229946054, 'TextTiling: Segmenting Text into Multi-paragraph Subtopic Passages'), (19, '0019', 6.288075769578995, 'Biased LexRank_ Passage retrieval using random walks with question-based priors'), (11, '0011', 6.287489149305555, 'Analyzing the use of word graphs for abstractive text summarization'), (24, '0024', 6.277564482465407, 'Combining Syntax and Semantics for Automatic Extractive Single-document Summarization'), (76, '0076', 6.270711264898116, 'Ranking with Recursive Neural Networks and Its Application to Multi-document Summarization'), (100, '0100', 6.252403619568291, 'The automatic creation of literature abstracts'), (30, '0030', 6.248262524644623, 'Document concept lattice for text understanding and summarization'), (89, '0089', 6.237769371659604, 'Summarization System Evaluation Revisited: N-Gram Graphs'), (83, '0083', 6.230124457553925, 'Semantic graph reduction approach for abstractive Text Summarization'), (92, '0092', 6.2248052609866775, 'SUMMARIZING TEXT by RANKING TEXT UNITS ACCORDING to SHALLOW LINGUISTIC FEATURES'), (20, '0020', 6.219928146569073, 'Building a Discourse-Tagged Corpus in the Framework of Rhetorical Structure Theory'), (54, '0054', 6.219269402279176, 'Learning Summary Prior Representation for Extractive Summarization'), (10, '0010', 6.217870218406767, 'An Extractive Text Summarizer Based on Significant Words'), (61, '0061', 6.18011836628512, 'Modeling Local Coherence: An Entity-based Approach'), (22, '0022', 6.169046977245687, 'Centering: A Framework for Modeling the Local Coherence of Discourse'), (84, '0084', 6.1125108131487895, 'Semantic Role Labelling with minimal resources: Experiments with French'), (49, '0049', 6.09940138626339, 'Information Extraction by an Abstractive Text Summarization for an Indian Regional Language'), (101, '0101', 6.059917355371901, 'The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries'), (48, '0048', 6.058926564875405, 'Improving the Estimation of Word Importance for News Multi-Document Summarization'), (40, '0040', 6.050426136363637, 'Framework for Abstractive Summarization using Text-to-Text Generation'), (25, '0025', 5.960007304601899, 'DEPEVAL(summ)_ dependency-based evaluation for automatic summaries'), (77, '0077', 5.7529218407596785, 'Re-evaluating Automatic Summarization with BLEU and 192 Shades of ROUGE'), (9, '0009', 5.642722117202268, 'Advances in Automatic Text Summarization'), (79, '0079', 4.744461540556365, 'Revisiting readability_ a unified framework for predicting text quality'), (82, '0082', 3.6746776323851797, 'Selecting a feature set to summarize texts in brazilian portuguese'), (55, '0055', 3.4094921514312095, 'Learning the parts of objects by non-negative matrix factorization'), (105, '0105', 3.0000438577255384, 'Unsupervised Clustering by k-medoids for Video Summarization'), (103, '0103', 2.9454761368522346, 'Topic keyword identification for text summarization using lexical clustering'), (81, '0081', 2.862244498394549, 'Scene Summarization for Online Image Collections'), (18, '0018', 2.816166428199792, 'Beyond keyword and cue-phrase matching: A sentence-based abstraction technique for information extraction'), (13, '0013', 1.8181818181818181, 'Aspects of sentence retrieval')]}
    print('----------chapter-------',testinfo['title'],chpater)
    chid = testinfo['chname']
    chtile =testinfo['title']
    keywords = chtile.split('\s')
    print('----------truth----------')
    for each in testinfo['truth']:
        print(each)

    print('----------rank sentence for the chapter from paper rank result----------')
    papersent_dict = {}
    for  (id,fid, score, title)  in testinfo['rankresult']:
        print( (id,fid, score, title) )
        paper_sent_result ={}
        if survgenmethod =='sentsim':
            paper_sent_result=sxpWordDist.RankOnePaper(fid,chid,keywords,survgenmethod)
        papersent_dict[fid]=paper_sent_result['ranksent']
    return papersent_dict

def LoadChapterSentenceRank(fid, chid,testname,survgenmethod):
    fname = output_dir + '/'+testname + '_'+survgenmethod+'_'+'allchapter_sent_dict.result.dict'
    allchapter_sent_dic=sxpReadFileMan.LoadObject(fname)
    return allchapter_sent_dic[chid][fid]
def main(maincmd=""):
    if maincmd:
        cmd = maincmd
    else:
        #  cmd = 'RunWordDistV6KS_DualSentRank'
       # cmd = 'BuilAllTopk'
        #cmd = 'RunDTFIPF'
        # cmd = 'RunTFIEF'
        # cmd = 'ShowDualGenSurv'
        # cmd = 'RunDens'
        #cmd ='RUNBM25'
        #cmd = 'RunWordDistV6KS_DualSentRankDirected'
        #cmd = 'RunWordDistV6KS_DualSentRank'
        cmd = 'BuilAllTopk'
        # cmd = 'RunMMR'
    if cmd =='RankAllChapterSentence':
        testname = 'wordquery_allv6'
        survgenmethod = 'sentsim'

        RankAllChapterSentence(testname,survgenmethod)
    if cmd == 'RunWordDist':
        RunWordDist()
        RunWordDistStop()
    if cmd == 'RunWordDistV2':
        #RunWordDist()
        RunWordDistV2()
    if cmd == 'RunWordDistV4':
        RunWordDistV4()
    if cmd == 'RunWordDistV6':
        RunWordDistV6() #20200808 the best score
        # RunWordDistV6Top2()
    if cmd == 'RunWordDistV6KS':
        RunWordDistV66KS() #20200808 the best score remove keyword query's stopwords
    if cmd == 'RunWordDistV6KS_DualSentRank':
        RunWordDistV6KS_DualSentRank()  # 20200808 the best score remove keyword query's stopwords
    if cmd == 'RunWordDistV6KS_DualSentRankDirected':
        RunWordDistV6KS_DualSentRankDirected()
    if cmd == 'RunWordDistBV7': #not good even than v4 20200821
        RunWordDistBV7()

    if cmd == 'ShowWDResult':
        ShowResult(testname='wordquery_all')
        ShowResult(testname='tfidf_all')
    if cmd == 'ShowRankResult':
        ShowRankResult(testname='wordquery_all')
    #    ShowRankResult(testname='tfidf_all')
    if cmd =='RunPrefixWordDist':
     #   RunPrefixWordDist()
        RunPrefixWordDistStop()
    if cmd == 'RunTFIDF':
        #RunTFIDF()
        RunTFIDFStop()
    if cmd == 'RUNBM25':
        RUNBM25()
     #   RUNBM25L()
     #   RUNBM25Plus()
    if cmd == 'RunTFIEF':
        #RunTFIDF()
        RunTFIEFStop()
    if cmd == 'RunDTFIPF':
        #RunTFIDF()
        RunDTFIPFStop()
    if cmd == 'RunDensSpanCover':
        RunDensSpanCover()
    if cmd == 'RunMMR':
        RunMMR()
    if cmd == 'TestPlot':
        TestPlot()
    if cmd == 'ShowChapter':
        # ShowAllChapter(testname = 'wordquery_allv6')
        ShowChapter()
    if cmd == 'listchaptertitle':
        ShowAllChapterTitle('wordquery_allv6')
    if cmd == 'ShowAllChapter':
        ShowAllChapter('wordquery_allv6ks')
    if cmd == 'BuilAllTopk':
     #   GetSurveyChapterText()
        subcmd = 'closeness'

     #-----closeness ranking sent study
        if subcmd == 'closeness':
            testname = 'wordquery_allv6ks_dual_sentrank' # the best one for all 20201111 study
            # topkmethod = 'opt'
            #topkmethod = 'orig' #the best topk selection algorith: 20201111
            topkmethod = 'LR'
            #topkmethod = 'opt_num'
            # topkmethod = 'opt_var' #the current best, for selecting num of doc and num of sents 20201107
     #----tfidf sent rank study
        if subcmd == 'tfidf':
            #testname = 'dtfipf_all_stop'
            testname = 'tfidf_BM25'
            # topkmethod = 'orig'
            topkmethod = 'LR'

        BuilAllTopk(testname,topkmethod,compress_factor=0.01)
    if cmd == 'ShowDualGenSurv':
        testname = 'wordquery_allv6ks_dual_sentrank'
        topkmethod = 'LR'
        ShowGenSurv(testname,topkmethod)
if __name__ == '__main__':
    main()
