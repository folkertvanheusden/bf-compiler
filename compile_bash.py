#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_base import CompileBase

class CompileToBash(CompileBase):
    def header(self):
        print('Brainfuck to Bash compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sf%d' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr=$((data_ptr + %d))' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr=$((data_ptr - %d))' % (ind, n))

    def addToData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[$data_ptr]=$((data_mem[data_ptr] + %d))' % (ind, n))
        print('%sdata_mem[$data_ptr]=$((data_mem[data_ptr] & 255))' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[$data_ptr]=$((data_mem[data_ptr] - %d))' % (ind, n))
        print('%sdata_mem[$data_ptr]=$((data_mem[data_ptr] & 255))' % ind)

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print("%sperl -e \"print chr(${data_mem[$data_ptr]});\"" % self.genindent(self.lindentlevel))

    def startLoop(self, n):
        for j in range(0, n):
            print('%swhile [ ${data_mem[$data_ptr]} -gt 0 ] ; do' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%sdone' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('# %s' % s)

    def multilineCommentStart(self):
        print('#')

    def multilineCommentLine(self, s):
        print('# %s' % s)

    def multilineCommentEnd(self):
        print('#')

    def emitProgramBootstrap(self):
        print('#! /bin/bash')
        print('')
        print('data_ptr=1')
        print('')
        print('memory_size=32768')
        print('i=0')
        print('while [ $i -lt $memory_size ] ; do')
        self.lindentlevel += 1
        print('%sdata_mem[$i]=0' % self.genindent(self.lindentlevel))
        print('%si=$((i + 1))' % self.genindent(self.lindentlevel))
        self.lindentlevel -= 1
        print('done')

        self.addComments(self.copyrightNotice)
        print('')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('function f%d {' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('}')

        self.lindentlevel -= 1

    def emitMainFunction(self):
        print('')

        self.translate(0, len(self.allCode))

        print('exit 0')
