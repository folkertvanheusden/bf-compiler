# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_x86 import CompileToX86

class CompileToSPARC(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    line_nr = 0

    def header(self):
        print('Brainfuck to SPARC ASM compiler.', file=sys.stderr)

    def get_name():
        return ('sparc', 'SUN Solaris')

    def genindent(self, level):
        return '\t' * level

    def line(self):
        #print(f'sym{self.line_nr}:')
        self.line_nr += 1

    def invokeFunction(self, funcNr):
        self.addComment('call function')

        self.line()
        print('%scall\tf%d' % (self.genindent(1), funcNr))
        print('%snop' % self.genindent(1))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to pointer')

        self.line()
        print(f'{ind}add\t%g5,{n},%g5')

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        self.line()
        print(f'{ind}sub\t%g5,{n},%g5')

    def addToData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to data')

        self.line()
        print(f'{ind}ldub\t[%g5],%g4')
        self.line()
        print(f'{ind}add\t%g4,{n},%g4')
        self.line()
        print(f'{ind}stb\t%g4,[%g5]')

    def subFromData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from data')

        self.line()
        print(f'{ind}ldub\t[%g5],%g4')
        self.line()
        print(f'{ind}sub\t%g4,{n},%g4')
        self.line()
        print(f'{ind}stb\t%g4,[%g5]')

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            self.line()
            print(f'{self.genindent(1)}call prtchr')

    def startLoop(self, n):
        self.line()
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))

            ind = self.genindent(1)

            self.line()
            print(f'{ind}ldub\t[%g5],%g4')
            self.line()
            print(f'{ind}tst\t%g4')
            self.line()
            print(f'{ind}be\t{loopName}_e')
            print(f'{ind}nop')

            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump back label
            self.line()
            print('%sjmp %s' % (self.genindent(1), jb_label))
            print('%snop' % self.genindent(1))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('/* %s */' % s)

    def multilineCommentStart(self):
        pass

    def multilineCommentLine(self, s):
        print('/* %s */' % s)

    def multilineCommentEnd(self):
        pass

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')

            print(f'f{blkLoop}:')
            print(f'\tsave\t%sp, -16, %sp')

            ind = self.genindent(1)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            self.line()
            print(f'\tret')
            self.line()
            print(f'\trestore')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        pass

    def emitMainFunction(self):
        ind = self.genindent(1)

        print(f'{ind}.section\t".data"')
        print(f'{ind}.align\t16')

        print(f'data_mem:\t.skip\t32000')
        print(f'{ind}.section\t".text"')
        print(f'{ind}.global\t_start')
        print('')
        self.addComments(self.copyrightNotice)
        print(f'{ind}.align\t16')
        print('_start:')
        print(f'{ind}set\tdata_mem,%g5')

        self.translate(0, len(self.allCode))

        print('')
        print(f'mov\t1,%g1			! 1 is SYS_exit')
        print(f'clr\t%o0			! return status is 0')
        print(f'ta\t8')

        ind = self.genindent(1)

        print('prtchr:')
        print(f'{ind}save\t%sp, -16, %sp')
        print(f'{ind}mov\t4,%g1			! 4 is SYS_write')
        print(f'{ind}mov\t1,%o0\t! 1 is stdout')
        print(f'{ind}mov\t%g5,%o1\t! pointer to buffer')
        print(f'{ind}mov\t1,%o2\t! length')
        print(f'{ind}ta\t8')
        print(f'{ind}ret')
        print(f'{ind}restore')
