# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import getpass
import sys
import time

from compile_base import CompileBase

class CompileToCOBOL(CompileBase):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to COBOL compiler.', file=sys.stderr)

    def get_name():
        return 'cobol'

    def genindent(self, level):
        labelspace = ' ' * 7

        indentstr = ' ' * (level * 2)

        return '%s%s' % (labelspace, indentstr)

    def invokeFunction(self, funcNr):
        print('%sPERFORM SECTION-%d' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot):
        print('%sADD %d TO DATA-PTR%s' % (self.genindent(self.lindentlevel), n, dot))

    def subFromDataPtr(self, n, dot):
        print('%sSUBTRACT %d FROM DATA-PTR%s' % (self.genindent(self.lindentlevel), n, dot))

    def addToData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sADD %d TO DATA-MEM(DATA-PTR)%s' % (ind, n, dot))
        print('%sIF DATA-MEM(DATA-PTR) > 255 THEN' % ind)
        print('%sSUBTRACT 256 FROM DATA-MEM(DATA-PTR)' % ind)
        print('%sEND-IF' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sSUBTRACT %d FROM DATA-MEM(DATA-PTR)%s' % (ind, n, dot))
        print('%sIF DATA-MEM(DATA-PTR) < 0 THEN' % ind)
        print('%sADD 256 TO DATA-MEM(DATA-PTR)' % ind)
        print('%sEND-IF' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sMOVE DATA-MEM(DATA-PTR) TO TEMP' % ind)
        print('%sADD 1 TO TEMP' % ind)

        for i in range(0, n):
            print('%sDISPLAY FUNCTION CHAR(TEMP) WITH NO ADVANCING%s' % (ind, dot))

    def startLoop(self, n):
        for j in range(0, n):
            print('%sPERFORM UNTIL DATA-MEM(DATA-PTR) = 0' % self.genindent(self.lindentlevel))

            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%sEND-PERFORM%s' % (self.genindent(self.lindentlevel), dot))
            print('')

    def addComment(self, s):
        print('%s* %s' % (' ' * 6, s))

    def multilineCommentStart(self):
        print('%s*' % (' ' * 6))

    def multilineCommentLine(self, s):
        print('%s* %s' % (' ' * 6, s))

    def multilineCommentEnd(self):
        print('%s*' % (' ' * 6))

    def emitProgramBootstrap(self):
        print('       IDENTIFICATION DIVISION.')
        print('       PROGRAM-ID. BRAINFUCK.')
        print('       AUTHOR. %s' % getpass.getuser())
        print('      * Brainfuck code compiled to COBOL using compiler written')
        print('      * by Folkert van Heusden - mail@vanheusden.com')
        print('      * www.vanheusden.com')
        print('      * Released in the public domain license.')
        tm = time.localtime()
        print('       DATE-WRITTEN. %02d/%02d/%02d.' % (tm.tm_year % 100, tm.tm_mon, tm.tm_mday))
        print('       ')
        print('       DATA DIVISION.')
        print('       WORKING-STORAGE SECTION.')
        print('       01 WS-TABLE.')
        print('      * Note: 30k memory elements is the minimum suggested size. You may')
        print('      * encounter programs for which 32768 elements is not enough. In')
        print('      * that case replace the 32768 for DATA-MEM and DATA-MEM-LEN to')
        print('      * something bigger.')
        print('         05 DATA-MEM                        PIC 9(3) OCCURS 32768 TIMES.')
        print('       01 DATA-MEM-LEN                      PIC 9(5) VALUE 32768.')
        print('       01 DATA-PTR                          PIC 9(5) VALUE 1.')
        print('       01 TEMP                              PIC 9(5).')
        print('       ')
        print('       PROCEDURE DIVISION.')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('%sSECTION-%d.' % (self.genindent(self.lindentlevel), blkLoop))

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

    def emitMainFunction(self):

        self.lindentlevel = 1
        ind = self.genindent(self.lindentlevel)

        print('%sMOVE 1 TO DATA-PTR' % ind)
        print('%sPERFORM UNTIL DATA-PTR > DATA-MEM-LEN' % ind)
        self.lindentlevel += 1
        ind = self.genindent(self.lindentlevel)
        print('%sMOVE 0 TO DATA-MEM(DATA-PTR)' % ind)
        print('%sADD 1 TO DATA-PTR' % ind)
        self.lindentlevel -= 1
        ind = self.genindent(self.lindentlevel)
        print('%sEND-PERFORM' % ind)
        print('%sMOVE 1 TO DATA-PTR' % ind)
        print()

        self.translate(0, len(self.allCode))

        print('%sSTOP RUN.' % ind)
