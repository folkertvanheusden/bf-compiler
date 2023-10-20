# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_x86 import CompileToX86

class CompileToPower(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to Power ASM compiler.', file=sys.stderr)

    def get_name():
        return ('power', 'IBM AIX')

    def genindent(self, level):
        return '\t' * level

    def emitDebug(self, ind, position):
        print('%s.loc 1 %d %d' % (ind, position[0], position[1]))

    def invokeFunction(self, funcNr):
        self.addComment('bl function')

        print('%sbl\tf%d' % (self.genindent(1), funcNr))
        print('%snop' % self.genindent(1))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to pointer')

        self.emitDebug(ind, position)

        print(f'{ind}addi\t16,16,{n}')

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        self.emitDebug(ind, position)

        print(f'{ind}addi\t16,16,{-n}')

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to data')

        self.emitDebug(ind, position)

        print(f'{ind}lbz\t17,0(16)')
        print(f'{ind}addi\t17,17,{n}')
        print(f'{ind}stb\t17,0(16)')

    def subFromData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from data')

        self.emitDebug(ind, position)

        print(f'{ind}lbz\t17,0(16)')
        print(f'{ind}addi\t17,17,{-n}')
        print(f'{ind}stb\t17,0(16)')

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            print(f'{self.genindent(1)}bl prtchr')
            print(f'\tnop')

    def startLoop(self, n, position):
        self.emitDebug('\t', position)

        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))

            ind = self.genindent(1)

            print(f'{ind}lbz\t17,0(16)')
            # print(f'{ind}cmp\t0,0,17,18')  # ibm as
            print(f'{ind}cmp\t0,17,18')  # gas
            print(f'{ind}beq\t{loopName}_e')

            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        self.emitDebug('\t', position)

        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump back label
            print('%sb %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('# %s' % s)

    def multilineCommentStart(self):
        pass

    def multilineCommentLine(self, s):
        print('# %s' % s)

    def multilineCommentEnd(self):
        pass

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')

            print(f'f{blkLoop}:')
            print(f'\tstwu 1,-16(1)')
            print(f'\tmflr 0')
            print(f'\tstw 0,20(1)')

            ind = self.genindent(1)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print(f'\tlwz 0,20(1)')
            print(f'\tmtlr 0')
            print(f'\taddi 1, 1, 16')
            print(f'\tblr')
            print('\tnop')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        pass

    def emitMainFunction(self):
        ind = self.genindent(1)

        print(f'{ind}.toc')

        print(f'{ind}.csect\t.data[RW]')
        print(f'\t.comm\tdata_mem,32000')
        print(f'\t.comm\tmsg,32')
        print(f'{ind}.csect\t.text[PR]')
        print(f'{ind}.globl\t__start')
        print('')
        self.addComments(self.copyrightNotice)
        print('__start:')
        print(f'{ind}la\t16,data_mem(2)')
        print(f'{ind}li\t17,0')
        print(f'{ind}li\t18,0')

        self.translate(0, len(self.allCode))

        print('')
        print(f'{ind}li\t0,1')
        print(f'{ind}li\t3,1')
#        print(f'{ind}sc')

        print('prtchr:')
        print(f'{ind}lbz 9,0(16)')
        print(f'{ind}mr 3,9')
        print(f'{ind}bl .putchar')
        print(f'{ind}nop')

        print(f'{ind}blr')
        print(f'{ind}nop')
