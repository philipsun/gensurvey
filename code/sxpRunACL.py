# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
# Create Time: 2021/2/27 17:38
# Author: Xiaoping Sun
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sxpDUC2007main
import sxpTestACLSum
import sxpReadFileMan
import sxpACLSumData
from sxpACLSumData import sxpNode

def Prepare():
    sxpACLSumData.main()
def RunRouge():

    sxpTestACLSum.main()
def main():
    runtype = 'rank and rouge'
    if runtype == 'runandclose':
        cmd = ['MakeACL','RunRouge','close']
   # cmd = ['MakeACL', 'RunRouge']
    if runtype == 'rank and rouge':
        cmd = [ 'MakeACL','RunRouge']
    if runtype == 'rouge':
        cmd = [ 'RunRouge']
    usetry = False;
    if usetry:
        try:
            if 'MakeACL' in cmd:
                #MakeRankDUC2007()
                Prepare()
            if 'RunRouge' in cmd:
                RunRouge()
            if 'close' in cmd:
                sxpReadFileMan.shutdown()
        except Exception:
            print(Exception)
            pass
    if 'MakeACL' in cmd:

        Prepare()
    if 'RunRouge' in cmd:
        RunRouge()
    if 'close' in cmd:
        sxpReadFileMan.shutdown()
if __name__ == '__main__':
    main()


