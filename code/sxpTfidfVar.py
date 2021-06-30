from __future__ import unicode_literals, division
#-------------------------------------------------------------------------------
# Name:        sxpFenciMakeTFIDF
# Purpose:
#
# Author:      sunxp
#
# Created:     07-04-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re
import pickle

from sklearn.utils.validation import check_is_fitted, check_array, FLOAT_DTYPES
from sklearn.preprocessing import normalize
import scipy.sparse as sp


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse import csr_matrix
from sxpFenciMakeTFIDF import sxpTFIDF,SegStrComplex

class DTFIPF(TfidfTransformer):

    def __init__(self):

        TfidfTransformer.__init__(self)

        self.tfidfmode = 'tfidf'

    def run(self):
        print('DTF-IPF is running...')
    def setmode(self,mode='tf_ief',rif = 0.5,ripf=0.3):
        self.tfidfmode = mode#'tfief'
        self.rif = 0.5
        self.ripf = 0.3
    def fit(self, X, y=None):
        """Learn the idf vector (global term weights)

        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
            a matrix of term/token counts
        """
        X = check_array(X, accept_sparse=('csr', 'csc'))
        if not sp.issparse(X):
            X = sp.csr_matrix(X)
        dtype = X.dtype if X.dtype in FLOAT_DTYPES else np.float64

        if self.use_idf:
            n_samples, n_features = X.shape
            df = _document_frequency(X).astype(dtype)

            # perform idf smoothing if required
            df += int(self.smooth_idf)
            n_samples += int(self.smooth_idf)

            # log+1 instead of log makes sure terms with zero idf don't get
            # suppressed entirely.
            if self.tfidfmode == 'tfidf':
                idf = np.log(n_samples / df) + 1
            if self.tfidfmode == 'tfief':
                idf = np.exp(-1*df/n_samples)
            if self.tfidfmode == 'dtfipf':
                idf = np.power(n_samples / df,self.ripf)
            self._idf_diag = sp.diags(idf, offsets=0,
                                      shape=(n_features, n_features),
                                      format='csr',
                                      dtype=dtype)

        return self

    def transform(self, X, copy=True):
        """Transform a count matrix to a tf or tf-idf representation

        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
            a matrix of term/token counts

        copy : boolean, default True
            Whether to copy X and operate on the copy or perform in-place
            operations.

        Returns
        -------
        vectors : sparse matrix, [n_samples, n_features]
        """
        X = check_array(X, accept_sparse='csr', dtype=FLOAT_DTYPES, copy=copy)
        if not sp.issparse(X):
            X = sp.csr_matrix(X, dtype=np.float64)

        n_samples, n_features = X.shape

        if self.sublinear_tf:
            np.log(X.data, X.data)
            X.data += 1
        if self.tfidfmode == 'dtfipf':
                X.data = np.power(X.data,self.rif)
        if self.use_idf:
            check_is_fitted(self, '_idf_diag', 'idf vector is not fitted')

            expected_n_features = self._idf_diag.shape[0]
            if n_features != expected_n_features:
                raise ValueError("Input has n_features=%d while the model"
                                 " has been trained with n_features=%d" % (
                                     n_features, expected_n_features))
            # *= doesn't work
            X = X * self._idf_diag

        if self.norm:
            X = normalize(X, norm=self.norm, copy=False)

        return X
def _document_frequency(X):
    """Count the number of non-zero values for each feature in sparse X."""
    if sp.isspmatrix_csr(X):
        return np.bincount(X.indices, minlength=X.shape[1])
    else:
        return np.diff(X.indptr)

def MakeTFIDFForCorpus(docset,tfidfmode='tfidf'):
    print('begin to load and fenci file',len(docset))
    corpus = []
    sxptfidf = sxpTFIDF()
    for docstr in docset:
    #****************Fenci*****************
       segcontent = SegStrComplex(docstr)
      # print segcontent
    #**************************************
       corpus.append(segcontent)
    #****************MakeTFIDF*****************
    print('begin to make tfidf',len(corpus))
 #   vectorizer = CountVectorizer(stop_words=None)
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             token_pattern = '(?u)\\b\S+\\b',\
                             stop_words = None)
    #transformer = TfidfTransformer()
    #here is what is my TFIDF version
    if tfidfmode == 'tfidf':
        transformer = DTFIPF()
    if tfidfmode == 'tfief':
        transformer = DTFIPF()
        transformer.setmode('tfief')
    if tfidfmode == 'dtfipf':
        transformer = DTFIPF()
        transformer.setmode('dtfipf',rif = 0.5,ripf=0.3)

    sxptfidf.ct =vectorizer.fit_transform(corpus)#ct
    sxptfidf.vectorizer = vectorizer
    sxptfidf.tfidf = transformer.fit_transform(sxptfidf.ct)#tf-idf matrix
    sxptfidf.word = vectorizer.get_feature_names()  #所有文本的关键字
    sxptfidf.tfidftransformer = transformer
##    for w in sxptfidf.word:
##        print w
##    sxptfidf.weight = sxptfidf.tfidf.toarray()
    print('finished')
    return sxptfidf
def TestKeywordQueryOnTFIDF(keywordquery,sxptfidf):
    qv = sxptfidf.vectorizer.transform(keywordquery);
    a = np.array(qv > 0);
    print(a)
    print((list(zip(*np.nonzero(qv)))))
    print((np.nonzero(qv)))
    print((np.nonzero(qv)[1]))
    cn = np.nonzero(qv)[1]
    test_tfidf = sxptfidf.tfidftransformer.transform(qv)
    print(test_tfidf)
    print((sxptfidf.tfidf.shape))
    print((sxptfidf.tfidf[0, cn]))
    print((sxptfidf.tfidf[1,cn]))
    print((np.sum(sxptfidf.tfidf[0,cn])))
    print((np.sum(sxptfidf.tfidf[1, cn])))
    r = np.sum(sxptfidf.tfidf[:, cn], 1)
    print(r)
#    print('tfidf',test_tfidf,test_tfidf.shape)

    return r;
def TestTFIDF():
    docset = ['hello this is a U.S. test, and we are 你好 going to  let the test 100 run', 'we can make a simple analysis in this work']
    seg = SegStrComplex(docset[0])
    print(seg)
    sxptfidf = MakeTFIDFForCorpus(docset,tfidfmode='dtfipf')
    kn = sxptfidf.GetKeywordCount()
    for i in range(kn):
        print(sxptfidf.GetKeyword(i))
        #print type(sxptfidf.GetCTCol(i))
    qy =['hello this']
    print((TestKeywordQueryOnTFIDF(qy,sxptfidf)))
def main():
    TestTFIDF()
if __name__ == '__main__':
    main()