#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToRuby(CompileBase):
    def header(self):
        print('Brainfuck to Ruby compiler.', file=sys.stderr)

    def get_name():
        return ('ruby', None)

    def genindent(self, level):
        return ' ' * (level * 3)

    def invokeFunction(self, funcNr):
        print('%sf%d()' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_ptr += %d' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_ptr -= %d' % (ind, n))

    def addToData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_mem[$data_ptr] += %d' % (ind, n))

        print('%s$data_mem[$data_ptr] &= 255' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_mem[$data_ptr] -= %d' % (ind, n))

        print('%s$data_mem[$data_ptr] &= 255' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        for i in range(0, n):
            print('%sprint $data_mem[$data_ptr].chr' % ind)

    def startLoop(self, n):
        for j in range(0, n):
            print('%swhile $data_mem[$data_ptr] > 0' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%send' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('# %s' % s)

    def multilineCommentStart(self):
        print('#')

    def multilineCommentLine(self, s):
        print('# %s' % s)

    def multilineCommentEnd(self):
        print('#')

    def emitProgramBootstrap(self, file):
        for i in self.copyrightNotice:
            print('# %s' % i)
        print('')
        print(f'# This is a translation of "{file}".')

        print('$memory_size = 32768')
        print('$data_mem = Array(0...$memory_size)')
        print('$data_ptr = 0')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('def f%d()' % blkLoop)

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('end')
            print('')

    def emitMainFunction(self):
        print('def main()')
        self.lindentlevel += 1
        print('%sfor i in 0..$memory_size' % self.genindent(self.lindentlevel))
        self.lindentlevel += 1
        print('%s$data_mem[i] = 0' % self.genindent(self.lindentlevel))
        self.lindentlevel -= 1
        print('%send' % self.genindent(self.lindentlevel))
        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
        print('end')
        print('')

        print('main()')
