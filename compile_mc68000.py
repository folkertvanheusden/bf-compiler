# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_x86 import CompileToX86

class CompileToMC68000(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False
    ind = '\t'

    def header(self):
        print('Brainfuck to MC68000 ASM compiler.', file=sys.stderr)

    def get_name():
        return ('mc68000', 'MC68000 assembly, Atari ST target')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('invoke function')
        print('%sjsr f%d' % (self.ind, funcNr))

    def addToDataPtr(self, n, dot, position):
        self.addComment('add value to data pointer')
        print('%smove.l #%d,A2' % (self.ind, n))
        print('%sadd.l a2,a0' % (self.ind, ))

    def subFromDataPtr(self, n, dot, position):
        self.addComment('sub value from data pointer')
        print('%ssub.l #%d,a0' % (self.ind, n))

    def addToData(self, n, dot, position):
        self.addComment('add to data')
        print(f'{self.ind}move.b (a0),d0')
        print(f'{self.ind}add.b #%d,d0' % n)
        print(f'{self.ind}move.b d0,(a0)')

    def subFromData(self, n, dot, position):
        self.addComment('sub from data')
        print(f'{self.ind}move.b (a0),d0')
        print(f'{self.ind}sub.b #%d,d0' % n)
        print(f'{self.ind}move.b d0,(a0)')

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')
        for i in range(0, n):
            print('%sjsr prtchr' % self.ind)

        print('')

    def startLoop(self, n, position):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s:' % (loopName,))
            print('%smove.b (a0),d0' % self.ind)
            print('%smove.b #0,d1' % self.ind)
            print('%scmp.b d0,d1' % self.ind)
            print('%sbeq %s_e' % (self.ind, loopName))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sjmp %s' % (self.ind, jb_label))

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
            self.addComment('function')

            print('f%d:' % blkLoop)
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            print('%srts' % self.ind)

        self.lindentlevel -= 1

    def emitProgramBootstrap(self, file):
        pass

    def emitProgramTail(self):
        print('.bss')
        print('data_mem: ds.b 32000' % self.ind)

    def emitMainFunction(self):
        self.addComments(self.copyrightNotice)
        print('.text')
        print('_start:')
        print('%sjsr init' % self.ind)

        self.translate(0, len(self.allCode))

        print('')
        print(f'{self.ind}clr.w -(sp)')  # quit (GEMDOS opcode 0)
        print(f'{self.ind}trap #1')

        print('prtchr:')
        print(f'{self.ind}move.l d0,-(sp)')
        print(f'{self.ind}move.l a0,-(sp)')
        print(f'{self.ind}and.b #255,d0')
        print(f'{self.ind}move.w d0,-(sp)')
        print(f'{self.ind}move.w #2,-(sp)')  # CONOUT
        print(f'{self.ind}trap #1')
        print(f'{self.ind}addq.l #4,sp')
        print(f'{self.ind}move.l (sp)+,a0')
        print(f'{self.ind}move.l (sp)+,d0')
        print('%srts' % self.ind)

        print('init:')
        print(f'{self.ind} move.l #data_mem,a0')
        print('%srts' % self.ind)
