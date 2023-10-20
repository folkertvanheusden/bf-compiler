#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_c import CompileToC

class CompileToScala(CompileToC):
    def header(self):
        print('Brainfuck to Scala compiler.', file=sys.stderr)

    def get_name():
        return ('scala', None)

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr += %d.toShort;' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr -= %d.toShort;' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem(data_ptr) = (data_mem(data_ptr) + %d).toShort;' % (ind, n))

        print('%sdata_mem(data_ptr) = (data_mem(data_ptr) & 255).toShort;' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem(data_ptr) = (data_mem(data_ptr) - %d).toShort;' % (ind, n))

        print('%sdata_mem(data_ptr) = (data_mem(data_ptr) & 255).toShort;' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        for i in range(0, n):
            print('%sprint(data_mem(data_ptr).toChar)' % ind)

    def emitProgramBootstrap(self, file):
        for i in self.copyrightNotice:
            print('// %s' % i)
        print('')
        print(f'// This is a translation of "{file}".')

        print('object BrainfuckProgram {')
        self.lindentlevel += 1
        ind = self.genindent(self.lindentlevel)

        print('%svar data_ptr = 0' % ind)
        print('%sval data_mem = new Array[Short](32768)' % ind)
        print('')

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile(data_mem(data_ptr) > 0) {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('def f%d() : Unit = {' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('}')

        self.lindentlevel -= 1

    def emitMainFunction(self):
        print('%sdef run() : Unit = {' % self.genindent(self.lindentlevel))
        self.lindentlevel += 1
        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
        print('%s}' % self.genindent(self.lindentlevel))
        print('')

        print('%sdef main(args: Array[String]): Unit = {' % self.genindent(self.lindentlevel))
        self.lindentlevel += 1
        print('%srun();' % self.genindent(self.lindentlevel))
        self.lindentlevel -= 1

        print('%s}' % self.genindent(self.lindentlevel))

        self.lindentlevel -= 1
        print('%s}' % self.genindent(self.lindentlevel))
