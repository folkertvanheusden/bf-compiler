#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToPython(CompileBase):
    def header(self):
        print('Brainfuck to Python compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d()' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr += %d' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr -= %d' % (ind, n))

    def addToData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] += %d' % (ind, n))

        print('%sdata_mem[data_ptr] &= 255' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] -= %d' % (ind, n))

        print('%sdata_mem[data_ptr] &= 255' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        for i in range(0, n):
            print('%ssys.stdout.write(chr(data_mem[data_ptr]))' % ind)

        print('%ssys.stdout.flush()' % ind)

    def startLoop(self, n):
        for j in range(0, n):
            print('%swhile data_mem[data_ptr] > 0:' % self.genindent(self.lindentlevel))

            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('# %s' % s)

    def multilineCommentStart(self):
        print('#')

    def multilineCommentLine(self, s):
        print('# %s' % s)

    def multilineCommentEnd(self):
        print('#')

    def emitProgramBootstrap(self):
        print('import sys')
        print('')

        for i in self.copyrightNotice:
            print('# %s' % i)
        print('')

        print('data_mem = [ 0 ] * 32768')
        print('data_ptr = 0')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('def f%d():' % blkLoop)

            self.lindentlevel += 1
            ind = self.genindent(self.lindentlevel)

            print('%sglobal data_mem' % ind)
            print('%sglobal data_ptr' % ind)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            self.lindentlevel -= 1

            print('')

    def emitMainFunction(self):
        print('if __name__ == "__main__":')

        self.lindentlevel += 1
        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
