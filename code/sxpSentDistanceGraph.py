__author__ = 'a'
from numpy import *
import numpy as np
from scipy.sparse import csr_matrix
import re
import sxpFenciMakeTFIDF
import sxpJudgeCharacter
import networkx as nx
import sxpPageRank
class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_id_dict ={}
    section_list = []
    paraset = []
    whole_sectitle = ''
    whole_text = ''
    keycount = None
    para_tfidf = None
    sentence_tfidf = None
    sentenceset = []
    context_set = []
    d_c = None
    c_p = None
    p_s = None
    s_k = None
    t_s = None #context - sentence
    p_t = None #paragraph - context
    g = None
    def __init__(self):
        self.fname = ''
        self.title = ''
        self.abstract = ''
        self.relatedwork = ''
        self.conclusion = ''
        self.reference = ''
        self.section_id_dict ={}
        self.section_list = []
        self.paraset = []
        self.whole_sectitle = ''
        self.whole_text = ''
        self.keycount = None
        self.para_tfidf = None
        self.sentence_tfidf = None
        self.sentenceset = []
        self.d_c = None
        self.c_p = None
        self.p_s = None
        self.s_k = None
        self.s_s = None
        self.g = None
        self.context_set = []
        self.t_s = None
        self.p_t = None
class MyDiffGraph:
    #1 means with stopwords
    #2 means without stopwords
    def __init__(self, sent_list, remove_stopwords=True, iteration_times=40):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.c_c = None
        self.w = []
        self.s = []
        self.p = []
        self.c = []
        self.idx_w = []
        self.idx_s = []
        self.idx_p = []
        self.idx_c = []
        self.times = iteration_times
        self.words = []
        self.alpha_beta=[0.8,0.2]
        self.text = self.BuildTextGraph(sent_list,removestop=remove_stopwords,addseq = 0,undirect=1)

        self.iterationss()
        self.rank_weight()

    def OutputAllRankSentence(self,wlen=500):
        print('output ranked sent',len(self.sentenceset))
        sent_txt_set = []
        i = 0
        n,r = self.idx_s.shape
        t = 0
        for i in range(n):
            sent = self.sentenceset[self.idx_s[i, 0]]
            print(i,sent)
            sent_txt_set.append(sent)
            if t > wlen:
                break
            t = t + len(re.split('\s+',sent.strip()))
        print('finished ranked')
        return sent_txt_set
    def OutputAllRankSentenceByDiff(self,wlen=500,simr=0.4):
        print('output ranked sent',len(self.sentenceset))
        sent_txt_set = []
        i = 0
        n,r = self.idx_s.shape
        t = 0
        skiped = 0
        for i in range(n):
            sent = self.sentenceset[self.idx_s[i, 0]]
            print(i,sent)
            if self.simsentgroup(sent,sent_txt_set,simr):
                skiped +=1
                continue
            sent_txt_set.append(sent)
            if t > wlen:
                break
            t = t + len(re.split('\s+',sent.strip()))
        print('finished ranked','skiped',skiped)
        return sent_txt_set

    def simsentgroup(self,sent, sent_txt_set, simr=0.4):
        ds = []
        for each in sent_txt_set:
            sim = sxpJudgeCharacter.jaccard_similarity(sent, each)
            ds.append(sim)
        sim = np.mean(ds)
        if sim >= simr:
            return True;
        return False
    def rank_weight(self):

        self.idx_s = argsort(array(-self.s), axis=0)


    @staticmethod
    def normalize(w):
        assert(sum(w) > 0)
        w = w / sum(w)
        return w

    def update_sentence_weight(self, w):
        s = self.w_s.T * w
        s = self.normalize(s)
        return s

    def update_paragraph_weight(self, s):
        p = self.s_p.T * s
        p = self.normalize(p)
        return p

    def update_section_weight(self, p):
        sec = self.c_c * self.p_c.T * p
        sec = self.normalize(sec)
        return sec

    def update_word_weight(self, w, s, p, sec):
        w = self.w_s * s + self.w_s * self.s_p * p\
            + self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * s
       # w = self.w_s * s + self.w_s * self.s_p * p #this is the mostly used model
        w = self.normalize(w)
        return w

    def iteration(self, w):
        for i in range(self.times):
            s = self.update_sentence_weight(w)

            p = self.update_paragraph_weight(s)

            c = self.update_section_weight(p)

            w = self.update_word_weight(w, s, p, c)

        self.w = w
        self.s = s
        self.p = p
        self.c = c
    def iterationss(self):
        self.s = sxpPageRank.pagerank(self.s_s)
    def iterateiondsds(self):
        self.ds = sxpPageRank.pagerank(self.ds_ds)
    def rankbydiff(self,use_diff=3,wlen=500, simr = 0.4):
        if use_diff == 'simgraph':
           self.iterationss()
           self.idx_s = argsort(array(-self.s), axis=0)
           return self.OutputAllRankSentence(wlen=wlen)
         #  return self.OutputAllRankSentenceByDiff(wlen=wlen)
        if use_diff == 'diffgraph':
           self.iterateiondsds()
           self.idx_s = argsort(array(-self.ds), axis=0)
           #return self.OutputAllRankSentence(wlen=wlen)
         #  return self.OutputAllRankSentenceByDiff(wlen=wlen)
        if use_diff == 'diffsimgraph':
            print('iterate ss')
            self.iterationss()
            print('iterate dsds')
            self.iterateiondsds()
            self.ts = self.s + self.ds
            print('sort s')
            self.idx_s = argsort(array(-self.ts), axis=0)
            return self.OutputAllRankSentence(wlen=wlen)
           #return self.OutputAllRankSentenceByDiff(wlen=wlen)
        if use_diff == 'simdiffskip':
            self.iterationss()
            self.idx_s = argsort(array(-self.s), axis=0)
            return self.OutputAllRankSentenceByDiff(wlen=wlen,simr=simr)
    def iterationws(self):
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        N = M.shape[0]
        alpha, max_iter, S_S, x, per, dangling_weights, is_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=self.alpha_beta[0]
        wpara =self.alpha_beta[1]
        for _ in range(max_iter):
            xlast = x.copy()
            sw = sum(xlast.T[is_dangling])
            x = alpha * xlast * S_S + alpha * sw * dangling_weights + (1 - alpha) * per
            s = self.w_s.T * w
         #   x = 0.5 * x + 0.5 * s.T
            x = spara * x + wpara * s.T
            s = x.T
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x - xlast))
            if err < N * tol:
                break
        self.w = w.T
        self.s = x.T
        print((self.s.shape))
    def BuildTextGraph(self, sentences,removestop=True,addseq = 0,undirect=1):

        self.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentences,removestop)
        self.sentenceset = sentences
    #***************************************************************
    #****************Now we try to build several matrix for graphs can be
    #               extracted from sxptxt
    #***************************************************************
        print('we begin to build matrix')

        ss = len(self.sentenceset)
        ks = len(self.sentence_tfidf.word)

        print(ss, ks)

        ns = len(sentences)
        m = np.zeros((ns, ns), dtype=np.float)
        g = nx.Graph()

        if addseq > 0:
            for i in range(len(sentences) - 1):
                if addseq == 1:
                    m[i + 1, i] = 1
                    g.add_edge(i + 1, i, weight=1)
                if addseq == 2:
                    m[i, i + 1] = 1
                    g.add_edge(i, i + 1, weight=1)
                if addseq == 3:
                    m[i + 1, i] = 1
                    m[i, i + 1] = 1
                    g.add_edge(i + 1, i, weight=1)
                    g.add_edge(i, i + 1, weight=1)
        tfactor = log(len(sentences))
        for i in range(len(sentences) - 1, -1, -1):
            for j in range(i, -1, -1):
                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i], sentences[j])
                d = j - i
                if d == 0:
                    d = 1
                d = (tfactor - log(abs(d))) / tfactor
              #  dist = jaccard * d
                dist = jaccard
                m[j, i] = dist  # note that j-i is good than i-j and
                g.add_edge(j, i, weight=dist)
                if undirect == 1:
                    # dist =  jaccard
                    m[i, j] = dist
                    g.add_edge(i, j, weight=dist)


        #fourth, building s-k matrix
        print('s_k matrix')
        self.s_k =csr_matrix(self.sentence_tfidf.tfidf)
        self.s_s = np.matrix(m)
        self.ds_ds = 1- self.s_s
        self.g = g
        self.words = self.sentence_tfidf.word
        return self.s_s


def BuildSentGraph(sentences, sim='dis', addseq=0, undirect=1):
    ns = len(sentences)
    m = np.zeros((ns, ns), dtype=np.float)
    if addseq > 0:
        for i in range(len(sentences) - 1):
            if addseq == 1:
                m[i + 1, i] = 1

            if addseq == 2:
                m[i, i + 1] = 1

            if addseq == 3:
                m[i + 1, i] = 1
                m[i, i + 1] = 1
    for i in range(len(sentences) - 1, -1, -1):
        for j in range(i, -1, -1):
            dist = sxpJudgeCharacter.jaccard_similarity(sentences[i], sentences[j])
            if sim == 'dis':
                dist = 1- dist
            d = j - i
            if d == 0:
                d = 1
            m[j, i] = dist  # note that j-i is good than i-j and
            if undirect == 1:
                # dist =  jaccard
                m[i, j] = dist

    # fourth, building s-k matrix
    print('s_k matrix')
    s_s = np.matrix(m)
    #ds_ds = 1 - self.s_s

    return s_s
def PreparePageRankMatrix(M, alpha=0.85, max_iter=100, p=None, alreadysym=True):

    # note M is a matrix object, and row is out degree
    #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M, mode='merg')
    N = M.shape[0]
    W = NormalizeMatrix(M, 1)
    #    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W, axis=axis_id))

    x = matrix(np.ones((N, 1), dtype=np.float) * 1.0 / N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p = p.T
    #    max_iter = 20
    tol = 1.0e-6
    i = 0
    return alpha, max_iter, W, x, p, dangling_weights, is_dangling


def MyPageRankMatT(M, alpha=0.85, max_iter=100, p=None, alreadysym=True):
    # note M is a matrix object, and row is out degree
    #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M, mode='merg')
    N = M.shape[0]
    W = NormalizeMatrix(M, 1)
    #    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W, axis=axis_id))

    x = matrix(np.ones((N, 1), dtype=np.float) * 1.0 / N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p = p.T
    #    max_iter = 20
    tol = 1.0e-6
    i = 0
    for _ in range(max_iter):
        xlast = x.copy()
        sw = sum(xlast.T[is_dangling])
        x = alpha * xlast * W + alpha * sw * dangling_weights + (1 - alpha) * p
        ##        if i == 0:
        ##            print sw
        ##            print alpha
        ##
        ##            print x
        i = i + 1
        #        x = alpha * M*x  + (1 - alpha) * p
        err = sum(abs(x - xlast))
        if err < N * tol:
            return x, W
    return x, W
def FindDanglingNodes(M,axis_id = 1):
    S = M.sum(axis=1)
    sel = np.where(S==0)
    return sel[0]
def NormalizeArrayMatrix(M,axis_id=1):
    S = np.sum(M,axis = axis_id)
    S[S != 0] = 1.0 / S[S != 0]
    Q = np.diag(S)
    M = np.dot(M,Q)
    return M
def NormalizeMatrix(M, axis_id = 1):
    S = M.sum(axis=1)
    sel = np.where(S==0)
    S[sel] = 1
    rown = M.shape[0]
    nm = M.copy()
    for r in range(rown):
        nm[r,:] = nm[r,:]/S[r]
    return nm
def MakeSymmetricMatrix(M,mode='half'):
    if mode == 'half':
        s = (M+M.T)/2
    if mode == 'merg':
        s = M.T.copy()
        nr = s.shape
        for index,x in np.ndenumerate(s):
            if s[index] ==0:
                s[index] = M[index]
            elif M[index] == 0:
                s[index] = s[index]
            else:
                s[index] = (s[index] + M[index])/2.0


    return s
def NormalizeMatrixFalse(M, axis_id=1):
    S = matrix(np.sum(M,axis = axis_id))
    sel = np.where(S!=0)
    S[sel] = 1.0 / S[sel]
    Q = np.diagflat(S.T)
    M = M*Q
    return M

def UpdateNormalizeDanglingMat(M):
    C = matrix(M)
    axis_id=1
    S = matrix(np.sum(C,axis = axis_id))
    colnum = C.shape[1]
    danglenodes = np.where(S == 0.0)
    nd = danglenodes[1].shape[1]
    if nd is None:
        return C
    st = matrix(np.ones((nd,colnum), dtype=np.float)*1.0/colnum)
    C[danglenodes[0],:] = st
    return C


def TestPickle():
 #   pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
 #   pk = r'E:\pythonworknew\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_3.pk'

    model= MyDiffGraph(pk)
    topksent = 10
    tops = model.OutPutTopKSent(topksent,1,-1)
    i = 0
    for eachs in tops:
        print('-----------------')
        print(i, eachs)
        i = i + 1
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    TestPickle()