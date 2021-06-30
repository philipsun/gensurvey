#-------------------------------------------------------------------------------
# Name:        sxpLogger
# Purpose:
#
# Author:      sunxp
#
# Created:     24-03-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logging
def logThisMessageStr(fpathname, str):
    logfile = fpathname
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    logger.info(str)
    logger.removeHandler(hdlr)
    hdlr.close()
def main():
    pass

if __name__ == '__main__':
    main()
