#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToPerl(CompileBase):
    def header(self):
        print('Brainfuck to Perl compiler.', file=sys.stderr)

    def get_name():
        return ('perl', None)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d();' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s++$data_ptr;' % ind)
        else:
            print('%s$data_ptr += %d;' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s--$data_ptr;' % ind)
        else:
            print('%s$data_ptr -= %d;' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s$data_mem[$data_ptr]++;' % ind)
        else:
            print('%s$data_mem[$data_ptr] += %d;' % (ind, n))

        print('%s$data_mem[$data_ptr] &= 255;' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s$data_mem[$data_ptr]--;' % ind)
        else:
            print('%s$data_mem[$data_ptr] -= %d;' % (ind, n))

        print('%s$data_mem[$data_ptr] &= 255;' % ind)

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sprint chr($data_mem[$data_ptr]);' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile($data_mem[$data_ptr]) {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))

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

        print('use strict;')
        print('use warnings;')
        print('')
        print('my $data_ptr = 0;')
        print('my $ram_size = 131072;');
        print('my @data_mem = (0) x $ram_size;')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('sub f%d() {' % blkLoop)

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('}')

    def emitMainFunction(self):
        print('')

        self.translate(0, len(self.allCode))
