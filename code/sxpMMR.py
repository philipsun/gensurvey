import nltk
import os
import numpy as np
import sxpFenciMakeTFIDF
# ---------------------------------------------------------------------------------


def build_sim_matrix(corpus):
    sxptfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(corpus,True)
    tfidf= sxptfidf.tfidf
    pairwise_similarity = (tfidf * tfidf.T).A
    #sim_matrix = pd.DataFrame(pairwise_similarity)
    return pairwise_similarity,sxptfidf
def build_query_sim_matrix(keywordquery, sxptfidf):
    qv = sxptfidf.vectorizer.transform([keywordquery]);
    a = np.array(qv > 0);
    # print(a)
    # print((list(zip(*np.nonzero(qv)))))
    # print((np.nonzero(qv)))
    # print((np.nonzero(qv)[1]))
    cn = np.nonzero(qv)[1]
    #test_tfidf = sxptfidf.tfidftransformer.transform(qv)
    # print(test_tfidf)
    # print((sxptfidf.tfidf.shape))
    # print((sxptfidf.tfidf[0, cn]))
    # print((sxptfidf.tfidf[1,cn]))
    # print((np.sum(sxptfidf.tfidf[0,cn])))
    # print((np.sum(sxptfidf.tfidf[1, cn])))
    r = np.sum(sxptfidf.tfidf[:, cn], 1)
    #print(r)
    return r
def mmr(q,corpus):
    n = len(corpus)
    sim2, sxptfidf = build_sim_matrix(corpus)
    sim1 = build_query_sim_matrix(q,sxptfidf)
    S = []
    D = np.array(range(n))
    m0 = np.argmax(sim1)
    ms = np.max(sim1)
    S = [m0]
    RI = np.ones((n,1)).astype(bool).reshape((n,))
    SI = np.zeros((n,1)).astype(bool).reshape((n,))
    SI[m0]=True
    RI[m0]=False

    L = 0.5
    topk = [m0]
    topkscore = [ms]
    maxdf = 1
    R_S = D[RI]
    if len(R_S) < 1:
        return topk, topkscore,maxdf
    while(len(R_S)>=1):
        pass
        R_S = D[RI]
        s = []
        for di in R_S:
            ms = []
            for dj in S:
                ms.append(sim2[di,dj])
            ms = max(ms)
            simscore = L *sim1[di]
            innersim = (1-L)*ms
            score = simscore - innersim
           # print(simscore,innersim)

            s.append(score[0,0])
        maxscore = max(s)
        NextS = R_S[np.argmax(s)]
        topk.append(NextS)
        topkscore.append(maxscore)
        SI[NextS]=True
        RI[NextS]=False
        if np.any(RI):
            continue;
        else:
            break;
    df = np.diff(topkscore)
    maxdf = np.argmax(df)
    return topk, topkscore,maxdf
def testmmr():
    corpus = ['hell this is a test for mmr',
              'mmr is an algorithm that is used to find most relevant sentences from a set of documents',
              'I am currently a research in ai',
              'I am good at doing mmr research',
              'I am experiences in algorithm programming']
    query  = 'mmr algorithm'
    topk, topkscore,maxdf = mmr(query,corpus)
    print(topk)
    print(topkscore)
    print(maxdf)
def testnp():
    a = np.ones((5,1)).astype(bool).reshape((5,))
    print(a,a[1])
    b = np.random.rand(5,5)
    print(b)
    c = b[[True,True,True,True,True],1]
    print(c, c.shape)
    d = b[a,1]
    print(d,d.shape)
    z = np.zeros((5,1)).astype(bool).reshape((5,))
    print(z)
    d = b[z, 1]

    print(d,d.shape) # []

    a[1]=False
    print(a,a[1])
    d = b[a,1]
    print(d,d.shape)
    for each in d:
        print(each)
def main():
    #testnp()
    testmmr()
if __name__ == '__main__':
    main()