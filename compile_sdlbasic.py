#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToSDLBasic(CompileBase):
    def header(self):
        print('Brainfuck to SDL-basic compiler.', file=sys.stderr)

    def get_name():
        return ('sdl-basic', None)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d()' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr = data_ptr + %d' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr = data_ptr - %d' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] = data_mem[data_ptr] + %d' % (ind, n))

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] = data_mem[data_ptr] - %d' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sfPrintS(chr(data_mem[data_ptr]))' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile data_mem[data_ptr] > 0' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%swend' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('\' %s' % s)

    def multilineCommentStart(self):
        print('\'')

    def multilineCommentLine(self, s):
        print('\' %s' % s)

    def multilineCommentEnd(self):
        print('\'')

    def emitProgramBootstrap(self, file):
        print('dim data_mem[32768]')
        print('data_ptr = 0')
        print('')
        print(f'\' This is a translation of "{file}".')

        self.addComments(self.copyrightNotice)
        print('')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('Function f%d()' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('End Function')

        self.lindentlevel -= 1

    def emitMainFunction(self):
        self.translate(0, len(self.allCode))
