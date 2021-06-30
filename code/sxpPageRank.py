__author__ = 'a'
#-------------------------------------------------------------------------------
# Name:        sxpDataDucMultSum.py
# Purpose:
#
# Author:      sunxp
#
# Created:     23/10/2018
# Copyright:   (c) sunxp 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
from numpy import *
import numpy as np
from scipy.sparse import csr_matrix
def pagerank(M,alpha=0.85):
    N = M.shape[0]
    alpha, max_iter, S_S, x, per, dangling_weights, is_dangling = PreparePageRankMatrix(M, alpha=alpha, max_iter=20,
                                                                                        p=None, alreadysym=True)
    i = 0
    tol = 1.0e-6

    for _ in range(max_iter):
        xlast = x.copy()
        sw = sum(xlast.T[is_dangling])
        x = alpha * xlast * S_S + alpha * sw * dangling_weights + (1 - alpha) * per
        i = i + 1
        #        x = alpha * M*x  + (1 - alpha) * p
        err = sum(abs(x - xlast))
        if err < N * tol:
            break

    s = x.T
    return s


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