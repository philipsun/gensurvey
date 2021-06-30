# this file contains some classes that are to read text files
# coding=UTF-8
import codecs
import os, sys
import sxpTextEncode
import re
import pickle
import xlrd
import xlsxwriter
import joblib
from sxpPackage import *
import sxpTestStringEncode

dirstack = []
dirfile_list = []
total_len = 0
total_word = 0

import json


def copydict(scoredict, doc_dict, prefix_key=""):
    for eachkey in doc_dict.keys():
        nk = prefix_key + eachkey
        scoredict[nk] = doc_dict[eachkey]
    return scoredict


def shutdown(cmd='close'):
    if 'close' in cmd:
        print('going to close computer by sxpReadFileMan')
        os.system('shutdown -s -t 1')


def makerowcolnum(n, r):
    nr, nc = divmod(n, r)
    rc = []
    if nc > 0:
        nr = nr + 1
    k = 0
    for i in range(nr):
        for j in range(r):
            if k < n:
                rc.append([i, j])
                k = k + 1
            else:
                break
    return rc, nr, r


def LoadFile(fname):
    if not os.path.exists(fname):
        print(('file does not exists', fname))
        return ''
    f = open(fname, 'r')
    txtc = f.read()
    f.close();
    tstr = sxpTestStringEncode.strencode(txtc, 'utf-8')
    return tstr


def SaveObject(ob, fname, dir=""):
    if len(dir) > 0:
        fullname = os.path.join(dir, fname)
    else:
        fullname = fname
    joblib.dump(ob, fullname)


def LoadObject(fname, dir=""):
    if len(dir) > 0:
        fullname = os.path.join(dir, fname)
    else:
        fullname = fname
    if os.path.exists(fullname) == False:
        print(('not exists', fullname))
        return None
    return joblib.load(fullname)


def IsExsit(fname):
    return os.path.exists(fname)


def GetDirFileList(filedir, filepat=""):
    if not os.path.exists(filedir):
        print('no dir to be read', filedir)
        return []
    filelist = []
    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    for f in files:
        if os.path.isdir(os.path.join(filedir, f)):
            continue
        if len(filepat) == 0:
            filelist.append(f)
        else:
            if re.match(filepat, f):
                filelist.append(f)
    return filelist


def sxpGetDirFileSubList(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        print(filedir)
        return []
    filelist = []
    subdirlist = []
    try:
        files = os.listdir(filedir)
        # now we first read each file in the txtPath
        for f in files:
            df = os.path.join(filedir, f)
            if os.path.isdir(df):
                subdirlist.append(f)
            else:
                filelist.append(f)
    except Exception as e:
        msg = filedir + ':' + str(e)
        print(msg)
    return filelist, subdirlist


def TestJsonDump():
    json_dict = {}

    urlrec = []
    for i in range(10):

        id = 0;
        for j in range(10):
            urlitem = {'i': i, 'j': j}
            urlrec.append(urlitem)
    json_dict['test'] = urlrec
    urlrecfile = 'test.json'
    urlf = open(urlrecfile, 'w+')
    json.dump(urlrec, urlf)
    urlf.close()
    fname = 'json_dict.json'
    StoreJsonDict(json_dict, fname)


def StoreJsonDict(json_dict, fname):
    strjson = json.dumps(json_dict)
    f = codecs.open(fname, 'w+', 'utf-8')
    f.write(strjson)
    f.close
    return 1


def ExtractJsonFromStr(jstr):
    t = json.JSONDecoder().decode(jstr)
    return t


def ReadJSonFromJSonFile(fname):
    f = file(fname)
    f = codecs.open(fname, 'r', 'utf-8')
    txt = f.read()
    t = json.JSONDecoder().decode(txt)
    return t


def ExtractJasonStr(jstr):
    ##        pattern = r"var\sdata=(\{.*?\})";
    ##        #but this won't work for nested brackets so we use another simple one
    ##        ct = re.findall(pattern,str,0)# it will return '{hello}' in ct[0] for str='var data={hello};
    ph = r'var\sdata='
    pe = r'};'
    str1 = re.sub(ph, '', jstr)
    str2 = re.sub(pe, '}', str1)
    return str2


def DeepSave(fname, ob):
    joblib.dump(ob, fname, compress=9)


def CheckLoadDict(dirfile):
    d = {}
    if os.path.exists(dirfile) == True:
        return joblib.load(dirfile)
    return d


def CheckLoadList(dirfile):
    d = []
    if os.path.exists(dirfile) == True:
        return joblib.load(dirfile)
    return d


def CheckMkDir(dirname):
    if os.path.exists(dirname):
        return 1
    else:
        os.path.os.mkdir(dirname)
    return 1

def CheckMkEachLevelSub(dirname):
    #print(dirname)
    if os.path.exists(dirname):
        return 1
    else:
        s = re.split(r'[\\|\/]',dirname)
        #print(s)
        n = len(s)
        if n == 1:
            os.path.os.mkdir(dirname)
            print('make dir', dirname)
            return 1
        else:
            for i in range(1,n+1):
                subs ='\\'.join(s[0:i])
                #print('check',subs)
                if os.path.exists(subs):
                    continue
                else:
                    os.path.os.mkdir(subs)
                    print('make dir',subs)
    return 1
def GetFilePathName(fname):
    pt = r'\\'
    pat = re.compile(pt)
    fs = pat.split(fname)
    if len(fs) == 1:
        return fname
    else:
        return ('\\'.join(fs[0:-1]), fs[-1])


def WriteExcel(fname, tableindex, rwstrset):
    if not os.path.exists(fname):
        print(('file does not exists', fname))
        return []
    try:
        workbook = xlsxwriter.Workbook(fname)
        nsheet = len(rwstrset)
        for eachtable in rwstrset:
            worksheet = workbook.add_worksheet()
            row = 0
            for eachrw in eachtable:
                col = 0
                for eachcol in eachrw:
                    # ctype 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    ctype = 1
                    xf = 0
                    value = str(eachcol)
                    worksheet.write(row, col, value)
                    col = col + 1
                row = row + 1
            print(('row write ', row))
        workbook.close()
    except Exception as e:
        print(('error in writing excel', e))


def LoadExcel(fname, tableindex=0):
    if not os.path.exists(fname):
        print(('file does not exists', fname))
        return []
    data = xlrd.open_workbook(fname)
    table = data.sheets()[tableindex]
    nrows = table.nrows
    ncols = table.ncols
    print(('load', fname, nrows, ncols))
    return table


def CountFileLineWord(filedir, ftype):
    dirstack = []
    dirfile_list = []
    total_len = 0
    total_word = 0
    total_len, total_word = TraverseCountDir(filedir, ftype)
    print(('in ', filedir, ' you have: len, word are:'))
    print((total_len, total_word))


def GetDirFileListByPat(filedir, pat):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0, 0
    filelist = []
    subdirlist = []
    total_fnum = 0
    total_type = 0
    total_size = 0
    dirstack = []

    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    subfile_dic = {}
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(df)
            dirstack.append(df.lower())
        else:
            filelist.append(f)
    file_type_set = []
    pt = re.compile(pattern=pat)
    for eachf in filelist:
        ff = os.path.join(filedir, eachf).lower()
        g = pt.match(eachf)
        total_fnum = total_fnum + 1
        if g:
            total_type = total_type + 1
            file_type_set.append(ff)
    return file_type_set


def GetDirFileListType(filedir, ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0, 0
    filelist = []
    subdirlist = []
    total_fnum = 0
    total_type = 0
    total_size = 0
    dirstack = []

    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    subfile_dic = {}
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(df)
            dirstack.append(df.lower())
        else:
            filelist.append(f)
    file_type_set = []
    for eachf in filelist:
        ff = os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        total_fnum = total_fnum + 1
        if urttype == ftype:
            total_type = total_type + 1
            file_type_set.append(ff)
    return file_type_set


def CountFileNum(filedir, ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0, 0
    #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    total_fnum = 0
    total_type = 0
    total_size = 0
    dirstack = []

    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    subfile_dic = {}
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(df)
            dirstack.append(df.lower())
        else:
            filelist.append(f)
    for eachf in filelist:

        ff = os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        total_fnum = total_fnum + 1
        if urttype == ftype:
            total_type = total_type + 1
            total_size = total_size + os.path.getsize(ff)
    while len(subdirlist) > 0:
        next_subdir = subdirlist.pop()
        tl, tw, ts = CountFileNum(next_subdir, ftype)
        total_fnum = total_fnum + tl
        total_type = total_type + tw
        total_size = total_size + ts
    return total_fnum, total_type, total_size


def TraverseCountDir(filedir, ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0, 0
    #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    total_len = 0
    total_word = 0
    dirstack = []

    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    subfile_dic = {}
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(df)
            dirstack.append(df.lower())
        else:
            filelist.append(f)
    for eachf in filelist:

        ff = os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        if urttype == ftype:
            dirfile_list.append([ff, eachf])
            txtlines = ReadTxtLines(ff)
            lennum = len(txtlines)
            wordnum = 0
            for eachline in txtlines:
                wds = eachline.split(' ')
                wordnum = wordnum + len(wds)
            print((lennum, wordnum, ff))
            total_len = total_len + lennum
            total_word = total_word + wordnum
    while len(subdirlist) > 0:
        next_subdir = subdirlist.pop()
        tl, tw = TraverseCountDir(next_subdir, ftype)
        total_len = total_len + tl
        total_word = total_word + tw

    return total_len, total_word


def GetFileType(fname):
    ft = fname.split('.')
    return ft[-1]


def GetURLFileType(urls):
    patstr = '/{0,2}(\w+)(\.)(\w+)$'
    pattern = re.compile(patstr)
    match = pattern.search(urls)
    pat_name = 'urltype'
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(urls, posd[1])
        return tg[2]
        # pattern_pos.append([tgtxt,posd,tg[2],pat_name,1,0])
    return ''


def StoreSxptext(sxptxt, fname):
    f = open(fname, 'wb')
    pickle.dump(sxptxt, f)
    f.close()


def LoadSxptext(fname):
    f = open(fname, 'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


rootdir = r'D:\pythonwork\code\axureui'
rootdir = r'./'
logfilename = rootdir + r'\weblog\log.txt'
indexpage = rootdir + r'\templates\index.html'
startuipage = rootdir + r'\templates\start.htm'
webfileroot = rootdir + r'\webfile'
webfilerootpattern = webfileroot.replace('\\', '\\\\').lower()


def GetWebFilePathName(s):
    patstr = 'd:\\\\pythonwork\\\\code\\\\axureui\\\\webfile(.+)'
    patstr = webfilerootpattern + '(.+)'
    pattern_pos = []
    pattern = re.compile(patstr)
    match = pattern.search(s)
    pat_name = 'url'
    filesuffixpatstr = r''
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s, posd[1])
        pattern_pos.append([tgtxt, posd, tg, pat_name, 1, 0])
        return tg[0]
    print('')


def TraverseDir(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    webfile_dic = {}
    # now we first read each file in the txtPath
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(df)
            dirstack.append(df.lower())
        else:
            filelist.append(f)
    for eachf in filelist:
        if eachf == 'axQuery.std.js':
            breakpoint = 1
        ff = os.path.join(filedir, eachf).lower()

        urlpath = GetWebFilePathName(ff)
        if urlpath is None:
            print(('none in', ff))
        else:
            urttype = GetURLFileType(eachf)
            webfile_dic[urlpath] = [ff, urttype]
            dirfile_list.append([ff, eachf, urlpath])
    while len(dirstack) > 0:
        next_subdir = dirstack.pop()
        TraverseDir(next_subdir)
    return filelist, subdirlist


def GetDir(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    # now we first read each file in the txtPath
    for f in files:
        df = os.path.join(filedir, f)
        #      print df, ' : ', os.path.isdir(df)
        if os.path.isdir(df):
            subdirlist.append(f)
        else:
            filelist.append(f)

    return filelist, subdirlist


def WriteStrFile(filename, txtstr, encodetype='gbk'):
    ut = sxpTextEncode.GetUnicode(txtstr)
    #     ut = ut.encode('utf-8')
    f = codecs.open(filename, 'w+', encodetype)
    f.write(ut)
    f.close();


def Read(fname, fdir="", encode='utf-8'):
    if len(fdir) > 0:
        fullname = os.path.join(fdir, fname)
    else:
        fullname = fname;
    try:
        #  f=file(fname)
        f = open(fullname, 'r', encoding=encode)
        txt = f.read()
        f.close()
        return txt
    except IOError:
        print(('wrong in open', fname))
        return []
    return textcontent


def ReadTextUTF(fname, fdir="", encode='utf-8'):
    if len(fdir) > 0:
        fullname = os.path.join(fdir, fname)
    else:
        fullname = fname;
    try:
        #  f=file(fname)
        f = codecs.open(fullname, 'r', encode)
        txt = f.read()
        f.close()
        return txt
    except IOError:
        print(('wrong in open', fname))
        return []
    return textcontent


def ReadTextContent(fpathname):
    try:
        file = open(fpathname, 'r')
        textcontent = file.read()
        file.close()
        return textcontent
    except IOError:
        print('wrong in open')
        return []
    return textcontent


def ReadALL(fpathname):
    print(fpathname)
    try:
        file = open(fpathname, 'r')
        lineset = [];
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                print(line);
            lineset = lineset + lines;

        file.close()
        return lineset
    except IOError:
        print(('wrong in open', fpathname))
        file.close();
        return []
    return lines


def ReadTxtLines(fpathname):
    try:
        file = open(fpathname, 'r',encoding = 'utf-8')
        lineset = [];
        while 1:
            line = file.readline()
            if not line:
                break
            if len(line.strip()) == 0:
                continue;
            else:
                lineset.append(line);
        file.close()
        return lineset
    except IOError:
        print(('wrong in open', fpathname))
        return []
    return lines


def SaveTxtFile(fname, txt, fdir, encodetype='utf-8'):
    fullname = os.path.join(fdir, fname)
    try:
        fileHandle = codecs.open(fullname, 'w', 'utf-8')
        fileHandle.write(txt)
        fileHandle.close()
    except IOError as e:
        print(fullname)
        print(('wrong in open', e))


def BackupTxtFile(fname):
    txt = ReadTextUTF(fname)
    fnamename = fname + '.bk'
    i = 0
    while (1):
        if os.path.exists(fnamename):
            fnamename = fnamename + '.bk'
            i = i + 1
            if i >= 2:
                fnamename = fname + '.bk'
                SaveTxtFile(fnamename, txt)
                print(('overlap the oldest fil:', fnamename))
                break
        else:
            SaveTxtFile(fnamename, txt)
            print(('backup it to file:', fnamename))
            break


def GetNewName(fname):
    fnamename = fname + '(1)'
    i = 0
    while (1):
        if os.path.exists(fnamename):
            fnamename = fnamename + '.bk'
            i = i + 1
            if i >= 10:
                fnamename = fname + '.bk'
                print(('overlap the oldest fil:', fnamename))
                break
        else:
            print(('backup it to file:', fnamename))
            break
    return fnamename


def TestCount():
    dirstack = []
    dirfile_list = []
    total_len = 0
    total_word = 0
    filedir = r'D:\pythonwork\code\queryparse\bookknowledge'
    print(filedir)
    print('--------------------- count source code')
    ftype = 'py'
    CountFileLineWord(filedir, ftype)
    ftype = 'html'
    CountFileLineWord(filedir, ftype)
    print('---------------------count document num')
    ftype = 'pdf'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num, f_size = CountFileNum(filedir, ftype)
    print(('There are %.3f' % (f_size / 1024 / 1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype))
    ftype = 'pptx'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num, f_size = CountFileNum(filedir, ftype)
    print(('There are %.3f' % (f_size / 1024 / 1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype))
    ftype = 'docx'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num, f_size = CountFileNum(filedir, ftype)
    print(('There are %.3f' % (f_size / 1024 / 1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype))
    ftype = 'jpg'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num, f_size = CountFileNum(filedir, ftype)
    print(('There are %.3f' % (f_size / 1024 / 1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype))


import re


def TestDir():
    submit_peers_dir = r'E:\pythonworknew\code\sentencerank\test\duc2002\duc2002\evaluation_results\evaluation_results\abstracts\phase1\SEEpeers\submittedpeers\SEE.abstracts.in.sentences'
    flist = GetDirFileList(submit_peers_dir)
    peerid = '27'
    pat = r'(D\d\d\d).P.(\d\d\d).([A-Z]).(%s).([A-Za-z0-9\-]+).html' % (peerid)  # D061.P.100.J.27.AP880911-0016.html

    for each in flist:
        print(each)
        g = re.match(pat, each)
        fullname = submit_peers_dir + '\\' + each
        #  print(fullname)
        if g:
            multid = g.groups()[0]
            lenstr = g.groups()[1]
            gid = g.groups()[2]
            sid = g.groups()[3]
            fid = g.groups()[4]
            print(fid)
            if fid == 'AP880217-0100':
                print((fid, 'found'))

def TestMkDir():
    cd = r'E:\pythonworknew\code\textsum\testdir\testdir'
    CheckMkEachLevelSub(cd)
def main():
    #TestDir()
    TestMkDir()

#  TestCount()
if __name__ == '__main__':
    main()
