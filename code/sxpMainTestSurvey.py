import sxpMultiPaperData
import sxpReferMan
import sxpTestWordDistQuerySurvey
import sxpSurveyData
from sxpSurveyData import sxpNode
import sxpTestSurveyAllChapter
import sxpTestSurveyAsOne
def RunAll():
    cmdlist = ['makesurvey','rouge']
    if 'multipaper' in cmdlist:
        sxpMultiPaperData.main('Work')
        sxpMultiPaperData.main('PaperSentenceNum')
    if 'refpreprocess' in cmdlist:
        sxpReferMan.main('ProcessRefText')

    if 'rankpaper' in cmdlist:
        sxpTestWordDistQuerySurvey.main('RunWordDistV6KS_DualSentRank')
        sxpTestWordDistQuerySurvey.main('BuilAllTopk')
        sxpTestWordDistQuerySurvey.main('ShowDualGenSurv')
    if 'makesurvey' in cmdlist:
        sxpSurveyData.main('Work')

        sxpSurveyData.main('BuildSurveyChapterByRankResult')
        sxpSurveyData.main('TraverseMakeSurvey')
        sxpSurveyData.main('MakeSurveyChapterID')
    if 'rouge' in cmdlist:
        sxpTestSurveyAllChapter.main()
def RunTopk():
#    sxpTestWordDistQuerySurvey.main('BuilAllTopk')
    #this is to make survey system files for each chapter
    #by ranking both artical and sententences with papers.
    sxpSurveyData.main('BuildSurveyChapterByRankResult')
    sxpSurveyData.main('TraverseMakeSurvey')
#
    sxpTestSurveyAllChapter.main()
def RunSurveyOne():
    sxpSurveyData.TestLoadAllChapterModelDoc()
    testname = 'wordquery_allv6ks_dual_sentrank'
    survgenmethod = 'opt_num'
    tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
    sxpTestSurveyAsOne.main();
def RunSurveyOneAbst():
    testname = 'wordquery_allv6ks_dual_sentrank'
    survgenmethod = 'opt_num'

    testname = 'wordquery_allv6ks_dual_sentrank'
    survgenmethod = 'abstract'

    tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
    for s in tops:
        print(s)


    sxpTestSurveyAsOne.main();
def RunSurveyOneTFIDFAbst():
    testname = 'wordquery_allv6ks_dual_sentrank'
    survgenmethod = 'opt_num'

    testname = 'wordquery_allv6ks_dual_sentrank'
    survgenmethod = 'abstract'

    testname = 'tfidf_all'
    survgenmethod = 'abstract'
    tops = sxpSurveyData.LoadGenSurveySentList(testname, survgenmethod)
    for s in tops:
        print(s)

    sxpTestSurveyAsOne.main();

def RunLRTopkSurveyEveryChapter():
    #cmdlist = ['rankpaper','topkcompute','makesurvey','rouge']
    cmdlist = ['makesurvey', 'rouge']
    if 'rankpaper' in cmdlist:
        sxpTestWordDistQuerySurvey.main('RunWordDistV6KS_DualSentRank')
    if 'topkcompute' in cmdlist:
        sxpTestWordDistQuerySurvey.main('BuilAllTopk')
        sxpTestWordDistQuerySurvey.main('ShowDualGenSurv')
    if 'makesurvey' in cmdlist:
        sxpSurveyData.main()
    if 'rouge' in cmdlist:
        sxpTestSurveyAllChapter.main()
import sxpDUC2007main
import sxpTestDUC2007MultSum
def RunDUC2007():
    cmdlist=['makesurvey','rouge']
    if 'makesurvey' in cmdlist:
        sxpDUC2007main.main()
    if 'rouge' in cmdlist:
        sxpTestDUC2007MultSum.main()
def main():
    #RunSurveyOneTFIDFAbst()
    #RunLRTopkSurveyEveryChapter()
    RunDUC2007()
  #  TestCount()
if __name__ == '__main__':
    main()
