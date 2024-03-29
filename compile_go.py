# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToGo(CompileBase):
    loopNr = 0
    lnrs = []

    def header(self):
        print('Brainfuck to Go compiler.', file=sys.stderr)

    def get_name():
        return ('go', None)

    def genindent(self, level):
        return ' ' * (level * 3)

    def invokeFunction(self, funcNr):
        print('%sf%d()' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_ptr++' % ind)
        else:
            print('%sdata_ptr += %d' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_ptr--' % ind)
        else:
            print('%sdata_ptr -= %d' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_mem[data_ptr]++' % ind)
        else:
            print('%sdata_mem[data_ptr] += %d' % (ind, n))

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_mem[data_ptr]--' % ind)
        else:
            print('%sdata_mem[data_ptr] -= %d' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sfmt.Printf("%%c", data_mem[data_ptr])' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%sfor data_mem[data_ptr] > 0 {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('/* %s */' % s)

    def multilineCommentStart(self):
        print('/*')

    def multilineCommentLine(self, s):
        print(' * %s' % s)

    def multilineCommentEnd(self):
        print(' */')

    def emitProgramBootstrap(self, file):
        print('package main')
        print('')
        print(f'// This is a translation of "{file}".')

        for i in self.copyrightNotice:
            print('// %s' % i)
        print('')

        print('import (')
        print('    "fmt"')
        print(')')
        print('')
        print('var data_ptr uint64')
        print('var data_mem [32768]uint8')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('%sfunc f%d() {' % (self.genindent(self.lindentlevel), blkLoop))

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('%s}' % self.genindent(self.lindentlevel))

    def emitMainFunction(self):
        print('func main() {')

        self.lindentlevel += 1
        print('%sdata_ptr = 0' % self.genindent(self.lindentlevel))

        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1

        print('}')
