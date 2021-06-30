# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      sunxp
#
# Created:     14/03/2019
# Copyright:   (c) sunxp 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'a'
from sxpPackage import *
import networkx as nx
import numpy as np
from numpy import *
from numpy import matrix
from numpy import random
import re
import sxpReadFileMan
import sxpJudgeCharacter
global_para= {}
global_para['undirect']=0
global_para['remove_stopwords']=0
global_para['addseq']=0
global_para['mode']='wd_ss'
global_para['alpha_beta']=[0.8,0.2]
global_para['maxword']=300
global_para['topksent']=-1
global_para['sent_dir']='frontfirst'
#global_para['sent_dir'] = 'frontfirst'
global_para['transpose']=False
class WordNetwork:
    def __init__(self, pickle_ob,undirect=0, remove_stopwords=1, iteration_times=20,mode='ss_pr'):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.t_p = None
        self.s_t = None
        self.w = []
        self.s = []
        self.p = []
        self.c = []
        self.t = [] #context5
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
        #self.text = LoadSxptext(pickle_path)
        self.text = pickle_ob
        undirect=global_para['undirect']
        remove_stopwords=global_para['remove_stopwords']
        mode=global_para['mode']
        addseq = global_para['addseq']
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        self.stopwords = [line.strip() for line in lines]
        if remove_stopwords == 0:
            self.get_parameters_with_stopwords()
        elif remove_stopwords == 1:
            self.get_parameters_without_stopwords()
        if mode == "wd_ss":
        #    15 ROUGE - 1  Average_R: 0.50488(95 % -conf.int. 0.49689 - 0.51257)
            print(('ModelDucHybrid',mode))
            self.reverse = 0
            w = matrix(random.rand(len(self.words))).T
            s = matrix(random.rand(len(self.text.sentenceset))).T
        # it is mainly due to undirect = 0 to let those sentences at the begining part have hight scores
        # and those sentences at end parts will have lower scores.
            useold =True
            if global_para['sent_dir'] == 'frontfirst':#frontsent
                if useold:
                   print('use old version of MakeSentenceWordMatrix to seg word')
                   self.MakeSentenceWordMatrix(undirect=undirect,addseq=addseq) #this is previous work
                else:
                    print('use new version of MakeSentenceWordMatrix to seg word')
                    self.MakeSentWordSentMatrix(undirect=undirect,addseq=addseq)
                testdebug = 1
            if global_para['sent_dir']=='endfirst':
                if useold:
                   print('use old version of MakeSentenceWordMatrix to seg word')
                   self.MakeSentenceWordMatrix(undirect=undirect,addseq=addseq) #this is previous work
                else:
                    print('use new version of MakeSentenceWordMatrix to seg word')
                    self.MakeSentWordSentMatrix(undirect=undirect,addseq=addseq)
                print('use end first version MakeEndSentenceWordMatrix build es-es matrix')
                self.MakeEndSentenceWordMatrix(undirect=undirect,addseq=addseq)
                testdebug = 3
            if global_para['sent_dir']=='endfront':
                if useold:
                    print('use old version of MakeSentenceWordMatrix to seg word')
                    self.MakeSentenceWordMatrix(undirect=undirect, addseq=addseq)  # this is previous work
                else:
                    print('use new version of MakeSentenceWordMatrix to seg word')
                    self.MakeSentWordSentMatrix(undirect=undirect, addseq=addseq)
                print('use end_front first version MakeFrontEndSentenceWordMatrix build s_s matrix')
                self.MakeFrontEndSentenceWordMatrix(undirect=undirect, addseq=addseq)
            testdebug = 1
            if global_para['sent_dir'] == 'endfront_debug':
                self.MakeFrontEndSentIteration(undirect=undirect, addseq=addseq)
                self.rank_weight()
                return
            if testdebug == 1:
                self.iterationws_debug()
            if testdebug == 2:
                self.iterationws()
            if testdebug == 3:
                print('use end first version to iterate es-es matrix')
                self.iterationes()
        self.rank_weight()
#        self.ordered_sentence_id_set()

    def get_parameters_with_stopwords(self):
        print("wordnet do not remove stopwords")
        self.words = self.text.sentence_tfidf.word
        self.w = matrix(random.rand(len(self.words))).T

       # import relation matrix
        #here s_k is the sentence -word tfidf matrix from sxpParseDUCText.py
        self.w_s = matrix(self.text.s_k.toarray()).T
        #self.w_s = matrix(self.text.sentence_tfidf.ct.toarray()).T #for version one
        nw,ns = self.w_s.shape
        print(('nw',nw,'ns',ns))
    def skipstop(self, eachword):
        if global_para['remove_stopwords']==0:
            return False;
        if eachword in self.stopwords:
            return True
        return False;

    def get_parameters_without_stopwords(self):
        print("wordnet remove stopwords")
        self.words = self.text.sentence_tfidf.word
        # import relation matrix
        self.w_s = matrix(self.text.s_k.toarray()).T
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        stopwords = [line.strip() for line in lines]
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
               and re.match(r'^[a-zA-Z]+$', self.words[i]) is not None]
        new_w_s = []
        for i in idx:
            new_w_s.append(np.array(self.w_s[i, :]).tolist())
        new_w_s = matrix(np.array(new_w_s))
        new_words = [self.words[i] for i in idx]
        self.words = new_words
        self.w_s = new_w_s
        self.w = matrix(random.rand(len(self.words))).T
     #   print(self.words)
    def rank_weight(self):
      #  print('word weight',self.w.shape)
        print((type(self.s)))
        self.idx_w = list(argsort(-self.w, axis=0).flat)
      #  print(self.idx_w)
        self.idx_s = list(argsort(-self.s, axis=0).flat)
      #  print self.idx_s
##        for i in self.idx_s:
##            print(self.s[i])

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
       # print self.idx_s
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        for sentence in ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set
    def OutputAllSentWeight(self):
        ranked_sentences = [[self.s[self.idx_s[i]], self.text.sentence_textset[self.idx_s[i]]]
                            for i in range(len(self.text.sentence_textset))]
        return ranked_sentences
    def OutPutTopKWord(self, topk=20):
      #  words = self.text.sentence_tfidf.word
      #  print(len(self.words))
      #  print(len(self.idx_w))
        ranked_words = [[self.words[self.idx_w[i]],self.w[self.idx_w[i]]]
                            for i in range(len(self.words))]
        return ranked_words[0:topk]

    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax=0,sortinraw=0):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        if useabstr == 0:
            if maxwords==-1:
                usetopk = True;
            else:
                usetopk = False
        if useabstr == 1:
            abstractlen = len(self.text.abstract.split(' '))
            maxwords = abstractlen
            usetopk = False

        if useabstr == 2:
            abstractlen = len(self.text.conclusion.split(' '))
            maxwords = abstractlen
            usetopk = False
        wordlen = 0
        print(('use topk', usetopk, 'maxword',maxwords))
        for sentence in ranked_sentences:
            if len(sentence.sentence_text)<=1:
                 continue
            words = sentence.sentence_text.split(' ')
            wl = len(words)
            if usetopk:
                if i>=topk:
                    break
            else:
                if strictmax == 1:
                    if wordlen + wl > maxwords:
                        seglen = wordlen+wl -maxwords
                        if seglen<=0:
                            break
                        else:
                            wl = seglen
                            segsent = words[0:wl]
                            usesent = ' '.join(segsent)
                            sent_txt_set.append(usesent)
                            wordlen = wordlen + wl
                            break
                else:
                    if wordlen >= maxwords:
                        break
            wordlen = wordlen + wl#len(sentence.sentence_text)
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        # this out put is to sort he topk sentences in their ranks.
        if sortinraw==1:
            ns = len(sent_txt_set)
            sid=self.idx_s[:ns]
            index_array = np.argsort(sid)
            sortsent = [sent_txt_set[i] for i in index_array]

            return sortsent
        else:
            return sent_txt_set
    def page_rank(self, pickle_path):
        g = create_graph(pickle_path)
        pr = nx.pagerank(g)
        self.idx_s = list(argsort(list(pr.values())))
        self.idx_s.reverse()
    def TestHits(self):

##        self.w = matrix(np.zeros((1,nw),dtype=np.float))
##        self.s = matrix(np.zeros((1,ns),dtype=np.float))
        self.MakeHitMatrix()
        self.iterationhits()
        self.rank_weight()
        sentlist=self.OutputAllSentWeight()
        for i, each in enumerate( sentlist):
            print(('----',i,each[0],each[1]))
        wordlist=self.OutPutTopKWord()
        for each in wordlist:
            print((each, ','))
    def TestHitsHybrid(self):
        self.MakeHitMatrix()
        self.iterationhitshybrid()
        self.rank_weight()
        sentlist=self.OutputAllSentWeight()
        for i, each in enumerate( sentlist):
            print(('----',i,each[0],each[1]))
        wordlist=self.OutPutTopKWord()
        for each in wordlist:
            print((each, ','))

    def TestPageRank(self):
        self.MakeSentSentMatrix()
        self.iterationhybrid()
        self.rank_weight()
        sentlist=self.OutputAllSentWeight()
        for i, each in enumerate( sentlist):
            print(('----',i,each[0],each[1]))
        wordlist=self.OutPutTopKWord()
        for each in wordlist:
            print((each, ','))

#build graph between sentences
    def TestRankSentence(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

                m[i,j]=jaccard
                m[j,i]=jaccard
        self.s_s = matrix(m)

        sentences = self.text.sentenceset
        g = nx.Graph()
        i = 0
        for sent in sentences:
            g.add_node(sent.id)
##            print i, sent.id, sentences[i].id
            i = i + 1
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)
                g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
                g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)

        nr,nc = self.s_s.shape
        gc = len(g)
        print((nr,nc,gc))
        gm = matrix(np.zeros((nr,nr),dtype=np.float))
        for i in range(nr):
            for j in g[i]:
                gij= g[i][j]
                gm[i,j] = gij['weight']

               # print gij['weight']
                if self.s_s[i,j] != gij['weight']:
                    print((i,j, self.s_s[i,j],gij['weight']))
        for i in range(nr):
            for j in range(nr):
                if gm[i,j] !=  self.s_s[i,j]:
                    if j in g[i]:
                        gij= g[i][j]
                        print((i,j, self.s_s[i,j],gm[i,j],gij['weight']))
                    else:
                        print((j, 'not in g[i]', i, 'but', self.s_s[i,j], 'and m[i,j] is ', m[i,j]))

        pr,W = nx.pagerank(g)

        self.idx_s = list(argsort(list(pr.values())))
        self.idx_s.reverse()
        print((self.idx_s))

        r,W1 = MyPageRankMatT(self.s_s,alreadysym=False)
        self.idx_s = argsort(r.flatten()).tolist()[0]
        self.idx_s.reverse()
        print((self.idx_s))
        print((np.sum(W1,1)))
        nw = matrix(np.zeros((nr,nr),dtype=np.float))
        for i in range(nr):
            for j in W[i]:
                wij= W[i][j]
               # print gij['weight']
                nw[i,j]= wij['weight']
##                if nw[i,j] != W1[i,j]:
##                    print i,j,nw[i,j],W1[i,j]
        print((np.sum(nw,1)))
        print((np.sum(nw[0,:]), nw[0,:]))
        print((np.sum(W1[0,:]), W1[0,:]))

    def iterationhybrid(self):
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        N = M.shape[0]
        alpha, max_iter, S_S, x, per, dangling_weights, is_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        max_iter = 200
        for _ in range(max_iter):
            xlast = x.copy()
            sw = sum(xlast.T[is_dangling])
            x = alpha * xlast * S_S + alpha * sw * dangling_weights + (1 - alpha) * per
            ws = self.w_s.T * w
            x = 0.6 * x + 0.4 * ws.T
            s = x.T
            w = self.w_s * s  # this is the latest one that incorporate context

            w = self.normalize(w)
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x - xlast))
            if err < N * tol:
                break
        self.w = w.T
        self.s = x.T
        print((self.s.shape))

    def iterationss(self):
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        N = M.shape[0]
        alpha, max_iter, S_S, x, per, dangling_weights, is_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6

        for _ in range(max_iter):
            xlast = x.copy()
            sw = sum(xlast.T[is_dangling])
            x = alpha * xlast * S_S + alpha * sw * dangling_weights + (1 - alpha) * per
            s = self.w_s.T * w
            x = 0.5 * x + 0.5 * s.T
            s = x.T
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x - xlast))
            if err < N * tol:
                break
        self.w = w.T
        self.s = x.T
        print((self.s.shape))
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
    def networkhits(self):
        ns,ns = self.s_s.shape
        try:
            hubs, authorities=nx.hits(self.g,max_iter=200)
            self.s = matrix(list(hubs.values())).reshape(ns, 1)
        except Exception(e):
            self.iterationhits()


    def iterationhits(self):

        M = self.s_s
        ns,ns = M.shape
        nw,ns = self.w_s.shape
        s_h = np.random.rand(ns,1)
        s_a = np.random.rand(ns,1)
        w_h = np.random.rand(nw,1)
        w_a = np.random.rand(nw,1)

        N = M.shape[0]
        alpha,max_iter,S_S,x,per,dangling_weights,is_dangling=PreparePageRankMatrix(M,alpha=0.85,max_iter=100, p=None, alreadysym=True)
        i = 0
        tol=1.0e-6
        s_a_t_1 = s_a.copy()
        s_h_t_1 = s_h.copy()
        max_iter = 10
        for _ in range(max_iter):
            s_a  = s_h.T * M
            s_h  = M*s_a.T

            s_h = s_h * 1.0 / np.max(s_h)
            s_a = s_a * 1.0 / np.max(s_a)
        self.w = w_a.reshape(1,nw)
        #this will got 0.43 precision.
        self.s = s_a.reshape(ns,1)
        #this will got 0.48 precision.
        #self.s = s_a.reshape(ns,1)
        #self.s = s_a.reshape(ns,1)=s_a.reshape(ns,1) + s_h.reshape(ns,1) #this will get 0.46
        self.s_a = s_a.reshape(ns,1)
        self.s_h = s_h.reshape(ns,1)
        self.w_a = w_a.reshape(1,nw)
        self.w_h = w_h.reshape(1,nw)
      #  print('HITS',s_a,s_h)
      #  print('word weight',self.w.shape,self.w)
        #here s_a is (1,9), s_h is (9,1)
       # print (s_a.shape,s_h.shape)
    def iterationhitshybrid(self):

        M = self.s_s
        ns,ns = M.shape
        nw,ns = self.w_s.shape
        s_h = np.random.rand(ns,1)
        s_a = np.random.rand(ns,1)
        w_h = np.random.rand(nw,1)
        w_a = np.random.rand(nw,1)

        N = M.shape[0]
        alpha,max_iter,S_S,x,per,dangling_weights,is_dangling=PreparePageRankMatrix(M,alpha=0.85,max_iter=100, p=None, alreadysym=True)
        i = 0
        tol=1.0e-6
        s_a_t_1 = s_a.copy()
        s_h_t_1 = s_h.copy()
        max_iter = 10
        for _ in range(max_iter):
            s_a  = s_h.T * self.s_s #here (9,1).T*(9,9) = (1,9)*(9,9)=(1,9)
            s_h  = self.s_s*s_a.T #here  (9,9)*(1,9).T = (9,9)*(9,1) = (9,1)
            s_a = s_a + w_h.T*self.w_s #w_h: (100,1).T * (100,9)=(1,9)
            s_h = s_h + self.w_s.T * w_a #w_a: (100,1), (100,9).T *(100,1)=(9,1)

            s_h = s_h * 1.0 / np.max(s_h) #(9,1)
            s_a = s_a * 1.0 / np.max(s_a) #(1,9)

            w_a = self.w_s * s_h #s_a is (1,9), (100,9)*(9,1)=(100,1)
            w_h = self.w_s * s_a.T # (100,9)*(1,9).T = (100,1)



        self.w = w_a.reshape(1,nw) + w_h.reshape(1,nw)
        self.s = s_a.reshape(ns,1) + s_h.reshape(ns,1)
        self.s_a = s_a.reshape(ns,1)
        self.s_h = s_h.reshape(ns,1)
        self.w_a = w_a.reshape(1,nw)
        self.w_h = w_h.reshape(1,nw)
      #  print('HITS',s_a,s_h)
      #  print('word weight',self.w.shape,self.w)
        #here s_a is (1,9), s_h is (9,1)
       # print (s_a.shape,s_h.shape)
    def iterationws_debug(self):
        print(('wordnet alpha iterationws', global_para['alpha_beta']))
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        ns,ns = M.shape
        print((ns, self.s_s.shape, self.w_s.shape, self.w_w.shape))
        #(9, (9, 9), (9, 130), (130, 130))
        N = M.shape[0]
        alpha, max_iter, S_S, x, sper, sdangling_weights, sis_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        alpha, max_iter, W_W, wx, wper, wdangling_weights, wis_dangling = PreparePageRankMatrix(self.w_w, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=global_para['alpha_beta'][0]
        wpara =global_para['alpha_beta'][1]
        # spara = 0.8
        # wpara =0.2
        for _ in range(max_iter):
            xlast = x.copy()
            sw = sum(xlast.T[sis_dangling])
            x = alpha * xlast * S_S + alpha * sw * sdangling_weights + (1 - alpha) * sper


            dangw = sum(wx.T[wis_dangling])
            ww = alpha * wx * W_W + alpha * dangw * wdangling_weights + (1 - alpha) * wper


            ws = ww * self.w_s.T
            # x = 0.6 * x + 0.4 * ws.T
            x = spara * x + wpara * ws
            s = x.T

            # print('s',i,s)
            # print('w',i,w)
            ssw = ww+s.T*self.w_s   # this is the latest one that incorporate context
            wx = self.normalize(ssw)  # this performs the same remove it or not, does not make any change on the whole rank
            s = self.normalize(s)
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x - xlast))
            if err < N * tol:
                break
        self.w = wx.T
        self.s = x.T
        print((self.w.shape))
        print((self.s.shape))
    def iterationes(self):
        print(('wordnet alpha iterationes', global_para['alpha_beta']))
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.es_es
        ns,ns = M.shape
        print((ns, self.es_es.shape, self.w_s.shape, self.w_w.shape))
        #(9, (9, 9), (9, 130), (130, 130))
        N = M.shape[0]
        alpha, max_iter, S_S, s, sper, sdangling_weights, sis_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        alpha, max_iter, W_W, wx, wper, wdangling_weights, wis_dangling = PreparePageRankMatrix(self.w_w, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=global_para['alpha_beta'][0]
        wpara =global_para['alpha_beta'][1]
        for _ in range(max_iter):
            slast = s.copy()
            dangs = sum(slast.T[sis_dangling])
            ss = alpha * slast * S_S + alpha * dangs * sdangling_weights + (1 - alpha) * sper
            dangw = sum(wx.T[wis_dangling])
            ww = alpha * wx * W_W + alpha * dangw * wdangling_weights + (1 - alpha) * wper

            ws =  ww* self.w_s.T

         #   s = 0.6 * ss + 0.4 * ws
            s = spara *ss + wpara *ws
            wx = ww.copy(); #update word network
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(s - slast))
            if err < N * tol:
                break
        self.w = ww.reshape(-1,1)
        self.s = s.reshape(-1,1)
        print((self.s.shape,self.w.shape))
    def iterationws(self):
        print(('wordnet alpha iterationws', global_para['alpha_beta']))
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        ns,ns = M.shape
        print((ns, self.s_s.shape, self.w_s.shape, self.w_w.shape))
        #(9, (9, 9), (9, 130), (130, 130))
        N = M.shape[0]
        alpha, max_iter, S_S, s, sper, sdangling_weights, sis_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        alpha, max_iter, W_W, wx, wper, wdangling_weights, wis_dangling = PreparePageRankMatrix(self.w_w, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=global_para['alpha_beta'][0]
        wpara =global_para['alpha_beta'][1]
        for _ in range(max_iter):
            slast = s.copy()
            dangs = sum(slast.T[sis_dangling])
            ss = alpha * slast * S_S + alpha * dangs * sdangling_weights + (1 - alpha) * sper
            dangw = sum(wx.T[wis_dangling])
            ww = alpha * wx * W_W + alpha * dangw * wdangling_weights + (1 - alpha) * wper

            ws =  ww* self.w_s.T

         #   s = 0.6 * ss + 0.4 * ws
            s = spara *ss + wpara *ws
            wx = ww.copy(); #update word network
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(s - slast))
            if err < N * tol:
                break
        self.w = ww.reshape(-1,1)
        self.s = s.reshape(-1,1)
        print((self.s.shape,self.w.shape))
    def MakeSentWordSentMatrix(self,undirect=1,addseq=0):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        self.g = nx.Graph()

        if addseq > 0:
            for i in range(len(sentences) - 1):
                if addseq == 1:
                    m[i + 1, i] = 1
                    self.g.add_edge(i+1, i, weight=1)
                if addseq == 2:
                    m[i, i + 1] = 1
                    self.g.add_edge(i, i + 1, weight=1)
                if addseq == 3:
                    m[i + 1, i] = 1
                    m[i, i + 1] = 1
                    self.g.add_edge(i + 1, i, weight=1)
                    self.g.add_edge(i, i + 1, weight=1)
        word_dict_id={}
        for i,wd in enumerate(self.words):
            word_dict_id[wd]=i
        num_word = len(list(word_dict_id.items()))
        self.w = np.random.rand(num_word,1)
        self.w_w = np.zeros((num_word,num_word))


        #begin to build w-w sequence graph
        self.w_s = np.zeros((ns,num_word))

        for t, eachsent in enumerate( sentences):
            wd = sentences[t].sentence_text.lower()
            n =len(wd)
            if n <=2:
                 continue
            for i in range(n-1):
                if wd[i] not in list(word_dict_id.keys()):
                    continue;
                if wd[i+1] not in list(word_dict_id.keys()):
                    continue;
                k = word_dict_id[wd[i]]
                j = word_dict_id[wd[i+1]]
                self.w_w[j,k]=1
                self.w_s[t,k]=1
            if wd[-1] in list(word_dict_id.keys()):
                self.w_s[ t,word_dict_id[wd[-1]]] = 1
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)
                m[j,i]=jaccard #note that j-i is good than i-j and
                self.g.add_edge(j, i, weight=jaccard)
                if undirect ==1:
                    m[i,j]=jaccard
                    self.g.add_edge(i, j, weight=jaccard)
        self.s_s = matrix(m)
    def MakeFrontEndSentenceWordMatrix(self, undirect=0, addseq=0):
        sentences = self.text.sentence_textset
        #  sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        ei = list(range(len(sentences)))
        ei.reverse()
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                si = ei[i]
                sj = ei[j]
                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[si],sentences[sj])

                if self.reverse:
                    if jaccard >0:
                        jaccard = 1.0/jaccard
                m[sj,si]=jaccard #note that j-i is good than i-j and
                if undirect ==1:
                    m[si,sj]=jaccard
        if global_para['transpose']==True:
            m = m.transpose()
            print('sent_matrix is transposed')
        self.es_es = matrix(m)
        self.s_s = self.s_s +self.es_es;
        print((ns, self.es_es.shape,self.w_s.shape,self.w_w.shape))
    def MakeFrontEndSentIteration(self,undirect=0, addseq=0):
        self.MakeSentenceWordMatrix(undirect,addseq)
        self.MakeEndSentenceWordMatrix(undirect,addseq)

        print(('wordnet alpha iterationes', global_para['alpha_beta']))
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T
        #-------------iterate es_es_______
        M = self.es_es
        ns,ns = M.shape
        print((ns, self.es_es.shape, self.w_s.shape, self.w_w.shape))
        #(9, (9, 9), (9, 130), (130, 130))
        N = M.shape[0]
        alpha, max_iter, S_S, s, sper, sdangling_weights, sis_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        alpha, max_iter, W_W, wx, wper, wdangling_weights, wis_dangling = PreparePageRankMatrix(self.w_w, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=global_para['alpha_beta'][0]
        wpara =global_para['alpha_beta'][1]
        for _ in range(max_iter):
            slast = s.copy()
            dangs = sum(slast.T[sis_dangling])
            ss = alpha * slast * S_S + alpha * dangs * sdangling_weights + (1 - alpha) * sper
            dangw = sum(wx.T[wis_dangling])
            ww = alpha * wx * W_W + alpha * dangw * wdangling_weights + (1 - alpha) * wper

            ws =  ww* self.w_s.T

         #   s = 0.6 * ss + 0.4 * ws
            s = spara *ss + wpara *ws
            wx = ww.copy(); #update word network
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(s - slast))
            if err < N * tol:
                break
        # ----------------------------
        fes = s.copy()
        few = w.copy()
        # -------------iterate s_s_______
        print(('wordnet alpha iterationws', global_para['alpha_beta']))
        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T

        M = self.s_s
        ns,ns = M.shape
        print((ns, self.s_s.shape, self.w_s.shape, self.w_w.shape))
        #(9, (9, 9), (9, 130), (130, 130))
        N = M.shape[0]
        alpha, max_iter, S_S, s, sper, sdangling_weights, sis_dangling = PreparePageRankMatrix(M, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        alpha, max_iter, W_W, wx, wper, wdangling_weights, wis_dangling = PreparePageRankMatrix(self.w_w, alpha=0.85, max_iter=100,
                                                                                            p=None, alreadysym=True)
        i = 0
        tol = 1.0e-6
        spara=global_para['alpha_beta'][0]
        wpara =global_para['alpha_beta'][1]
        for _ in range(max_iter):
            slast = s.copy()
            dangs = sum(slast.T[sis_dangling])
            ss = alpha * slast * S_S + alpha * dangs * sdangling_weights + (1 - alpha) * sper
            dangw = sum(wx.T[wis_dangling])
            ww = alpha * wx * W_W + alpha * dangw * wdangling_weights + (1 - alpha) * wper

            ws =  ww* self.w_s.T

         #   s = 0.6 * ss + 0.4 * ws
            s = spara *ss + wpara *ws
            wx = ww.copy(); #update word network
            i = i + 1
            #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(s - slast))
            if err < N * tol:
                break
        # ----------------------------
        fs = s.copy();
        fw = w.copy();
        ww = few + fw;
        ss = fs + fes;
        self.w = ww.reshape(-1,1)
        self.s = ss.reshape(-1,1)
    def MakeEndSentenceWordMatrix(self, undirect=0, addseq=0):
        sentences = self.text.sentence_textset
        #  sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        ei = list(range(len(sentences)))
        ei.reverse()
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                si = ei[i]
                sj = ei[j]
                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[si],sentences[sj])

                if self.reverse:
                    if jaccard >0:
                        jaccard = 1.0/jaccard
                m[sj,si]=jaccard #note that j-i is good than i-j and
                if undirect ==1:
                    m[si,sj]=jaccard
        if global_para['transpose']==True:
            m = m.transpose()
            print('sent_matrix is transposed')
        self.es_es = matrix(m)
        print((ns, self.es_es.shape,self.w_s.shape,self.w_w.shape))
    def MakeSentenceWordMatrix(self,undirect=0,addseq=0):
        sentences = self.text.sentence_textset
        #  sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)

        word_dict ={}
        for i, eachsent in enumerate( sentences):
            wd = sxpJudgeCharacter.segsenttowords(eachsent)
            for eachword in wd:
                if len(eachword)==0:
                    continue
                if eachword.isspace():
                    continue
                if self.skipstop(eachword):
                    continue;
                if eachword in word_dict:
                    sentid = word_dict[eachword]
                    sentid.append(i)
                else:
                    sentid =[]
                    sentid.append(i)
                    word_dict[eachword]=sentid
        word_dict_id={}
        self.words=[]

        for i,(each,sentid) in enumerate( word_dict.items()):
            word_dict_id[each] = i
            self.words.append(each)

        num_word = len(list(word_dict_id.items()))
        self.w = np.random.rand(num_word,1)
        self.w_w = np.zeros((num_word,num_word))


        #begin to build w-w sequence graph
        self.w_s = np.zeros((ns,num_word))

        for t, eachsent in enumerate( sentences):
            sents = sxpJudgeCharacter.SplitSubSent(eachsent)
            for eachsub in sents:
                ewd = sxpJudgeCharacter.segsenttowords(eachsent)
                wd = []
                for ew in ewd:
                   if self.skipstop(ew):
                        continue;
                   wd.append(ew)
                n =len(wd)
                if n <=0:
                    continue
                for i in range(n-1):

                    k = word_dict_id[wd[i]]
                    j = word_dict_id[wd[i+1]]
                    self.w_w[j,k]=1
                    self.w_s[t,k]=1
                self.w_s[ t,word_dict_id[wd[-1]]] = 1

        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i],sentences[j])

                if self.reverse:
                    if jaccard >0:
                        jaccard = 1.0/jaccard
                m[j,i]=jaccard #note that j-i is good than i-j and
                if undirect ==1:
                    m[i,j]=jaccard
        if global_para['transpose']==True:
            m = m.transpose()
            print('sent_matrix is transposed')
        self.s_s = matrix(m)
        print((ns, self.s_s.shape,self.w_s.shape,self.w_w.shape))
    def MakeSentSentSeqMatrix(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)-1):
            m[i+1,i]=1
            #  m[i , i+1] = 1

        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

                if self.reverse:
                    if jaccard >0:
                        jaccard = 1.0/jaccard
                m[i, j] = jaccard
                m[j, i] = jaccard
        self.s_s = matrix(m)
    def MakeSentSentMatrix(self,undirect=1,addseq=0):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        self.g = nx.Graph()

        if addseq > 0:
            for i in range(len(sentences) - 1):
                if addseq == 1:
                    m[i + 1, i] = 1
                    self.g.add_edge(i+1, i, weight=1)
                if addseq == 2:
                    m[i, i + 1] = 1
                    self.g.add_edge(i, i + 1, weight=1)
                if addseq == 3:
                    m[i + 1, i] = 1
                    m[i, i + 1] = 1
                    self.g.add_edge(i + 1, i, weight=1)
                    self.g.add_edge(i, i + 1, weight=1)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

                m[j,i]=jaccard #note that j-i is good than i-j and
                self.g.add_edge(j, i, weight=jaccard)
                if undirect ==1:
                    m[i,j]=jaccard
                    self.g.add_edge(i, j, weight=jaccard)

        if global_para['transpose']==True:
            m = m.transpose()
            print('sent_matrix is transposed')
        self.s_s = matrix(m)

    def MakeHitMatrix(self, undirect=1, addseq=0):
        self.reverse = 0
        #     addseq =0
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns, ns), dtype=np.float)
        self.g = nx.Graph()

        if addseq > 0:
            for i in range(len(sentences) - 1):
                if addseq == 1:
                    m[i + 1, i] = 1
                    self.g.add_edge(i+1, i, weight=1)
                if addseq == 2:
                    m[i, i + 1] = 1
                    self.g.add_edge(i, i + 1, weight=1)
                if addseq == 3:
                    m[i + 1, i] = 1
                    m[i, i + 1] = 1
                    self.g.add_edge(i + 1, i, weight=1)
                    self.g.add_edge(i, i + 1, weight=1)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

                m[j,i]=jaccard #note that j-i is good than i-j and
                self.g.add_edge(j, i, weight=jaccard)
                if undirect ==1:
                    m[i,j]=jaccard
                    self.g.add_edge(i, j, weight=jaccard)
        self.s_s = matrix(m)

    def RankSentenceMyMat(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

                m[i,j]=jaccard
                m[j,i]=jaccard
        self.s_s = matrix(m)
        r,W1 = MyPageRankMatT(self.s_s,alreadysym=False)
       # idx_s = argsort(r.flatten()).tolist()[0]
       # idx_s.reverse()
        return r.T
    def RankSentenceNX(self):
        sentences = self.text.sentenceset
        g = nx.Graph()
        i = 0
        for sent in sentences:
            g.add_node(sent.id)
##            print i, sent.id, sentences[i].id
            i = i + 1
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):

                jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text,sentences[j].sentence_text)

        pr = nx.pagerank(g)
        #self.idx_s = list(argsort(pr.values()))
        #self.idx_s.reverse()
        return matrix(list(pr.values())).T

    @staticmethod
    def normalize(w):
#        assert(sum(w) > 0)
        w = w / sum(w)
        return w
    def update_sentence_weight_w_s(self, w,s):
        pass
    def update_sentence_weight(self, w, s):
        s = self.w_s.T * w + self.s_s*s
     #   s = self.s_s*s
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

            jaccard = sxpJudgeCharacter.jaccard_sim_norm(sentences[i].sentence_text, sentences[j].sentence_text)

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

def TestPageRankMatrix():
    M = matrix([[1.0,1.0,0.0,1.0],
         [1.0,0.0,0.0,0.0],
         [0.0,0.0,0.0,0.0],
         [1.0,1.0,0.0,1.0]])
    M = matrix(np.random.rand(10,10))
    print(('matrix m', M))
    print(('transposed m',M.T))
    M = MakeSymmetricMatrix(M,mode='merg')
    print(('symmetrized', M))
    nM = NormalizeMatrix(M)
    print(('normalized matrix',nM))
    g = MakeGraphObjectFromMatrix(M)
##    for i in range(M.shape[0]):
##        print i,g[i]
    nr,nc = M.shape
    gc = len(g)
    print((nr,nc,gc))

    for i in range(nr):
        for j in g[i]:
            gij= g[i][j]
           # print gij['weight']
            if M[i,j] != gij['weight']:
                print((i,j, M[i,j],gij['weight']))

    v = nx.pagerank(g)
    print(('vpagerank',list(v.values())))
    v = MyPageRankMatT(M) #this will be the equal implementation of nx.pagerank because it treat M as an
    print(('vmypagerank',v))


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
          #  print 'i,j',i,j,jaccard
            g.add_edge(i, j, weight=jaccard)
          #  g.add_edge(j, i, weight=jaccard)
    return g

def MakeAdjecentMatrix(M):
    dm= M.copy()
    sel = np.where(dm>0.0)
    dm[sel] = 1
    return dm
def PreparePageRankMatrix(M,alpha=0.85,max_iter=100, p=None, alreadysym=True):
        #note M is a matrix object, and row is out degree
  #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M,mode='merg')
    N = M.shape[0]
    W=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p= p.T
#    max_iter = 20
    tol=1.0e-6
    i = 0
    return alpha,max_iter,W,x,p,dangling_weights,is_dangling
def MyPageRankMatT(M,alpha=0.85,max_iter=100, p=None, alreadysym=True):
    #note M is a matrix object, and row is out degree
  #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M,mode='merg')
    N = M.shape[0]
    W=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p= p.T
#    max_iter = 20
    tol=1.0e-6
    i = 0
    for _ in range(max_iter):
        xlast = x.copy()
        sw = sum(xlast.T[is_dangling])
        x = alpha * xlast*W + alpha * sw * dangling_weights + (1 - alpha) * p
##        if i == 0:
##            print sw
##            print alpha
##
##            print x
        i = i + 1
#        x = alpha * M*x  + (1 - alpha) * p
        err = sum(abs(x-xlast))
        if err < N*tol:
            return x,W
    return x,W


def GetTopkFromRaw(fid,topk=4,maxword = 100):
    sxptxt = sxpDataDUCSum.LoadSingleDucData(fid)
    ss =[]
    n = 0
    for sent in sxptxt.sentence_textset:
        wd = sxpJudgeCharacter.segsenttowords(sent)
        if len(wd)==0:
            continue
        n = n + len(wd)
        if n>=maxword:
            break
        ss.append(sent)
    return ss
import sxpDataDUCSum
def GetMaxword(allsent,maxword=300):

    ss =[]
    n = 0
    for sent in allsent:
        wd = sxpJudgeCharacter.segsenttowords(sent)
        if len(wd)==0:
            continue
        n = n + len(wd)
        if n>=maxword:
            break
        ss.append(sent)
    return ss
def TestRawSrc(graph_dict_fid):

    print(('---------RAW Sentences-',graph_dict_fid,'------------'))
    sxptxt = sxpDataDUCSum.LoadSingleDucData(graph_dict_fid)
    for i, each in enumerate(sxptxt.sentence_textset):
        print(('_____',i,each))
    print('---------END RAW-------------------------------')
    tops = sxpDataDUCSum.LoadManualSys(graph_dict_fid, lenstr='100', peeridx=0)
    print(('---------Mannual Sentences-',graph_dict_fid,'------------'))
    for i, each in enumerate(tops):
        print(('_____',i,each))
    print('-----------END Manuall-----------------------------')
    print('-----------Model Sentences-----------------------------')
    modelist = sxpDataDUCSum.GetModelText(graph_dict_fid)
    for model_info in modelist:
        sent = model_info['sent_list']
        for i, each in enumerate( sent):
            print(('-----',i, each))
    models = sxpDataDUCSum.LoadSingleModelSent()
def TestAll():
    doc_model_sent_list = sxpDataDUCSum.LoadSingleModelSent()
    testdata =doc_model_sent_list[0]
    md_list=testdata['model']
    docid=testdata['title']
    docid=testdata['fid']

    tops = sxpDataDUCSum.LoadManualSys(docid, lenstr='100', peeridx=0)
    sxptxt = sxpDataDUCSum.LoadSingleDucData(docid)
from sklearn.naive_bayes import GaussianNB
def CollectSample():
    doc_model_sent_list = sxpDataDUCSum.LoadSingleModelSent()
    sentidx={}
    pos_sel=[]
    data=[]
    target=[]
    for testdata in doc_model_sent_list:
        md_list = testdata['model']

        docid = testdata['title']
        docid = testdata['fid']

        tops = sxpDataDUCSum.LoadManualSys(docid, lenstr='100', peeridx=0)
        sxptxt = sxpDataDUCSum.LoadSingleDucData(docid)
        docsent = sxptxt.sentence_textset
        for i,each in enumerate( tops):
            di = calcmatch(each,docsent)
            data.append(di)
            target.append(i)
            pos_sel.append([i,di])
    pos_selfname = sxpDataDUCSum.fdir +'//'+'pos_sel.pk'
    sxpReadFileMan.SaveObject([data, target,pos_sel],pos_selfname)
def MakePred():
    pos_selfname = sxpDataDUCSum.fdir +'//'+'pos_sel.pk'
    data, target, pos_sel =sxpReadFileMan.LoadObject(pos_selfname)
    print((np.max(target)))
    gnb = GaussianNB()
    test = np.array(list(range(0,14))).reshape(-1,1)
    data=np.array(data).reshape(-1,1)
    target= np.array(target).reshape(-1,1)
 #   print(data)
    print((data.shape))
    print((target.shape))
    model = gnb.fit(data, target)
    y_pred = model.predict(test)
    y_prob = model.predict_proba(test)
    print(y_pred)
    print(y_prob)
def calcmatch(sent,sentset):
    dl=[]
    for each in sentset:
        d = sxpJudgeCharacter.sentdist(sent,each)
        dl.append(d)
    i=np.argmax(dl)
    return i
def TestCalc():
    s = 'hello'
    ss =['hell','hello','worhel']
    print((calcmatch(s,ss)))

def TestPickle():
 #   pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_2.txt.pk'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_4.pk'
 #   pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2063.xhtml_2.pickle'
    pk = r'E:\pythonworknew\code\sentencerank\test\duc2002single\single_papers_pk\AP880217-0100.pk'

    TestRawSrc()
    ss= GetTopkFromRaw('AP880217-0100')
    print((len(ss)))
    sxptxt = sxpReadFileMan.LoadObject(pk)
    remove_stopwords=1
    iteration_times=20
    print('-----------TOP 100------------------')
    allsent = sxptxt.sentence_textset
    tops = GetMaxword(allsent)
    i=0
    for eachs in tops:

        print(('-----',i, eachs))
        i = i + 1
    print('-----------End model---------------')

    print('-----------This SmallSent model---------------')
    model= WordNetwork(sxptxt,remove_stopwords=1,iteration_times=30)

##    topksent = 10
##    tops = model.OutPutTopKSent(topksent,1,-1)
    topksent = 10
    useabstr = 0
    maxwords = 100
    strictmax=0
    tops = model.OutPutTopKSent(topksent,useabstr,maxwords,strictmax)
    i = 0
    for eachs in tops:
        print('-----------------')
        print((i, eachs))
        i = i + 1
    print('-----------End This Smallworld Model Top 10---------------')
    print('------------All Hits weight--------')
    model.TestHits()
    print('------------End Hits weight--------')


    print('------------All Hits Hybrid weight--------')
    model.TestHitsHybrid()
    print('------------End  Hybrid  weight--------')



    print('------------All PageRank Hybrid word-sentence, similarity weight--------')
    model.TestPageRank()
    print('------------End PageRank weight--------')
def TestDUCModel():
    graphid = 'AP880217-0100'
    pk = r'E:\pythonworknew\code\sentencerank\test\duc2002single\single_papers_pk\%s.pk'%(graphid)
    TestRawSrc(graphid)
    ss= GetTopkFromRaw(graphid)
    print((len(ss)))
    sxptxt = sxpReadFileMan.LoadObject(pk)
    remove_stopwords=1
    iteration_times=20
    print('-----------TOP 100------------------')
    allsent = sxptxt.sentence_textset
    tops = GetMaxword(allsent)
    i=0
    for eachs in tops:

        print(('-----',i, eachs))
        i = i + 1
    print('-----------End model---------------')

    print('-----------This SmallSent model---------------')

    model= WordNetwork(sxptxt,remove_stopwords=1,iteration_times=100, mode='wd_ss')
    all = model.OutputAllSentWeight()
    for each in all:
        print(('---------',each))
    words = model.OutPutTopKWord()
    for each in words:
        print((each,))
def TestACL():
    graphid= "0000"
    pk = r'E:\pythonworknew\code\textsum\test\acl2014\papers_pk\inc\%s.pk' % (graphid)

    sxptxt = sxpReadFileMan.LoadObject(pk)
    remove_stopwords=0
    iteration_times=20
    print('-----------TOP 100------------------')
    allsent = sxptxt.sentence_textset
    tops = GetMaxword(allsent)
    i=0
    for eachs in tops:

        print(('-----',i, eachs))
        i = i + 1
    print('-----------End model---------------')

    print('-----------This WordNetwork model---------------')

    model= WordNetwork(sxptxt,remove_stopwords=0,iteration_times=100, mode='wd_ss')
    all = model.OutputAllSentWeight()
    i=1
    for each in all:
        print((i,'---------',each))
        i = i + 1
    words = model.OutPutTopKWord(100)
    for each in words:
        print((each,))
def TestDUCSingle():
    graphid= "AP880217-0100"
   # graphid="AP880228-0013"
    pk = r'E:\pythonworknew\code\textsum\test\duc2002single\single_papers_pk\%s.pk' % (graphid)
    TestRawSrc(graphid)
  #  sxptxt = sxpReadFileMan.LoadObject(pk)
    sxptxt = sxpDataDUCSum.LoadSingleDucData(graphid,usesub=True)
    remove_stopwords=0
    iteration_times=20
    print('-----------TOP 100------------------')
    allsent = sxptxt.sentence_textset
    tops = GetMaxword(allsent)
    i=0
    for eachs in tops:

        print(('-----',i, eachs))
        i = i + 1
    print('-----------End model---------------')

    print('-----------This WordNetwork model on DUC---------------')
    mode = "wd_ss"  # 0.5
    global_para['undirect'] = 0
    global_para['remove_stopwords'] = 0
    global_para['addseq'] = 0
    global_para['mode'] = 'wd_ss'
    global_para['alpha_beta'] = [0.5, 0.5]
    global_para['maxword'] = 100
    global_para['topksent'] = -1

    global_para['sent_dir'] = 'endfront_debug'
    global_para['transpose'] = False


  #  model= WordNetwork(sxptxt,undirect=undirect, remove_stopwords=0,iteration_times=30, mode='wd_ss')
    mode = "wd_ss"  # 0.5
    undirect = 0;
    remove_stopwords = 0;
    model = WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    print('---model.OutputAllSentWeight()------')
    all = model.OutputAllSentWeight()
    i=1
    for each in all:
        print((i,'---------',each))
        i = i + 1
    words = model.OutPutTopKWord(100)
    for each in words:
        print((each,))
    topksent = -1
    useabstr = 0

    strictmax = 0
    maxword = 100
    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    tops = MakeFullSent(graphid,tops)
    i=1
    print('this output will rerank the topk in their original order, final output topk of the OutPutTopKSent(topksent, useabstr, maxword, strictmax)--')
    for each in tops:
        print((i,'---------',each))
        i = i + 1
def MakeFullSent(graph_dict_fid,tops):
    fullst = sxpDataDUCSum.GetSentenceListFromFID(graph_dict_fid)
    fulltops = []
    for eachfull in fullst:
        for eacht  in tops:
            if eachfull.find(eacht)>-1:
                fulltops.append(eachfull)
                break
    return fulltops
def TestOneDUC():
    graphid = "AP880217-0100"
    # graphid="AP880228-0013"
    pk = r'E:\pythonworknew\code\textsum\test\duc2002single\single_papers_pk\%s.pk' % (graphid)
 #   TestRawSrc(graphid)

    sxptxt = sxpDataDUCSum.LoadSingleDucData(graphid)

    print('--------Raw---TOP 100------------------')
    allsent = sxptxt.sentence_textset
    tops = GetMaxword(allsent)
    i=0
    for eachs in tops:

        print(('-----',i, eachs))
        i = i + 1


    print('------final output topk of the model')
    topk = -1;
    tops = GetWordNetHybridEndFrontDebug(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0)
    i = 1
    for each in tops:
        print((i,'---------',each))
        i = i + 1
def GetWordNetHybridEndFrontDebug(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    global_para['undirect'] = undirect
    global_para['remove_stopwords'] = remove_stopwords
    global_para['addseq'] = 0
    global_para['mode'] = 'wd_ss'
    global_para['alpha_beta'] = [0.8, 0.2]
    global_para['maxword'] = maxword
    global_para['topksent'] = topk
    global_para['sent_dir'] = 'endfront_debug'
    global_para['transpose'] = False
    model = WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def GetWordNetHybrid(sxptxt, topk, maxword=100, remove_stopwords=0,undirect=0):
    mode = "wd_ss"  # 0.5
    global_para['undirect'] = undirect
    global_para['remove_stopwords'] = remove_stopwords
    global_para['addseq'] = 0
    global_para['mode'] = 'wd_ss'
    global_para['alpha_beta'] = [0.8, 0.2]
    global_para['maxword'] = maxword
    global_para['topksent'] = topk

    model = WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops


def GetWordNetHybridNoWord():
    topk=-1
    maxword = 300
    remove_stopwords =0
    undirect = 0
    graphid= "0000"

    pk = r'E:\pythonworknew\code\textsum\test\acl2014\papers_pk\inc\%s.pk' % (graphid)

    sxptxt = sxpReadFileMan.LoadObject(pk)
    mode = "wd_ss"  # 0.5


    global_para['undirect'] = undirect
    global_para['remove_stopwords'] = remove_stopwords
    global_para['addseq'] = 0
    global_para['mode'] = 'wd_ss'
    global_para['alpha_beta'] = [0.8, 0.2]
    global_para['maxword'] = maxword
    global_para['topksent'] = topk
    global_para['transpose'] = False;
    global_para['sent_dir']='frontfirst'
    model = WordNetwork(sxptxt, undirect=undirect, remove_stopwords=remove_stopwords, iteration_times=30,
                                        mode=mode)
    topksent = -1
    useabstr = 0

    strictmax = 0

    tops = model.OutPutTopKSent(topksent, useabstr, maxword, strictmax)
    return tops
def testnoword():
    tops=GetWordNetHybridNoWord()
    i=1
    for each in tops:
        print((i,'---------',each))
        i = i + 1
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    #TestPickle()
    #TestModel()
    #TestACL()
    #testnoword()
    TestDUCSingle() #20200514;
  #  TestOneDUC()#20200515
    #TestAll()
    # CollectSample()
#    MakePred()
    # TestCalc()
  #  TestPageRankMatrix()
