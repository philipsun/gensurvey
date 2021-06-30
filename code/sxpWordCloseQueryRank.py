
import sxpSegSentWord
from scipy import *
import re
from sxpComputeCloseDist import *
from numpy import argsort
from nltk.corpus import stopwords
import sxpJudgeCharacter

def stop_words():
    sw = stopwords.words("english")
    return sw

global_stopwords= stop_words()
def queryrank(keywordseq,prefix, sent_list,wdlen = 250,simr = 0.4,removestop=True,groupsim=True,selectbydiff='NO',version = 'dual_v6'):

    newnk = ProcessKeyword(keywordseq, prefix, removestop=removestop)
    print('keyword to be query', newnk)

    wd_dist,sent_dist_dict = sxpSegSentWord.dualwordsentposdist(newnk, sent_list)
      #  print('word dist',wd_dist)
        # score = computeworddistscore(keywordseq, wd_dist)
    nl = len(sent_list) / 1.0
    # score = computecloseness(nk, wd_dist,nl)
#    score = computeclosenesstwo(newnk, wd_dist, nl,version=version) #only score of paper, 20200808 the best one
  #  version = 'dual_v6'
    print('-----this ranking dual sentence and word,version = dual_v6---')
    score,dual_sent_score = dualcomputeclosenesstwo(newnk, wd_dist, nl,version=version)
    #score is for the rank of current doc, and dual_sent_score is for the score of all sents in the current doc
    #

    idx_sent = list(argsort(-dual_sent_score, axis=0,kind='mergesort',).flat)
    ranked_sent = [sent_list[idx] for idx in idx_sent]
    sent_rank_dict= {}
    sent_rank_dict['doc_score']=score
    sent_rank_dict['sent_score']=dual_sent_score
    sent_rank_dict['ranked_sent'] = ranked_sent
    sent_rank_dict['idx_sent'] = idx_sent
    if selectbydiff == 'YES':
        sent_txt_set, top_idx=OutputAllRankSentenceByDiff(idx_sent,sent_list,wdlen,simr,groupsim)
    else:
        #sent_txt_set = ranked_sent
        #top_idx = idx_sent
        sent_txt_set, top_idx=OutputBoundTopk(ranked_sent, idx_sent, wdlen)
    sent_rank_dict['topsent']=sent_txt_set
    sent_rank_dict['topidx'] = top_idx
    sent_rank_dict['rawtopscore']=dual_sent_score[top_idx,0]
    sent_rank_dict['topscore'] = normalize(dual_sent_score[top_idx,0])
    return sent_rank_dict
def OutputBoundTopk(sent_list,idx_sent,wdlen):
    select = []
    topk_idx = []
    s = 0
    for i,each in enumerate(sent_list):
        wd = re.split('\s+',each)
        for eachw in wd:
            ws = eachw.strip()
            if len(ws)==0:
                continue
            if ws in ['.',',',':',"'",'"']:
                continue
            s = s + 1
        if s > wdlen:
            break
        select.append(each)
        topk_idx.append(idx_sent[i])
    return select,topk_idx
def normalize(score):
    a = np.array(score).reshape(-1,1)
    r = np.sum(a,0)
    if r == 0:
        r = 1
    a = a /r
    return a

def OutputAllRankSentenceByDiff(idx_s,sentenceset,wlen=500,simr=0.4,groupsim=True):
    print('output ranked sent',len(sentenceset))
    sent_txt_set = []
    i = 0
    n = len(idx_s)
    t = 0
    skiped = 0
    top_idx = []
    for i in range(n):
        sent = sentenceset[idx_s[i]]
        if t > wlen:
            break
        print(i,sent)
        if groupsim == False and simsent(sent,sent_txt_set,simr):
            skiped +=1
            continue
        if groupsim and simsentgroup(sent,sent_txt_set,simr):
            skiped +=1
            continue
        sent_txt_set.append(sent)
        top_idx.append(idx_s[i])

        t = t + len(re.split('\s+',sent.strip()))
    print('finished ranked','skiped',skiped)
    return sent_txt_set,top_idx
def simsent(sent,sent_txt_set,simr=0.4):
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent,each)
        if sim>simr:
            return True
    return False
def simsentgroup(sent,sent_txt_set,simr=0.4):
    ds = []
    for each in sent_txt_set:
        sim = sxpJudgeCharacter.jaccard_similarity(sent,each)
        ds.append(sim)
    sim = np.mean(ds)
    if sim >= simr:
        return True;
    return False
def ProcessKeyword(keywordseq,prefix=[],removestop=False):
    nk = []

    for each in keywordseq:
        sk = re.split('\s+', each)
        for eachw in sk:
            if len(eachw.strip()) == 0:
                continue
            if removestop:
                if eachw in global_stopwords:
                    continue
            g = re.findall('(\w+)',eachw)
            for w in g:
                if w in ['what','how','why','describe']:
                    continue
                if len(w.strip())<=1:
                    continue;
                if w.lower() not in nk:
                    nk.append(w.lower())
    newnk = []
    for pk in prefix:
        newnk.append(pk)
    for pk in nk:

        lpk = pk.lower()
        if lpk == pk:
            s = re.split('\-', pk)
            hs = " ".join(s)
            newnk.append(hs)
        else:
            #newnk.append('({0}|{1})'.format(pk,lpk))
            s = re.split('\-', lpk)
            hs = " ".join(s)
            newnk.append(hs)
    return newnk
