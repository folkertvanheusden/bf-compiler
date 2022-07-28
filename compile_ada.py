# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_base import CompileBase

class CompileToAda(CompileBase):
    loopNr = 0
    lnrs = []

    def header(self):
        print('Brainfuck to Ada compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d;' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot):
        print('%sdata_ptr := data_ptr + %d;' % (self.genindent(self.lindentlevel), n))

    def subFromDataPtr(self, n, dot):
        print('%sdata_ptr := data_ptr - %d;' % (self.genindent(self.lindentlevel), n))

    def addToData(self, n, dot):
        print('%sdata_mem(data_ptr) := data_mem(data_ptr) + %d;' % (self.genindent(self.lindentlevel), n))

    def subFromData(self, n, dot):
        print('%sdata_mem(data_ptr) := data_mem(data_ptr) - %d;' % (self.genindent(self.lindentlevel), n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print("%sput(Character'Val(data_mem(data_ptr)));" % self.genindent(self.lindentlevel))

        print('%sFlush;' % self.genindent(self.lindentlevel))

    def startLoop(self, n):
        for j in range(0, n):
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s :' % (self.genindent(self.lindentlevel - 1), loopName))
            print('%swhile data_mem(data_ptr) > 0 loop' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1

            print('%send loop %s;' % (self.genindent(self.lindentlevel), self.lnrs.pop(-1)))

    def addComment(self, s):
        print('-- %s' %s)

    def multilineCommentStart(self):
        print('--')

    def multilineCommentLine(self, s):
        print('-- %s' % s)

    def multilineCommentEnd(self):
        print('--')

    def emitProgramBootstrap(self):
        print('with Ada.Text_IO; use Ada.Text_IO;')
        print('')

        for i in self.copyrightNotice:
            print('-- %s' % i)
        print('')

        print('procedure main is')
        print('%sdata_mem : Array(0..32768) of Integer;' % self.genindent(self.lindentlevel))
        print('%sdata_ptr : Integer;' % self.genindent(self.lindentlevel))
        print('')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('%sprocedure f%d is' % (self.genindent(self.lindentlevel), blkLoop))
            print('%sbegin' % self.genindent(self.lindentlevel))

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('%send f%d;' % (self.genindent(self.lindentlevel), blkLoop))
            print('')

        self.lindentlevel -= 1

    def emitMainFunction(self):
        print('begin')

        self.lindentlevel = 1
        print('%sdata_ptr := 0;' % self.genindent(self.lindentlevel))

        self.translate(0, len(self.allCode))

        print('End main;')
