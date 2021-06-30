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
import time
import warnings

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice
import sxpKMeans
def clustermodels(X,dataparams,algorithm) :
    default_base = {'quantile': .3,
                    'eps': .3,
                    'damping': .9,
                    'preference': -200,
                    'n_neighbors': 10,
                    'n_clusters': 3}
    params = default_base.copy()
    params.update(dataparams)
    # estimate bandwidth for mean shift
    bandwidth = cluster.estimate_bandwidth(X, quantile=params['quantile'])

    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(
        X, n_neighbors=params['n_neighbors'], include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    # ============
    # Create cluster objects
    # ============
    ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
    two_means = cluster.MiniBatchKMeans(n_clusters=params['n_clusters'])
    ward = cluster.AgglomerativeClustering(
        n_clusters=2, linkage='ward',
        connectivity=connectivity)

    spectral = cluster.SpectralClustering(
        n_clusters=2, eigen_solver='arpack',
        affinity="nearest_neighbors")

    dbscan = cluster.DBSCAN(eps=params['eps'])
    affinity_propagation = cluster.AffinityPropagation(
        damping=params['damping'], preference=params['preference'])
    average_linkage = cluster.AgglomerativeClustering(
        linkage="average", affinity="cityblock",
        n_clusters=params['n_clusters'], connectivity=connectivity)
    birch = cluster.Birch(n_clusters=params['n_clusters'])
    gmm = mixture.GaussianMixture(
        n_components=params['n_clusters'], covariance_type='full')
#    clustering_algorithms = (
#        ('MiniBatchKMeans', two_means),
#        ('AffinityPropagation', affinity_propagation),
#        ('MeanShift', ms),
#        ('SpectralClustering', spectral),
#        ('Ward', ward),
#        ('AgglomerativeClustering', average_linkage),
#        ('DBSCAN', dbscan),
#        ('Birch', birch),
#        ('GaussianMixture', gmm)
#    )
    sxpkmeans = sxpKMeans.sxpKmeans(params['n_clusters'])
    clustering_algorithms ={}
    clustering_algorithms['MiniBatchKMeans']=two_means
    clustering_algorithms['AffinityPropagation']=affinity_propagation
    clustering_algorithms['MeanShift']=ms
    clustering_algorithms['SpectralClustering']=spectral
    clustering_algorithms['Ward']=ward
    clustering_algorithms['AgglomerativeClustering']=average_linkage
    clustering_algorithms['DBSCAN']=dbscan
    clustering_algorithms['Birch'] = birch
    clustering_algorithms['GaussianMixture']=gmm
    clustering_algorithms['sxpkmeans'] = sxpkmeans

    return clustering_algorithms[algorithm]

def clusterby(X,nc=2,algorithm="MiniBatchKMeans"):
#    X = StandardScaler().fit_transform(X)
    dataparams ={
        'n_clusters':nc
    }
    model = clustermodels(X,dataparams,algorithm)


    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="the number of connected components of the " +
                    "connectivity matrix is [0-9]{1,2}" +
                    " > 1. Completing it to avoid stopping the tree early.",
            category=UserWarning)
        warnings.filterwarnings(
            "ignore",
            message="Graph is not fully connected, spectral embedding" +
                    " may not work as expected.",
            category=UserWarning)
        model.fit(X)


        if hasattr(model, 'labels_'):
            y_pred = model.labels_.astype(np.int)
        else:
            y_pred = model.predict(X)
        return y_pred


def run_test(datasets,clustermodels,fname='cluster_algorithm.jpg'):
    # ============
    # Set up cluster parameters
    # ============
    plt.figure(figsize=(9 * 2 + 3, 12.5))
    plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                        hspace=.01)

    pred_list=[]
    for i_dataset, (dataset, algo_params) in enumerate(datasets):
        # update parameters with dataset-specific values

        X, y = dataset

        # normalize dataset for easier parameter selection
        X = StandardScaler().fit_transform(X)



        clustering_algorithms = clustermodels(X,  algo_params)
        print(i_dataset)

        for name, algorithm in clustering_algorithms:
            print(name)
            t0 = time.time()

            # catch warnings related to kneighbors_graph
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="the number of connected components of the " +
                    "connectivity matrix is [0-9]{1,2}" +
                    " > 1. Completing it to avoid stopping the tree early.",
                    category=UserWarning)
                warnings.filterwarnings(
                    "ignore",
                    message="Graph is not fully connected, spectral embedding" +
                    " may not work as expected.",
                    category=UserWarning)
                algorithm.fit(X)

            t1 = time.time()
            if hasattr(algorithm, 'labels_'):
                y_pred = algorithm.labels_.astype(np.int)
            else:
                y_pred = algorithm.predict(X)
            print((type(y_pred[0])))
            pred_list.append((i_dataset,name,y_pred))
    return pred_list