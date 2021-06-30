#-------------------------------------------------------------------------------
# Name:        sxpTimeManage
# Purpose:
#
# Author:      sunxp
#
# Created:     07/07/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import datetime
class sxpTimeString():
    def __init__(self):
        self.timereal = time.time()
        ctime = time.localtime(self.timereal)
        self.strYear = time.strftime('%Y')
        self.strMonth = time.strftime('%m')
        self.strDay = time.strftime('%d')
        self.strHour = time.strftime('%H')
        self.strMin = time.strftime('%M')
        self.strSec = time.strftime('%S')

# the default template is for strings like this "%Y-%m-%d %H:%M:%S" for 2015-01-01 10:24:20
# "%a %b %d %H:%M:%S %Y" timestr = "Sat Mar 28 22:24:24 2009"
    def ParseTimeStr(self, timestr,templatestr='%Y-%m-%d %H:%M:%S'):
        b = time.mktime(time.strptime(timestr,templatestr))
        bst = time.localtime(b) #bst is the time structure
        self.timereal = b #b is the real number time
        self.strYear = time.strftime('%Y',bst)
        self.strMonth = time.strftime('%m',bst)
        self.strDay = time.strftime('%d',bst)
        self.strHour = time.strftime('%H',bst)
        self.strMin = time.strftime('%M',bst)
        self.strSec = time.strftime('%S',bst)
# the default template is for strings like this "%Y-%m-%D" for 2015-01-01
    def ParseDayStr(self, timestr,templatestr='%Y-%m-%d'):
        b = time.mktime(time.strptime(timestr,templatestr))
        bst = time.localtime(b)
        self.timereal = b;
        self.strYear = time.strftime('%Y',bst)
        self.strMonth = time.strftime('%m',bst)
        self.strDay = time.strftime('%d',bst)
        self.strHour = time.strftime('%H',bst)
        self.strMin = time.strftime('%M',bst)
        self.strSec = time.strftime('%S',bst)
    @staticmethod
    def GetDayStrFromRealTime(b,templatestr='%Y-%m-%d'):
        timereal = time.time()
        ctime = time.localtime(b)

        return time.strftime(templatestr,ctime)
    @staticmethod
    def GetNow(templatestr='%Y-%m-%d %H:%M:%S'):
        timereal = time.time()
        bst = time.localtime(timereal)
        return time.strftime(templatestr,bst)

    @staticmethod
    def GetTodayStr():
        timereal = time.time()
        ctime = time.localtime(timereal)
        strYear = time.strftime('%Y')
        strMonth = time.strftime('%m')
        strDay = time.strftime('%d')
        strHour = time.strftime('%H')
        strMin = time.strftime('%M')
        strSec = time.strftime('%S')
        strDate = '{0}-{1}-{2}'.format(strYear,strMonth,strDay)
        return strDate
    @staticmethod
    def GetTimeStructFromTimeStr(timestr,templatestr='%Y-%m-%d'):
        b = time.mktime(time.strptime(timestr,templatestr))
        bst = time.localtime(b)
        return bst
    @staticmethod
    def CompareTwoTime(timestr_a,timestr_b,templatestr='%Y-%m-%d'):
        a =time.mktime(time.strptime(timestr_a,templatestr))
        b =time.mktime(time.strptime(timestr_b,templatestr))
        return a<b
    @staticmethod
    def IsInRange(timestr, timestr_a,timestr_b,templatestr='%Y-%m-%d'):
        a =time.mktime(time.strptime(timestr_a,templatestr))
        b =time.mktime(time.strptime(timestr_b,templatestr))
        c =time.mktime(time.strptime(timestr,templatestr))
        if a<=c and c<= b:
            return True;
        else:
            return False;
    @staticmethod
    def GetPrevDay(timestr,templatestr='%Y-%m-%d'):
        a =time.mktime(time.strptime(timestr,templatestr))
        bst = time.localtime(a)
        ct = datetime.datetime(bst[0],bst[1],bst[2])
        dt = timedelta(days=1)
        pt = ct - dt
        return pt.strftime('%Y-%m-%d')
    @staticmethod
    def GetNextDay(timestr,templatestr='%Y-%m-%d'):
        a =time.mktime(time.strptime(timestr,templatestr))
        bst = time.localtime(a)
        ct = datetime.datetime(bst[0],bst[1],bst[2])
        dt = timedelta(days=1)
        pt = ct + dt
        return pt.strftime('%Y-%m-%d')
def GetDateTimeFromTimeStr(timestr, templatestr='%Y-%m-%d'):
    t = time.mktime(time.strptime(timestr,templatestr))
    d_from_t = datetime.datetime.fromtimestamp(t)
    return d_from_t
def GetTimeRealNumFromTimeStr(timestr,templatestr='%Y-%m-%d'):
    b = time.mktime(time.strptime(timestr,templatestr))
    return b
def GetNow(templatestr='%Y-%m-%d %H:%M:%S'):
    timereal = time.time()
    bst = time.localtime(timereal)
    return time.strftime(templatestr,bst)
def GetNowForFile(templatestr='%Y_%m_%d_%H_%M_%S'):
    timereal = time.time()
    bst = time.localtime(timereal)
    return time.strftime(templatestr,bst)
def GetRange(timestr_a, timestr_b,templatestr='%Y-%m-%d %H:%M:%S'):
    a =time.mktime(time.strptime(timestr_a,templatestr))
    b =time.mktime(time.strptime(timestr_b,templatestr))
    da = datetime.datetime.fromtimestamp(a)
    db = datetime.datetime.fromtimestamp(b)

    if a < b:
        t = db-da
    else:
        t = da-db
    return str(t.total_seconds())
def AddRange(rangestr1,rangestr2):
    if len(rangestr1)==0:
        rgsec1 = 0
    else:
        rgsec1 = float(rangestr1)
    if len(rangestr2)==0:
        rgsec2 = 0
    else:
        rgsec2 = float(rangestr2)
    t = rgsec1 + rgsec2
    return str(t)
def Test():
    print(sxpTimeString.GetNow())
def main():
    Test()
    dt1 = GetNow()
    dt2 = '2015-09-10 13:20:23'
    rg1 = GetRange(dt2,dt1)
    rg2 = '1000.0'
    print(AddRange(rg1,rg2))
if __name__ == '__main__':
    main()
