#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_c import CompileToC

class CompileToJavascript(CompileToC):
    def header(self):
        print('Brainfuck to Javascript compiler.', file=sys.stderr)

    def get_name():
        return ('javascript', None)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d();' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_ptr++;' % ind)
        else:
            print('%sdata_ptr += %d;' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_ptr--;' % ind)
        else:
            print('%sdata_ptr -= %d;' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_mem[data_ptr]++;' % ind)
        else:
            print('%sdata_mem[data_ptr] += %d;' % (ind, n))

        print('%sdata_mem[data_ptr] &= 255;' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_mem[data_ptr]--;' % ind)
        else:
            print('%sdata_mem[data_ptr] -= %d;' % (ind, n))

        print('%sdata_mem[data_ptr] &= 255;' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        for i in range(0, n):
            print('%sprocess.stdout.write(String.fromCharCode(data_mem[data_ptr]));' % ind)

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile(data_mem[data_ptr] > 0) {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))

    def emitProgramBootstrap(self, file):
        print(f'// This is a translation of "{file}".')
        for i in self.copyrightNotice:
            print('// %s' % i)
        print('')

        print('memory_size = 32768;')
        print('var data_mem = [];')
        print('for(i=0; i < memory_size; i++) {')
        self.lindentlevel += 1
        print('%sdata_mem.push(0);' % self.genindent(self.lindentlevel))
        self.lindentlevel -= 1
        print('}')
        print('var data_ptr = 0;')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('function f%d() {' % blkLoop)

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('}')

    def emitMainFunction(self):
        self.lindentlevel += 1

        print('')

        self.translate(0, len(self.allCode))

        print('')

        self.lindentlevel -= 1
