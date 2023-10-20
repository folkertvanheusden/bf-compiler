# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_x86 import CompileToX86

class CompileToMSX(CompileToX86):
    loopNr = 0
    hlNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to MSX-ASM compiler.', file=sys.stderr)

    def get_name():
        return ('msx', 'Z80 assembly targeting MSX')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sCALL f%d' % (self.genindent(1), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        while n > 0:
            print('; add to pointer')

            if n <= 3:
                cur = n

                for i in range(0, n):
                    print('%sINC HL' % ind) # 6

            else:
                cur = min(n, 255)

                print('%sLD A,%d' % (ind, cur)) # 7
                print('%sLD C,A' % ind) # 4
                print('%sADD HL,BC' % ind) # 11

            n -= cur

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        while n > 0:
            print('; sub from pointer')

            if n <= 5:
                cur = n

                for i in range(0, n):
                    print('%sDEC HL' % ind) # 6

            else:
                cur = min(n, 255)

                print('%sAND A' % ind) # clear carry flag, 4
                print('%sLD A,%d' % (ind, cur)) # 7
                print('%sLD C,A' % ind) # 4
                print('%sSBC HL,BC' % ind) # 15

            n -= cur

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        print('; add to data')

        if n == 1:
            print('%sINC (HL)' % ind) # 11

        else:
            print('%sLD A,%d' % (ind, n)) # 7
            print('%sADD A,(HL)' % ind) # 7
            print('%sLD (HL),A' % ind) # 7

    def subFromData(self, n, dot, position):
        ind = self.genindent(1)

        print('; sub from data')

        if n == 1:
            print('%sDEC (hl)' % ind) # 11

        else:
            print('%sLD A,(HL)' % ind) # 7
            print('%sSUB %d' % (ind, n)) # 7
            print('%sLD (HL),A' % ind) # 7

    def emitCharacter(self, n, dot):
        ind = self.genindent(1)

        for i in range(0, n):
            print('; print char')
            print('%sCALL prtchr' % ind)

        print('')

    def startLoop(self, n, position):
        for j in range(0, n):
            print('; start loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))
            ind = self.genindent(1)
            print('%sLD A,(HL)' % ind)
            print('%sAND A' % ind)
            print('%sJP Z,%s_e' % (ind, loopName))

    def finishLoop(self, n, dot):
        for j in range(0, n):
            print('; end loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sJP %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('; %s' % s)

    def multilineCommentStart(self):
        print(';')

    def multilineCommentLine(self, s):
        print('; %s' % s)

    def multilineCommentEnd(self):
        print(';')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('f%d:' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('%sRET' % self.genindent(1))

        self.lindentlevel -= 1

    def emitProgramTail(self):
        ind = self.genindent(1)
        print('%sdata_mem: DB "dummy",0' % ind)
        print('ending: equ $-1')

    def emitMainFunction(self):
        ind = self.genindent(1)

        print('%sORG $8050-7' % ind)
        print('%sDB  $FE' % ind)
        print('%sDW  start,ending,start' % ind)
        self.addComments(self.copyrightNotice)
        print('start:')
        print('%sLD HL,data_mem' % ind)
        print('')
        print('%sLD D, 0' % ind)
        print('%sLD BC, freemem' % ind)
        print('clear:')
        print('%sLD (HL),D' % ind)
        print('%sINC HL' % ind)
        print('%sDEC BC' % ind)
        print('%sLD A,B' % ind)
        print('%sCP D' % ind)
        print('%sJP NZ,clear' % ind)
        print('%sLD A,C' % ind)
        print('%sCP D' % ind)
        print('%sJP NZ,clear' % ind)
        print('')
        print('%sLD HL,data_mem' % ind)
        print('%sLD B,0' % ind)

        self.translate(0, len(self.allCode))

        print('%sRET' % ind)

        print('prtchr:')
        print('%sLD A,(HL)' % ind)
        print('%sCALL $A2' % ind)

        self.addComment('Add CR when emitting an LF')
        print('%sLD D,$0A' % ind)
        print('%sCP D' % ind)
        label = 'nocarry%d' % self.hlNr
        self.hlNr += 1
        print('%sJP nc,%s' % (ind, label))
        print('%sLD A,$0d' % ind)
        print('%sCALL $A2' % ind)

        print('%s:' % (label))
        print('%sLD B,0' % ind)
        print('%sRET' % ind)
        print('')

        print('freemem: equ 2048')
