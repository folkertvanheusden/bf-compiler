#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToPowerShell(CompileBase):
    def header(self):
        print('Brainfuck to PowerShell compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def get_name():
        return ('powershell', 'PowerShell')

    def invokeFunction(self, funcNr):
        print('%sf%d;' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_ptr += %d;' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_ptr -= %d;' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_mem[$data_ptr] += %d;' % (ind, n))

        print('%s$data_mem[$data_ptr] = $data_mem[$data_ptr] -band 255;' % ind)

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%s$data_mem[$data_ptr] -= %d;' % (ind, n))

        print('%s$data_mem[$data_ptr] = $data_mem[$data_ptr] -band 255;' % ind)

    def emitCharacter(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        for i in range(0, n):
            print('%sWrite-Host ([char]::ConvertFromUtf32($data_mem[$data_ptr])) -NoNewLine;' % ind)

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile($data_mem[$data_ptr] -gt 0) {' % self.genindent(self.lindentlevel))

            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
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
        print('')

        print('$data_mem = [int[]]::new(32768);')
        print('$data_ptr = 0;')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('function f%d {' % blkLoop)

            self.lindentlevel += 1
            ind = self.genindent(self.lindentlevel)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            self.lindentlevel -= 1

            print('')

    def emitMainFunction(self):
        self.lindentlevel += 1
        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
