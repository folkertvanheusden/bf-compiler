#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_perl import CompileToPerl

class CompileToPerl6(CompileToPerl):
    def header(self):
        print('Brainfuck to Perl6 compiler.', file=sys.stderr)

    def get_name():
        return ('perl6', None)

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s++@data_mem[$data_ptr];' % ind)
        else:
            print('%s@data_mem[$data_ptr] += %d;' % (ind, n))

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%s--@data_mem[$data_ptr];' % ind)
        else:
            print('%s@data_mem[$data_ptr] -= %d;' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sprint chr(@data_mem[$data_ptr]);' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile @data_mem[$data_ptr] {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def emitProgramBootstrap(self, file):
        for i in self.copyrightNotice:
            print('# %s' % i)
        print('')
        print(f'# This is a translation of "{file}".')

        print('my int32 $data_ptr = 0;')
        print('my uint8 @data_mem;');
