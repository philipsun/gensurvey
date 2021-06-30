__author__ = 'a'
from sxpPackage import *
import networkx as nx
import numpy as np
from numpy import *
import re
import sxpReadFileMan

class HybridGraph:
    def __init__(self, pickle_path, choice=2, iteration_times=20):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.t_p = None
        self.s_t = None
        self.w = []
        self.s = []
        self.p = []
        self.c = []
        self.t = [] #context
        self.idx_w = []
        self.idx_s = []
        self.idx_p = []
        self.idx_c = []
        self.idx_t = [] #sorted context
        self.times = iteration_times
        self.words = []
        self.s_s = []
        self.section2sentence_id_list = {}
        self.idx_s = []
        self.text = LoadSxptext(pickle_path)

        if choice == 1:
            self.get_parameters_with_stopwords()
        elif choice == 2:
            self.get_parameters_without_stopwords()

        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T
        self.RankSentence()
     #   self.iteration(w, s)
     #   self.rank_weight()

        self.ordered_sentence_id_set()

    def page_rank(self, pickle_path):
        g = create_graph(pickle_path)
        pr = nx.pagerank(g)
        self.idx_s = list(argsort(list(pr.values())))
        self.idx_s.reverse()
    def get_parameters_with_stopwords(self):
        self.words = self.text.sentence_tfidf.word
        # import relation matrix
        self.w_s = matrix(self.text.s_k.toarray()).T
        #self.w_s = matrix(self.text.sentence_tfidf.ct.toarray()).T #for version one
        self.s_p = matrix(self.text.p_s.toarray()).T
        self.p_c = matrix(self.text.c_p.toarray()).T
        self.t_p = matrix(self.text.p_t.toarray()).T
        self.s_t = matrix(self.text.t_s.toarray()).T

#build graph between sentences
    def RankSentence(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        g = np.ones((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                g[i,j]=jaccard
                g[j,i]=jaccard
        self.s_s = matrix(g)

        g = create_graph(self.text)
        pr = nx.pagerank(g)
        self.idx_s = list(argsort(list(pr.values())))
        self.idx_s.reverse()
        print(self.idx_s)

        pr = MyPageRankMatT( self.s_s)
        self.idx_s = argsort(pr.flatten()).tolist()[0]
        self.idx_s.reverse()
        print(self.idx_s)
    def get_parameters_without_stopwords(self):
        self.get_parameters_with_stopwords()
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        stopwords = [line.strip() for line in lines]
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
               and re.match(r'^[a-zA-Z]+$', self.words[i]) is not None]
        new_w_s = []
        for i in idx:
            new_w_s.append(array(self.w_s[i, :]).tolist())
        new_w_s = matrix(array(new_w_s))
        new_words = [self.words[i] for i in idx]
        self.words = new_words
        self.w_s = new_w_s
    def rank_weight(self):
        self.idx_w = argsort(array(-self.w), axis=0)
     #   self.idx_s = argsort(array(-self.s), axis=0)
        self.idx_p = argsort(array(-self.p), axis=0)
        self.idx_c = argsort(array(-self.c), axis=0)
        self.idx_t = argsort(array(-self.t), axis=0)

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
        sec_titles = []
        for sec in self.text.section_list:
            self.section2sentence_id_list[sec.title] = []
            sec_titles.append(sec.title)
        for sentence in ranked_sentences:
            section_tag = self.text.paraset[sentence.id_para].section_title
            #section_id = text.paraset[sentence.id_para].id_sec
            if section_tag != '' and section_tag in sec_titles:
                self.section2sentence_id_list[section_tag].append(sentence.id)
    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        if useabstr == 1:
            abstractlen = len(self.text.abstract)
        if useabstr == 2:
            abstractlen = len(self.text.conclusion)
        wordlen = 0
        for sentence in ranked_sentences:
            if  wordlen>= abstractlen and maxwords == -1:
                break
            if len(sentence.sentence_text)<=1:
                continue
            if i >= topk and maxwords == 0:
                break;
            wordlen = wordlen + len(sentence.sentence_text)
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set

    @staticmethod
    def normalize(w):
        assert(sum(w) > 0)
        w = w / sum(w)
        return w

    def update_sentence_weight(self, w, s):
     #   s = self.w_s.T * w + self.s_s*s
        s = self.s_s*s
        #s = self.normalize(s)
        return s

    def update_paragraph_weight(self, s):
        p = self.s_p.T * s
        p = self.normalize(p)
        return p
    def update_context_weigth(self, s):
        t = self.s_t.T * s
        t = self.normalize(t)
        return t

    def update_paragraph_weight_bycontext(self, t):
        p = self.t_p.T * t
        p = self.normalize(p)
        return p

    def update_section_weight(self, p):
        sec = self.p_c.T * p
        sec = self.normalize(sec)
        return sec

    def update_word_weight(self, w, s, p, sec):
        #w = self.w_s * s + self.w_s * self.s_p * p\
           # + self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * s
        w = self.w_s * s + self.w_s * self.s_p * p
        w = self.normalize(w)
        return w
    def update_word_weight_bycontext(self, w, s, t,p):
#        w = self.w_s * s + self.w_s * self.s_t * self.t_p * p #this is the mostly used one in previous experiments
        w = self.w_s * s + self.w_s*self.s_t*t + self.w_s * self.s_t * self.t_p * p #this is the latest one that incorporate context

        w = self.normalize(w)
        return w


    def iteration(self, w, s):
        for i in range(self.times):
            s = self.update_sentence_weight(w, s)

            t = self.update_context_weigth(s)

            p = self.update_paragraph_weight_bycontext(t)

            c = self.update_section_weight(p)

            w = self.update_word_weight_bycontext(w, s, t, p)

        self.w = w
        self.s = s
        self.p = p
        self.c = c
        self.t = t
    def SentenceIteration(self,w,s):
        for i in range(self.times):
            s = self.s_s*s

# input : path, file_name
# output: matrix
def create_graph(text):
#    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    g = nx.Graph()
    for sent in sentences:
        g.add_node(sent.id)
    for i in range(len(sentences)):
        for j in range(i, len(sentences)):
            sent_a = set(sentences[i].sentence_text.split())
            sent_b = set(sentences[j].sentence_text.split())
            common_word = sent_a.intersection(sent_b)
            if not common_word:
                continue
            jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
            g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
            g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)
    return g
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
        s = M.T
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
def TestNormalizeArrayMatrix(M,axis_id):
    S = np.sum(M,axis = axis_id).T
    print(S)
    print(S.shape)
    sel = (S!=0).flatten()
    print(sel)
    print(sel.shape)
    S[sel] = 1.0 / S[sel]
    Q = np.diag(S)
    print(Q)
    M = np.dot(M,Q)
    S = np.sum(M,axis = axis_id)
    print(S)
    return M
def TestMatrix():
  #  g = np.ones((ns,ns), dtype=np.float)
    m = np.random.rand(3,3)
    m = [[1.0,2.0,3.0],
         [1.0,2.0,3.0],
         [1.0,2.0,3.0]]
    v = np.random.rand(3,1)
    m = m
    print(v)
    pv= m*v
    print('p*v:')
    print(pv)
    print(m)
    print(TestNormalizeArrayMatrix(m,0)) #0 for column normalization, 1 for row normalization
def TestNormalizeMatrix():
    v = matrix(np.random.rand(3,1))
    b = matrix(np.random.rand(3,1))
    sel = matrix((v!=0).flatten())
    print(v,sel)
    print(matrix([1,2,3]))
    condition = (v > 0)
    print('condition',condition)
    print('vcondition',v[condition], v[condition].shape, type(v))
    print('v and b',v)
    print(b)
 #   v[condition]=b.T
    c  = matrix(np.array([True,False,True])).T
    print(c, c.shape)
    print(v[c])
    sum = np.sum(v)
    v = v/sum
    a = v
    print(a)
    select = v
   # select[:] =  (v[:] > 0).astype(b)
    select = np.where(v>0.5)
    print('select', select)
    v[select[:]] = v[select[:]] + 1
    print(v)
def TestNormalizeMatrixA():
    M = matrix([[1.0,2.0,3.0],
         [1.0,2.0,3.0],
         [1.0,2.0,3.0]])
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))
    print('S',S)
    sel = np.where(S!=0)
    print('sel',sel)
    S[sel] = 1.0 / S[sel]
    print('norm S',S)
    Q = np.diagflat(S.T)
    print('Q',Q)
    M = M*Q
    print(M)
    S = matrix(np.sum(M,axis = axis_id))
    print(S)
    return S
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
def TestUpdateZeroRow():
    M = matrix([[1.0,2.0,3.0],
         [0.0,0.0,0.0],
         [0.0,0.0,0.0],
         [1.0,2.0,3.0]])
    nm = UpdateNormalizeDanglingMat(M)
    print(M)
    axis_id=1
    S = matrix(np.sum(M,axis = axis_id))
    is_dangling = np.where(S == 0)[0]
    colnum = M.shape[1]
    print(colnum)
    p = matrix(np.ones((1,3), dtype=np.float)*1.0/colnum)
    S = matrix(np.sum(M,axis = axis_id))
    st = matrix(np.ones((2,3), dtype=np.float)*1.0/colnum)
    danglenodes = np.where(S == 0.0)
    print(danglenodes)
    M[danglenodes[0],:] = st
    print(M)
def TestPageRankMatrix():
    M = matrix([[1.0,1.0,1.0,1.0],
         [0.0,0.0,0.0,0.0],
         [0.0,0.0,0.0,0.0],
         [1.0,1.0,1.0,1.0]])

    print('matrix m', M)
    print('transposed m',M.T)
    M = MakeSymmetricMatrix(M,mode='merg')
    print('symmetrized', M)
    nM = NormalizeMatrix(M)
    print('normalized matrix',nM)
    g = MakeGraphObjectFromMatrix(M)
    for i in range(M.shape[0]):
        print(i,g[i])
    v = nx.pagerank(g)
    print('vpagerank',list(v.values()))
    v = MyPageRankMatT(M) #this will be the equal implementation of nx.pagerank because it treat M as an
    print(('vmypagerank',v))



def TestPageRank():
    M = matrix([[1.0,1.0,1.0,1.0],
         [0.0,0.0,0.0,0.0],
         [0.0,0.0,0.0,0.0],
         [1.0,1.0,1.0,1.0]])
    M = M + M.T
    N = M.shape[0]
    print(M)
    print(N)
    alpha=1
    axis_id = 1
    p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    print(('p',p))
    print(('dangling_weights',dangling_weights))
    S = matrix(np.sum(M,axis = axis_id))
    x = matrix(np.random.rand(N,1))
    print('x',x)
    v=M*x
    print('v',v)
    print(('S',S))
    is_dangling = np.where(S == 0)[0]
    print(is_dangling)
    sw = sum(x[is_dangling])
    print(('sw',sw*dangling_weights))
    max_iter = 5
    for _ in range(max_iter):
        print(x)
        v = M*x
        print(('M*x',v))
        a = sw * dangling_weights
        print(('a',a))
        x = alpha * ( M*x + sw * dangling_weights) #+ (1 - alpha) * p
        print(('x',x))
    print(x)
    v = MyPageRank(M)
    print(('v',v))
    v = MyPageRankMatT(M) #this will be the equal implementation of nx.pagerank because it treat M as an
    #undirected adjecent matrix with only 0,1 score in it.
    print(('v1',v))
    print(('M',M))
    g = MakeGraphObjectFromMatrix(M)
    print(g[0])
    print(g[1])
    print(g[2])
    print(g[3])
    v = nx.pagerank(g)
    print('v2',list(v.values()))
def MyPageRank(M,alpha=0.9,max_iter=20, p=None):
    #note M is a matrix object, and row is out degree
    N = M.shape[0]
    M=NormalizeMatrix(M,1)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))


    x = matrix(np.random.rand(N,1))
    is_dangling = np.where(S == 0)[0]
    sw = sum(x[is_dangling])
#    max_iter = 20
    for _ in range(max_iter):
        sw = sum(x[is_dangling])
        x = alpha * ( M*x + sw * dangling_weights) + (1 - alpha) * p
    return x
def MyPageRankMat(M,alpha=0.85,max_iter=100, p=None):
    #note M is a matrix object, and row is out degree
    N = M.shape[0]
    M=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0)[0]
    is_dangling = []
    sw = sum(x[is_dangling])

#    max_iter = 20
    for _ in range(max_iter):
        sw = sum(x[is_dangling])
        x = alpha * M*x + sw * dangling_weights + (1 - alpha) * p
#        x = alpha * M*x  + (1 - alpha) * p
    return x
def MakeGraphObjectFromMatrix(M,makebidirect=False):
    nr,nc=M.shape
    print(M)
    g = nx.Graph()
    for i in range(nr):
        g.add_node(i)
    for i in range(nr):
        for j in range(nc):
            jaccard = M[i,j]
            print('i,j',i,j,jaccard)
            g.add_edge(i, j, weight=jaccard)
          #  g.add_edge(j, i, weight=jaccard)
    return g

def MakeAdjecentMatrix(M):
    dm= M.copy()
    sel = np.where(dm>0.0)
    dm[sel] = 1
    return dm
def MyPageRankMatT(M,alpha=0.85,max_iter=100, p=None):
    #note M is a matrix object, and row is out degree
  #  M = MakeAdjecentMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    N = M.shape[0]
    M=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0)[0]
    sw = sum(x[is_dangling])
    is_dangling = []
    x = x.T
    dangling_weights = dangling_weights.T
    p= p.T
#    max_iter = 20
    tol=1.0e-6
    for _ in range(max_iter):
        xlast = x
        sw = sum(xlast.T[is_dangling])
        x = alpha * xlast*M + sw * dangling_weights + (1 - alpha) * p
#        x = alpha * M*x  + (1 - alpha) * p
        err = sum(abs(x-xlast))
        if err < N*tol:
            return x
    return x

def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_2.txt.pk'
    model= HybridGraph(pk)
    topksent = 10
    tops = model.OutPutTopKSent(topksent,1,-1)
    for eachs in tops:
        print(eachs)
if __name__ == '__main__':
    #TestNormalizeMatrixA()
  #  TestPickle()
  #  TestPageRank()
    TestPageRankMatrix()
    #TestUpdateZeroRow()
"""
def test_page_rank():
    path = r'C:\\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    page_rank(pickle_path)


def main():
    test_page_rank()

"""