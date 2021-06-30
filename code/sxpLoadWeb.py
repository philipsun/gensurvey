#-------------------------------------------------------------------------------
# Name:        sxpLoadWeb
# Purpose:
#
# Author:      sunxp
#
# Created:     27/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib.request, urllib.parse, urllib.error
import socket
import urllib.parse
import os
from bs4 import BeautifulSoup
import sxpTestStringEncode
fpath = r'D:\pythonwork\data\down'
fname = r'download.html'
timeout = 5

def FetchWebAndSubImg(urlstr, fpathname):
    print('to store at:', fpathname)
    try:
        socket.setdefaulttimeout(timeout)
        sock = urllib.request.urlopen(urlstr)
        #sock = urllib2.urlopen()
        urlcontent = sock.read()
        sock.close()
        f = open(fpathname,'wb+')
        f.write(urlcontent)
        f.close()
        FutureDownloadImgs(urlstr,urlcontent,fpathname)
        return urlcontent
    except Exception as e:
        print(('failed to access the web page:',urlstr))
        print(e)
        strmsg = '{0}:{1}'.format(urlstr,e)
        print(strmsg)
        return 0
def FutureDownloadImgs(urlstr,urlcontent,fpathname):
    fname = os.path.basename(fpathname)
    fpath = os.path.dirname(fpathname)
    fseg = fname.split('.')
    fprename = fseg[0]
    ffiles = fpath+ '\\'+fprename + '_files'
    if not os.path.exists(ffiles):
        os.path.os.mkdir(ffiles)
    soup = BeautifulSoup(urlcontent)
      #  urllinks = soup.a #this only return the first a tag, and you need to use next to find it
      #  self.urllinks = soup.find_all('a')
#    urlinks = soup.find_all("a", attr = {"href":'P14-2104.xhtml'})
    urlinks = soup.find_all('img')
    for img in urlinks:
        if img.has_attr('src'):
            imgsrc =img['src']
            imgurl = urllib.parse.urljoin(urlstr,imgsrc)
            imgfilename =  ffiles + '\\'+ os.path.basename(imgsrc)
##            socket.setdefaulttimeout(timeout)
##            sock = urllib.urlopen(imgurl)
##            #sock = urllib2.urlopen()
##            urlcontent = sock.read()
##            sock.close()
##            f = open(imgfilename,'w+')
##            f.write(urlcontent)
##            f.close()
            urllib.request.urlretrieve(imgurl, imgfilename, cbk)
def cbk(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)
def FetchWeb(urlstr,fpathname):
    print('to store at:', fpathname)
    timeout = 5
    try:
        socket.setdefaulttimeout(timeout)
        sock = urllib.request.urlopen(urlstr)
        #sock = urllib2.urlopen()
        urlcontent = sock.read()
        sock.close()
        f = open(fpathname,'w+')
        f.write(urlcontent)
        f.close()
        return urlcontent
    except Exception as e:
        print(('failed to access the web page:',urlstr))
        print(e)
        strmsg = '{0}:{1}'.format(urlstr,e)
        print(strmsg)
        return 0

def GetFileName(fpathname):
    fname = os.path.basename(fpathname)
    fpath = os.path.dirname(fpathname)
    fseg = fname.split('.')
    fsuffix = fseg[len(fseg)-1]
    ps = list(range(1,(len(fseg)-1)))
    if len(ps)== 0:
        fprefix = fseg[0]
    else:
        fprefix = fseg(ps)
    return [fpath,fname,fprefix, fsuffix]
def GetNewFileName(fname,i):
    fseg = fname.split('.')
    fsuffix = fseg[len(fseg)-1]
    if len(fseg)-1 == 0:
        fsuffix = ''
    ps = list(range(1,(len(fseg)-1)))
    if len(ps)== 0:
        fprefix = fseg[0]
    else:
        fprefix = fseg(ps)
    fnewname = fprefix + '({0}).'.format(i)+fsuffix
    return fnewname

def FindFilePathName(fpath,fname):
    if not os.path.exists(fpath):
        print('first create the directory')
        os.path.os.mkdir(fpath)
    fnewname = fpath + '\\' + fname
    if not os.path.exists(fnewname):
        return fname
    [fpath,fname,fprefix, fsuffix]  = GetFileName(fname)
    i = 0
    while 1:
      fnewname = fpath+ '\\' + GetNewFileName(fname,i)
      i = i+1
      if os.path.exists(fnewname) == False:
          break;
    return fnewname
def LoadFile(fname):
    if not os.path.exists(fname):
        print('file does not exists',fname)
        return ''
    f = open(fname,'r')
    txtc = f.read()
    f.close();
    tstr = sxpTestStringEncode.strencode(txtc,'utf-8')
    return tstr
def TestImg():
    urlstr = r'https://www.aclweb.org/anthology/P/P14/P14-1010.xhtml'
    fpathname = r'D:\pythonwork\data\down\test.xhtml'
    FetchWebAndSubImg(urlstr, fpathname)
def TestURL():
    urlstr = r'http://www.taobao.com'
    fpath = r'D:\pythonwork\data\down'
    fname = r'download.html'
    fpathname = fpath + '\\'+fname
    fnewname = FindFilePathName(fpath,fname)
    fpathname = fpath +  '\\'+fnewname
    print(fpathname)
    FetchWeb(urlstr,fpathname)
def main():
    TestImg()
if __name__ == '__main__':
    main()
