import numpy as np

def computeclosenessv0(keywordseq,wd_dist):
    global_one = []
    for w in wd_dist[keywordseq[0]]:
        global_one.append(w)
    gd = 0;
    for i,eachkey in enumerate(keywordseq):
        if i == 0:
            continue
        w = wd_dist[eachkey]
        d = closenessv0(global_one,w)
        for each in w:
            global_one.append(each)
        gd = gd + d;
    return gd;
def computecloseness(keywordseq,wd_dist,L):
    global_one = []
    for w in wd_dist[keywordseq[0]]:
        global_one.append(w)
    gd = 0;
    for i,eachkey in enumerate(keywordseq):
        if i == 0:
            continue
        w = wd_dist[eachkey]
        d = closeness(global_one,w,L)
        for each in w:
            global_one.append(each)
        gd = gd + d;
    return gd;

def computeclosenesstwo(keywordseq,wd_dist,L,version='v2'):

    gd = [];
    n = len(keywordseq)
    all_dual_sent_score = np.zeros((int(L), 1))
    for i in range(n-1):
        eachkey = keywordseq[i]
        w = wd_dist[eachkey]
        pw = keywordseq[i+1]
        nwdist = wd_dist[pw]
        if version == 'v1':
            d,dual_sent_score = closenesstwo(w,nwdist,L,symm=True)
        if version == 'v2':
            d,dual_sent_score = closenessv2(w,nwdist,L,symm=False)
        if version == 'v3':
            d,dual_sent_score = closenessv3(w, nwdist, L)
        if version == 'v4':
            d,dual_sent_score = closenessv4(w,nwdist,L,version = 'avg')

        if version == 'v5':
            d,dual_sent_score  = closenessv5(w,nwdist,L,version = 'sum')
        if version == 'v6':
            d,dual_sent_score = closnesscovertwo(w,nwdist,L,version = 'sum')
        if version == 'bv7':
            d,dual_sent_score = closnesscovertwobias(w,nwdist,L,version = 'sum')
        all_dual_sent_score = all_dual_sent_score + dual_sent_score
        gd.append(d)
#    print(gd)
    return np.sum(gd)/(1.0),all_dual_sent_score
def computekeydistfeature(w, L):
    coverlist = []
    m = len(w)
    if m == 0:
        coverlength = 0
        c1 = 0
        coverlist.append(c1)
        span = 0
        dens_L = 0
        cov_L = 0

    if m == 1:
        coverlength = 1
        c1 = 1.0 / L
        coverlist.append(c1)
        span = 0
        dens_L = m*1.0/L
        cov_L = span*1.0/L
    if m > 1:
        for i in range(m - 1):
            m1 = w[i]
            m2 = w[i + 1]
            d = m2 - m1
            coverlist.append(d)
        span = w[-1] - w[0]
        dens_L = m*1.0/L
        cov_L = m*1.0/L
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist + np.abs(d - avgd)
    if len(coverlist) <= 1:
        evendist = 0;
    else:
        evendist = 1.0 - evendist / m / L

    feature = {}
    feature['density']=density
    feature['evendist']=evendist
    feature['dens_L']=dens_L
    feature['cov_L']=cov_L
    feature['m']=m
    return feature
def denscoverscore(keywordseq,wd_dist,L,version='dens'):
    gd = [];
    n = len(keywordseq)
    dual_sent_score = np.zeros((int(L),1))
    for i in range(n):
        eachkey = keywordseq[i]
        w = wd_dist[eachkey]
        feature = computekeydistfeature(w,L)
        gd.append([feature['m'],feature['dens_L'],feature['cov_L'],feature['evendist']])
        for each in w:
            dual_sent_score[each] = dual_sent_score[each]+1

    sa = np.array(gd)
    avgv =np.mean(sa,0)
    maxv = np.max(sa,0)
    avgdens = avgv[1]
    avgspan = avgv[2]
    avgeven = avgv[3]
    if version == 'dens':
        return avgdens,dual_sent_score
    if version == 'cover':
        return avgspan, dual_sent_score
    if version == 'denscover':
        return  avgdens+avgspan, dual_sent_score
    if version == 'denseven':
        return avgeven + avgdens, dual_sent_score
    if version == 'even':
        return avgeven, dual_sent_score
    return None,None
def dualcomputeclosenesstwo(keywordseq,wd_dist,L,version='v2'):

    gd = [];
    n = len(keywordseq)
    dual_sent_score = np.zeros((int(L),1))
    for i in range(n-1):
        eachkey = keywordseq[i]
        w = wd_dist[eachkey]
        pw = keywordseq[i+1]
        nwdist = wd_dist[pw]

        if version == 'v1':
            d,sent_score  = closenesstwo(w,nwdist,L,symm=True)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'v2':
            d,sent_score  = closenessv2(w,nwdist,L,symm=False)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'v3':
            d,sent_score  = closenessv3(w, nwdist, L)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'v4':
            d,sent_score  = closenessv4(w,nwdist,L,version = 'avg')
            dual_sent_score = dual_sent_score + sent_score
        if version == 'v5':
            d,sent_score = closenessv5(w,nwdist,L,version = 'sum')
            dual_sent_score = dual_sent_score + sent_score
        if version == 'v6':

            d,sent_score = closnesscovertwo(w, nwdist, L, version='sum')
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6':
            cversion = 'sum'
            closetype = 'avg'
            d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,closetype=closetype,exclusion='yes')
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_dcd':
            cversion = 'sum'
            d,sent_score = singledirectedcloseness(w, nwdist, L, version=cversion,exclusion='no')
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_fcd':
            cversion = 'sum'
            d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,exclusion='no')
            dual_sent_score = dual_sent_score + sent_score

        if version == 'dual_v6_noexclusion':
            cversion = 'sum'
            exclusion = 'no'
            d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,closetype='max',exclusion = exclusion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meanclose':
            cversion = 'sum'
            exclusion = 'yes'
            closetype = 'avg'
            d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meanclose_v1':
            cversion = 'sum'
            exclusion = 'yes'
            closetype = 'avg'
            d,sent_score = dualclosnesscovertwoV1(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_even_v1':
            cversion = 'even'
            exclusion = 'yes'
            closetype = 'avg'
            d,sent_score = dualclosnesscovertwoV1(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_reci':
            cversion = 'sum'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'reci'
            d,sent_score = dualclosnesscovertwoV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score

        if version == 'dual_v6_exclusion_meannormclose_v2_covr':
            cversion = 'sum'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'covr'
            d,sent_score = dualclosnesscovertwoV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score


        if version == 'dual_v6_exclusion_meannormclose_v2_covr_nodense':
            cversion = 'nodens'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'covr'
            d,sent_score = dualclosnesscovertwoV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_reci_nodense':
            cversion = 'nodens'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'reci'
            d,sent_score = dualclosnesscovertwoV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_reci_onlyclose':
            cversion = 'close'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'reci'
            d, sent_score = dualclosnesscovertwoV2(w, nwdist, L, version=cversion, closetype=closetype,
                                                   exclusion=exclusion,
                                                   normmethod=normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_covr_onlyclose':
            cversion = 'close'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'covr'
            d, sent_score = dualclosnesscovertwoV2(w, nwdist, L, version=cversion, closetype=closetype,
                                                   exclusion=exclusion,
                                                   normmethod=normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_reci_onlyself':
            cversion = 'self'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'reci'
            d, sent_score = dualclosnesscovertwoV2(w, nwdist, L, version=cversion, closetype=closetype,
                                                   exclusion=exclusion,
                                                   normmethod=normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_exclusion_meannormclose_v2_covr_onlyself':
            cversion = 'self'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'covr'
            d, sent_score = dualclosnesscovertwoV2(w, nwdist, L, version=cversion, closetype=closetype,
                                                   exclusion=exclusion,
                                                   normmethod=normmethod)
            dual_sent_score = dual_sent_score + sent_score

        if version == 'dual_v6_noeven_reci':
            cversion= 'noeven'
            exclusion = 'yes'
            closetype ='avg'
            normmethod = 'reci'
            #d,sent_score = dualclosnesscovertwo(w,nwdist,L,version = cversion,closetype = closetype)
            d,sent_score = dualclosnesscovertwoV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_nodens_reci':
            cversion = 'nodens'
            exclusion = 'yes'
            closetype = 'avg'
            normmethod = 'reci'
            d,sent_score = dualclosenesscoverV2(w,nwdist,L,version = cversion,closetype=closetype,exclusion = exclusion,
                                                  normmethod = normmethod)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_directed':
            cversion = 'sum'
            d,sent_score = singledirectedcloseness(w,nwdist,L,version = cversion)
            dual_sent_score = dual_sent_score + sent_score
        if version == 'dual_v6_backdirected':
            cversion = 'sum'
            d,sent_score = singlebackdirectedcloseness(w,nwdist,L,version = cversion)
            dual_sent_score = dual_sent_score + sent_score

        if version == 'bv7':
            d = closnesscovertwobias(w,nwdist,L,version = 'sum')
        gd.append(d)
#    print(gd)
    docscore = np.sum(gd)/1.0 #2020 best
    #if len(gd)==0:
    #    docscore = 0;
    #else:
    #    docscore = np.max(gd) # I try to see if max is better no way, using max will get a worse
    return docscore,dual_sent_score
def computeclosenessbiascover(keywordseq,wd_dist,L,version='v2'):

    gd = [];
    n = len(keywordseq)

    for i in range(n-1):
        eachkey = keywordseq[i]
        w = wd_dist[eachkey]
        pw = keywordseq[i+1]
        nwdist = wd_dist[pw]
        if version == 'v1':
            d = closenesstwo(w,nwdist,L,symm=True)
        if version == 'v2':
            d = closenessv2(w,nwdist,L,symm=False)
        if version == 'v3':
            d = closenessv3(w, nwdist, L)
        if version == 'v4':
            d = closenessv4(w,nwdist,L,version = 'avg')
        if version == 'v5':
            d = closenessv5(w,nwdist,L,version = 'sum')
        if version == 'v6':
            d = closnesscovertwo(w,nwdist,L,version = 'sum')
        if version == 'v7':
            d = closnesscovertwobias(w,nwdist,L,version = 'sum')
        gd.append(d)
#    print(gd)
    return np.sum(gd)/(1.0);

def testcomputedist(keywordseq,wd_dist,L,version='v2'):
    gd = [];
    n = len(keywordseq)

    for i in range(n-1):
        eachkey = keywordseq[i]
        w = wd_dist[eachkey]
        pw = keywordseq[i+1]
        nwdist = wd_dist[pw]

        if version == 'v4':
            d = testclosenessv4(w, nwdist, L)
        gd.append(d)
    return gd;

def computeclosenesstwo_sym(keywordseq,wd_dist,L,version='v2'):

    gd = [];
    n = len(keywordseq)

    for i in range(n-1):
        eachkey = keywordseq[i][0]
        symm = keywordseq[i][1]
        w = wd_dist[eachkey]
        pw = keywordseq[i+1]
        nwdist = wd_dist[pw]
        if version == 'v1':
            d = closenesstwo(w,nwdist,L,symm=='symm')
        if version == 'v2':
            d = closenessv2(w, nwdist, L, symm == 'symm')
        gd.append(d)
    return np.sum(gd)/(1.0);
def closenessv0(v1, v2):
    md = []
    for c2 in v2:
        m = np.Inf
        for c1 in v1:
            d = np.abs(c2-c1)
            if d < m:
                m = d
        md.append(m)
    if len(md)==0:
        md.append(np.Inf)
    d = np.sum(md)
    return d
def closenesstwo(v1,v2,L,symm=True):
    md = []
    tn = len(v1)
    td = 0;
    bases = 0;

    sent_score = np.zeros((int(L),1))
    if len(v1)>=1:
        bases = bases + 1;
    for c1 in v1:
        #        D = L;
        m = L;
        sent_score[c1] =  sent_score[c1] + 1./m
        mc = 0
        for c2 in v2:
            d = np.abs(c2 - c1)
            if d < m:
                m = d
                mc = c2
        sent_score[mc] =  sent_score[mc] + 1./m
        md.append(m+1)
    if symm:
        if len(v2)>=1:
            bases = bases + 1;
        for c2 in v2:
            #        D = L;
            m = L;
            mc = 0
            sent_score[c2] = sent_score[c2] + 1. / m
            for c1 in v1:
                d = np.abs(c2 - c1)
                if d < m:
                    m = d
                    mc = c1

            sent_score[mc] = sent_score[mc] + 1./m
            md.append(m+1)


    if len(md) == 0:
        md.append(L * L)
    td = np.sum(md)

    T = L * L;
    if td == 0:
        td = 0;
    return bases +1.0 * (T - td) / T, sent_score
    # if td is smaller but not zero, means that there is closer or fewer.
    # but we see that fewer ones is not a good one, closer one is a
    # the more closer is better.
    # for exa
    #   return 1.0*td/T;
def closeness(v1, v2,L):
    md = []
    tn = len(v1)
    td = 0;
    for c2 in v2:
#        D = L;
        m = L;
        for c1 in v1:
            d = np.abs(c2-c1)
            if d < m:
                m = d
        md.append(m)
        td = td + m+1.0;


    for c1 in v1:
        #        D = L;
        m = L;
        for c2 in v2:
            d = np.abs(c2 - c1)
            if d < m:
                m = d
        md.append(m)
        td = td + m+1.0;
    if len(md)==0:
        md.append(L*L)
    d = np.sum(md)

    T = L*L;
    if td == 0:
        td = 0;
    return 1.0*(T-td)/T;
    #if td is smaller but not zero, means that there is closer or fewer.
    #but we see that fewer ones is not a good one, closer one is a
    #the more closer is better.
    #for exa
    #   return 1.0*td/T;

def closenessv1(v1, v2, L):
    md = []
    tn = len(v1)
    td = L * L;
    for c2 in v2:
        #        D = L;
        m = L;
        for c1 in v1:
            d = np.abs(c2 - c1)
            if d < m:
                m = d
        md.append(m)
        td = td - m - 1;

    for c1 in v1:
        #        D = L;
        m = L;
        for c2 in v2:
            d = np.abs(c2 - c1)
            if d < m:
                m = d
        md.append(m)
        td = td - m - 1;
    if len(md) == 0:
        md.append(L * L)
    d = np.sum(md)
    return td
def computeworddistscore(keywordseq,wd_dist):
    t = 0.0
    for eachkey in keywordseq:
        w = wd_dist[eachkey]
        a = np.array(w)
        d = len(w)*1.0;
        s = np.sum(a)/d
        t = t + s;
    return t
def closenessv2(v1,v2,L,symm=True):
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))
    bases = 0;
    if len(v1)>=1:
        bases = bases + 1;
    dual_sent_score = np.zeros((int(L),1))
    for c1 in v1:
        #        D = L;
        m = L;
        mi=-1;
        dual_sent_score[c1] = dual_sent_score[c1] + 1.0 / m
        for i,c2 in enumerate(v2):
            d = np.abs(c2 - c1)
            if v2i[i]==1:
                continue;
            if d < m:
                m = d
                mi = i
        dual_sent_score[mi] = dual_sent_score[mi] + 1.0/m
        # if mi >=0:
        #     v2i[mi]=1
        md.append(m)

    if symm:
        if len(v2)>=1:
            bases = bases + 1;
        n1 = len(v1)
        v2i = np.zeros((n1, 1))
        for c2 in v2:
            #        D = L;
            m = L;
            mi = -1;
            dual_sent_score[c2] = dual_sent_score[c2] + 1.0 / m
            for i, c1 in enumerate(v1):
                if v2i[i] == 1:
                    continue;
                d = np.abs(c2 - c1)
                if d < m:
                    m = d
                    mi = i;
            dual_sent_score[mi] = dual_sent_score[mi] + 1.0 / m
            if mi >= 0:
                v2i[mi] = 1
            md.append(m+1)


    if len(md) == 0:
        md.append(L * L)
    td = np.sum(md)

    T = L * L;
    if td == 0:
        td = 0;
    return bases +1.0 * (T - td) / T,dual_sent_score

def closenessv3(v1,v2,L):
    return closenessv2(v2,v1,L,symm=False)
def closenessv4(v1,v2,L,version='avg'):
    d1,sentscore1 = closenessv4oneside(v1,v2,L,version)
    d2,sentscore2 = closenessv4oneside(v2,v1,L,version)
    d = d1 + d2;
    s = sentscore1 + sentscore2
    return d,s
def closenessv5(v1,v2,L,version='sum'):
    d1,dual_sent_score1 = closenessv5oneside(v1,v2,L,version)
    d2,dual_sent_score2 = closenessv5oneside(v2,v1,L,version)
    sent_score = (dual_sent_score1 + dual_sent_score2)/2
    d = d1 + d2;
    return d,sent_score
def closenessv4oneside(v1,v2,L,version='avg'):
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []

    for c1 in v1:
        #        D = L;
        m = L-1;
        mi=-1;
        sv2=-1

        for i,c2 in enumerate(v2):
            d = np.abs(c2 - c1)
            if v2i[i]==1:
                continue;
            if d < m:
                m = d*1.0;
                mi = i
                sv2 = c2;
        if mi == -1:
            m = L-1;
        else:
            v2i[mi]=1
        md.append(m)
        matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    td = np.sum(md)
    T = L * L;
    base = 0
    if len(v1)>0:
        base = base+1;
    if len(v2)>0:
        base = base+1;
    cd = base + 1.0 * (T - td) / T;
    if n1 == 0:
        avgt = 0
    else:
        avgt = base+1.0-td / n1/L;
    sumt = td /L;
    sent_score = np.zeros((int(L),1))
    if len(matchpair) ==0:
        return avgt,sent_score

    for (m,c1,sv2) in matchpair:
        if m == 0:
            s = 0;
        else:
            s = 1./m
        sent_score[c1,0] = sent_score[c1,0] + s
        sent_score[sv2,0] = sent_score[sv2,0] + s

    return avgt,sent_score
def closenessv5oneside(v1,v2,L,version='sum'):
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))
    sent_score = np.zeros((int(L), 1))
    matchpair = []

    for c1 in v1:
        #        D = L;
        m = L-1;
        mi=-1;
        sv2=-1
        sent_score[c1] = sent_score[c1]  + 1./m
        for i,c2 in enumerate(v2):
            d = np.abs(c2 - c1)
            if v2i[i]==1:
                continue;
            if d < m:
                m = d*1.0;
                mi = i
                sv2 = c2;

        if mi == -1:
            m = L-1;
            sent_score[mi] = sent_score[mi] + 1. / m
        else:
            v2i[mi]=1
        md.append(m)
        matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    td = np.sum(md)
    T = L * L;
    base = 0
    if len(v1)>0:
        base = base+1;
    if len(v2)>0:
        base = base+1;
    cd = base + 1.0 * (T - td) / T;
    if n1 == 0:
        avgt = 0
    else:
        avgt = base+1.0-td /T;
    sumt = td /L;
    print(td,T,avgt,td/T)
    return avgt,sent_score

#the problem here is that first the begining part should be better than behind part
#the second problem is about normalization factor between different papers.
#for example, if one paper has 100 sents, anthor has 1000 sents, then
#the distance for two consequtive sents is 0.01 and 0.001, so which one is better,
# the larger the better.
def testclosenessv4(v1,v2,L):
    dv1 = np.array(v1)*1.0 /L
    dv2 = np.array(v2)*1.0 /L

    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []
    if len(v2)>0:
        for c1 in v1:
            #        D = L;
            m = L+1;
            mi=-1;
            sv2=0

            for i,c2 in enumerate(v2):
                d = np.abs(c2 - c1)
                if v2i[i]==1:
                    continue;
                if d < m:
                    m = d*1.0;
                    mi = i
                    sv2 = c2;
            if mi == -1:
                m = L +1;
            else:
                v2i[mi]=1
            md.append(m)
            matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    td = np.sum(md)
    T = L * L;
    base = 0
    if len(v1)>0:
        base = base+1;
    if len(v2)>0:
        base = base+1;
    cd = base + 1.0 * (T - td) / T;
    if n1 >0:
        avgt = base+1.0-td / n1/L;
    else:
        avgt = 0;
    sumt = td /L;

    dist_dict = {}
    dist_dict['cd'] = cd;
    dist_dict['t']=td;
    dist_dict['sumt'] = sumt;
    dist_dict['avgt'] = avgt;
    dist_dict['match']=matchpair
    return dist_dict

def closnesscovertwobias(v1,v2,L,version='sum'):
    d1,dual_sent_score1 = closenesscover(v1,v2,L,version='sum')
    d2,dual_sent_score2 = closenesscover(v2,v1,L,version='sum')

    u = (d1*d1+d2*d2)/2
    v = np.var([d1,d2])
    snr = np.log10(u/v)
   # print('closnesscovertwobias d1, d2,u,v,snr, score',d1, d2,u,v,snr,snr *(d1 + d2))
    sent_score = (dual_sent_score1 + dual_sent_score2)/2
    return snr *(d1 + d2), sent_score
def closenesscover(v1,v2,L,version='sum'):
    #this is the best score till 20200826
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []
    if len(v2)>0:
        for c1 in v1:
            #        D = L;
            m = L+1;
            mi=-1;
            sv2=0
            for i,c2 in enumerate(v2):
                d = np.abs(c2 - c1)
                if v2i[i]==1:
                    continue;
                if d < m:
                    m = d*1.0;
                    mi = i
                    sv2 = c2;
            if mi == -1:
                m = L +1;
                continue
            else:
                v2i[mi]=1 #this makes the v6 version best 20200826
                m = m + 1
            md.append(1./m)
            matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)

    sent_score = np.zeros((int(L),1))
    if len(md)==0:
        return 0,sent_score

    for (m,c1,sv2) in matchpair:
        sent_score[c1,0] = sent_score[c1,0] + 1./m
        sent_score[sv2,0] = sent_score[sv2,0] + 1. / m
    close = np.mean(md)
    m = len(md)
    coverlength=0
    coverlist=[]
    if m == 1:
        m1 = matchpair[0]
        coverlength = 1
        c1  = 1.0/m1[0]
        coverlist.append(c1)

    if m > 1:
        for i in range(m-1):
            m1 = matchpair[i]
            m2 = matchpair[i+1]
            c1 = 1.0/m1[0]
            c2 = 1.0/m2[0]
            d = m2[1]-m1[1]
            coverlist.append(d)
   # density = np.sum(coverlist)/L;
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist +np.abs(d-avgd)
    if len(coverlist)<=1:
        evendist = 0;
    else:
        evendist = 1.0-evendist / m/L

    wscore = 0.33*close + 0.33*density + 0.33*evendist
    #wscore = close * density * evendist #2020826 very poor performance
  #  print('wscore',wscore,'close',close,'density',density,'even',evendist)
   # print(wscore,close,density,evendist)
    return wscore,sent_score

def dualclosenesscover(v1,v2,L,version='sum',closetype='max',exclusion='yes'):
    #this is the best score till 20200826
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []

    if len(v2)>0:

        for c1 in v1:
            #        D = L;
            m = L+1;
            mi=-1;
            sv2=0
            for i,c2 in enumerate(v2):
                d = np.abs(c2 - c1)
                if v2i[i]==1:
                    continue;
                if d < m:
                    m = d*1.0;
                    mi = i
                    sv2 = c2;
            if mi == -1:
                m = L +1;
                continue
            else:
                if exclusion=='yes':
                    v2i[mi]=1 #this makes the v6 version best 20200826
                m = m + 1

            md.append(1./m)

            matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    sent_score = np.zeros((int(L),1))
    if len(md)==0:
        return 0,sent_score

    for (m,c1,sv2) in matchpair:
        sent_score[c1,0] = sent_score[c1,0] + 1./m
        sent_score[sv2,0] = sent_score[sv2,0] + 1. / m
    if closetype == 'max':
        close = np.max(md)
    if closetype == 'avg':
        close = np.mean(md)
    m = len(md)
    coverlength=0
    coverlist=[]
    if m == 1:
        m1 = matchpair[0]
        coverlength = 1
        c1  = 1.0/m1[0]
        coverlist.append(c1)

    if m > 1:
        for i in range(m-1):
            m1 = matchpair[i]
            m2 = matchpair[i+1]
            c1 = 1.0/m1[0]
            c2 = 1.0/m2[0]
            d = m2[1]-m1[1]
            coverlist.append(d)
   # density = np.sum(coverlist)/L;
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist +np.abs(d-avgd)
    if len(coverlist)<=1:
        evendist = 0;
    else:
      #  evendist = 1.0-evendist / m/L #this is the best eveness
        evendist = 1.0 - avgd / L # this is the test
    if version == 'sum':
        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'close':
        wscore = close
    if version == 'c1even':
        if len(v1)>=2:
            ceven = np.diff(v1).mean()
            evendist = 1.0-ceven /L
        else:
            evendist = 0

        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'noeven':
       #wscore = 0.5 * close + 0.5 * density
       #wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
       wscore = 0.5 * close +  0.5 * evendist
    if version == 'nodens':
       wscore = 0.5*close + 0.5*evendist
    #wscore = close * density * evendist #2020826 very poor performance
  #  print('wscore',wscore,'close',close,'density',density,'even',evendist)
   # print(wscore,close,density,evendist)
    return wscore,sent_score

def dualclosenesscoverV2(v1, v2, L, version='sum', closetype='avg', exclusion='yes', normmethod='reci'):
    #this is the best score till 20200826
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []

    if len(v2)>0:

        for c1 in v1:
            #        D = L;
            m = L+1;
            mi=-1;
            sv2=0
            for i,c2 in enumerate(v2):
                d = np.abs(c2 - c1)
                if v2i[i]==1:
                    continue;
                if d < m:
                    m = d*1.0;
                    mi = i
                    sv2 = c2;
            if mi == -1:
                m = L +1;
#                continue #this makes it different from v2old, one is 0.396827, another use continue is 0.40114
            else:
                if exclusion=='yes':
                    v2i[mi]=1 #this makes the v6 version best 20200826
                m = m + 1

            #md.append(1./m)
            if normmethod == 'reci':
                md.append(1. / m) # ub main version of dualclosenesscover, this has poor single performance
            if normmethod == 'covr':
                md.append(m/(L+1))
            matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    sent_score = np.zeros((int(L),1))
    if len(md)==0:
        return 0,sent_score

    for (m,c1,sv2) in matchpair:
        sent_score[c1,0] = sent_score[c1,0] + 1./m
        sent_score[sv2,0] = sent_score[sv2,0] + 1. / m
    if closetype == 'max':
        close = np.max(md)
    if closetype == 'avg':
        #close = np.mean(md)
        if normmethod == 'reci':
            close = np.mean(md)
        if normmethod == 'covr':
            close = 1-np.mean(md) #0.33
    m = len(md)
    coverlength=0
    coverlist=[]
    if m == 1:
        m1 = matchpair[0]
        coverlength = 1
        c1  = 1.0/m1[0]
        coverlist.append(c1)

    if m > 1:
        for i in range(m-1):
            m1 = matchpair[i]
            m2 = matchpair[i+1]
            c1 = 1.0/m1[0]
            c2 = 1.0/m2[0]
            d = m2[1] - m1[1]
            if normmethod == 'reci':
                se = 1./d
            if normmethod == 'covr':
                se = d / L  # 0.33

            coverlist.append(se)
   # density = np.sum(coverlist)/L;
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist +np.abs(d-avgd)
    if len(coverlist)<=1:
        evendist = 0;
    else:
      #  evendist = 1.0-evendist / m/L #this is the best eveness
      #  evendist = 1.0 - avgd / L # this is the test
    # close = np.mean(md)
        if normmethod == 'reci':
            evendist = np.mean(coverlist)
        if normmethod == 'covr':
            evendist = 1 - np.mean(coverlist)/L   # 0.33
    if version == 'sum':
        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'close':
        wscore = close
    if version == 'c1even':
        if len(v1)>=2:
            ceven = np.diff(v1).mean()
            evendist = 1.0-ceven /L
        else:
            evendist = 0

        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'self':
        wscore = evendist
    if version == 'noeven':
       #wscore = 0.5 * close + 0.5 * density
       #wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
       wscore = 0.5 * close +  0.5 * density
    if version == 'nodens':
       wscore = 0.5*close + 0.5*evendist
    #wscore = close * density * evendist #2020826 very poor performance
  #  print('wscore',wscore,'close',close,'density',density,'even',evendist)
   # print(wscore,close,density,evendist)
    return wscore,sent_score


def dualclosenesscoverV2old(v1, v2, L, version='sum', closetype='avg', exclusion='yes',normmethod='reci'):
   # print('dualclosenesscoverV2')
    # this is the best score till 20200826
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i = np.zeros((n2, 1))

    matchpair = []

    if len(v2) > 0:

        for c1 in v1:
            #        D = L;
            m = L + 1;
            mi = -1;
            sv2 = 0
            for i, c2 in enumerate(v2):
                d = np.abs(c2 - c1)
                if v2i[i] == 1:
                    continue;
                if d < m:
                    m = d * 1.0;
                    mi = i
                    sv2 = c2;
            if mi == -1:
                m = L + 1;
       #         continue
            else:
                if exclusion == 'yes':
                    v2i[mi] = 1  # this makes the v6 version best 20200826
                m = m + 1
            if normmethod == 'reci':
                md.append(1. / m) # ub main version of dualclosenesscover, this has poor single performance
            if normmethod == 'covr':
                md.append(m/(L+1))
            matchpair.append((m, c1, sv2))
    #   print(m,c1,sv2)
    sent_score = np.zeros((int(L), 1))
    if len(md) == 0:
        return 0, sent_score

    for (m, c1, sv2) in matchpair:
        sent_score[c1, 0] = sent_score[c1, 0] + 1. / m
        sent_score[sv2, 0] = sent_score[sv2, 0] + 1. / m
    if closetype == 'max':
        close = np.max(md)
    if closetype == 'avg':
        if normmethod == 'reci':
            close = np.mean(md)
        if normmethod == 'covr':
            close = 1-np.mean(md) #0.33
      # close = 1 - np.sum(md)/L #0.22
      #  close = np.mean(md)
    m = len(md)
    coverlength = 0
    coverlist = []
    if m == 1:
        m1 = matchpair[0]
        coverlength = 1
        c1 = 1.0 / m1[0]
        coverlist.append(c1)

    if m > 1:
        for i in range(m - 1):
            m1 = matchpair[i]
            m2 = matchpair[i + 1]
            c1 = 1.0 / m1[0]
            c2 = 1.0 / m2[0]
            d = m2[1] - m1[1]
            coverlist.append(d)
    # density = np.sum(coverlist)/L;
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist + np.abs(d - avgd)
    if len(coverlist) <= 1:
        evendist = 0;
    else:
        #  evendist = 1.0-evendist / m/L #this is the best eveness
        evendist = 1.0 - avgd / L  # this is the test
    if version == 'sum':
        wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
    if version == 'close':
        wscore = close
    if version == 'c1even':
        if len(v1) >= 2:
            ceven = np.diff(v1).mean()
            evendist = 1.0 - ceven / L
        else:
            evendist = 0

        wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
    if version == 'noeven':
        # wscore = 0.5 * close + 0.5 * density
        # wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
        #wscore =  close #
        #wscore = 0.5 * close + 0.5 * evendist #0.375106
       # wscore = 0.33 * close + 0.33 * density + 0.33 * evendist#0.387549
       # wscore = close #0.187467 md.append(1. / m) close = np.mean(md)
       # wscore = close*0.33 + 0.33*density + 0.33 * evendist#0.396827 md.append(1. / m) close = np.mean(md)
       # wscore = close * 0.33 + 0.33 * density + 0.33 * evendist  # 0.379797 md.append(m/(L+1))close = 1-np.mean(md) #0.33
        wscore = close # 0.331320 md.append(m/(L+1))close = 1-np.mean(md) #0.33
        # wscore = evendist #0.364530
    if version == 'nodens':
        wscore = 0.5 * close + 0.5 * evendist
    # wscore = close * density * evendist #2020826 very poor performance
    #  print('wscore',wscore,'close',close,'density',density,'even',evendist)
    # print(wscore,close,density,evendist)
    return wscore, sent_score


def dualclosenesscoverV1(v1,v2,L,version='sum',closetype='max',exclusion='yes'):
    #this is the best score till 20200826
    #in V1, I remove using len(v2) = 0 to judge
    md = []
    n1 = len(v1)
    td = L * L;
    n2 = len(v2)
    v2i =np.zeros((n2,1))

    matchpair = []



    for c1 in v1:
        #        D = L;
        m = L+1;
        mi=-1;
        sv2=0
        for i,c2 in enumerate(v2):
            d = np.abs(c2 - c1)
            if v2i[i]==1:
                continue;
            if d < m:
                m = d*1.0;
                mi = i
                sv2 = c2;
        if mi == -1:
            m = L +1;
        else:
            if exclusion=='yes':
                v2i[mi]=1 #this makes the v6 version best 20200826
            m = m + 1
        md.append(1./m)

        matchpair.append((m,c1,sv2))
     #   print(m,c1,sv2)
    sent_score = np.zeros((int(L),1))
    if len(md)==0:
        return 0,sent_score

    for (m,c1,sv2) in matchpair:
        sent_score[c1,0] = sent_score[c1,0] + 1./m
        sent_score[sv2,0] = sent_score[sv2,0] + 1. / m
    if closetype == 'max':
        close = np.max(md)
    if closetype == 'avg':
        close = np.mean(md)
    m = len(md)
    coverlength=0
    coverlist=[]
    if m == 1:
        m1 = matchpair[0]
        coverlength = 1
        c1  = 1.0/m1[0]
        coverlist.append(c1)

    if m > 1:
        for i in range(m-1):
            m1 = matchpair[i]
            m2 = matchpair[i+1]
            c1 = 1.0/m1[0]
            c2 = 1.0/m2[0]
            d = m2[1]-m1[1]
            coverlist.append(d)
   # density = np.sum(coverlist)/L;
    density = m / L;
    avgd = np.mean(coverlist)
    evendist = 0
    for d in coverlist:
        evendist = evendist +np.abs(d-avgd)
    if len(coverlist)<=1:
        evendist = 0;
    else:
        #evendist = 1.0-evendist / m/L This is the before 03 29 best version for
        evendist = 1.0 - avgd / L  # this is the test
    if version == 'sum':
        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'close':
        wscore = close
    if version == 'even':
        wscore = evendist
    if version == 'c1even':
        if len(v1)>=2:
            ceven = np.diff(v1).mean()
            evendist = 1.0-ceven /L
        else:
            evendist = 0
        wscore = 0.33*close + 0.33*density + 0.33*evendist
    if version == 'noeven':
       #wscore = 0.5 * close + 0.5 * density
       wscore = 0.33 * close + 0.33 * density + 0.33 * evendist
    if version == 'nodens':
       wscore = 0.5*close + 0.5*evendist
    #wscore = close * density * evendist #2020826 very poor performance
  #  print('wscore',wscore,'close',close,'density',density,'even',evendist)
   # print(wscore,close,density,evendist)
    return wscore,sent_score

def closnesscovertwo(v1,v2,L,version='sum'):
    d1,sentscore1 = closenesscover(v1,v2,L,version='sum')
    d2,sentscore2 = closenesscover(v2,v1,L,version='sum')
   # print(d1,d2)
    sent_score = (sentscore1 + sentscore2) / 2.0
    return (d1+d2)/2,sent_score
def dualclosnesscovertwo(v1,v2,L,version='sum',closetype='max',exclusion='yes'):
    d1,sentscore1 = dualclosenesscover(v1,v2,L,version=version,closetype=closetype,exclusion=exclusion)
    d2,sentscore2 = dualclosenesscover(v2,v1,L,version=version,closetype=closetype,exclusion=exclusion)
    sent_score = (sentscore1 + sentscore2)/2.0
   # print(d1,d2)
    return (d1+d2)/2, sent_score
def dualclosnesscovertwoV1(v1,v2,L,version='sum',closetype='max',exclusion='yes'):
    d1,sentscore1 = dualclosenesscoverV1(v1,v2,L,version=version,closetype=closetype,exclusion=exclusion)
    d2,sentscore2 = dualclosenesscoverV1(v2,v1,L,version=version,closetype=closetype,exclusion=exclusion)
    sent_score = (sentscore1 + sentscore2)/2.0
   # print(d1,d2)
    return (d1+d2)/2, sent_score
def dualclosnesscovertwoV2(v1,v2,L,version='sum',closetype='max',exclusion='yes',normmethod='reci'):
    d1,sentscore1 = dualclosenesscoverV2(v1,v2,L,version=version,closetype=closetype,exclusion=exclusion,normmethod=normmethod)
    d2,sentscore2 = dualclosenesscoverV2(v2,v1,L,version=version,closetype=closetype,exclusion=exclusion,normmethod=normmethod)
    sent_score = (sentscore1 + sentscore2)/2.0
   # print(d1,d2)
    return (d1+d2)/2, sent_score

def singledirectedcloseness(v1,v2,L,version='sum',exclusion='yes'):
    d1,sentscore1 = dualclosenesscover(v1,v2,L,version=version,exclusion = exclusion)
   # print(d1,d2)
    return d1, sentscore1
def singlebackdirectedcloseness(v1,v2,L,version='sum'):
    d1,sentscore1 = dualclosenesscover(v2,v1,L,version=version)
   # print(d1,d2)
    return d1, sentscore1