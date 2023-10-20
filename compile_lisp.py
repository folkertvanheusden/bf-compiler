#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToLisp(CompileBase):
    def header(self):
        print('Brainfuck to Lisp compiler.', file=sys.stderr)

    def get_name():
        return ('lisp', None)

    def genindent(self, level):
        return ''

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

    def subFromData(self, n, dot):
        ind = self.genindent(self.lindentlevel)

        if n == 1:
            print('%sdata_mem[data_ptr]--;' % ind)
        else:
            print('%sdata_mem[data_ptr] -= %d;' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sprintf("%%c", data_mem[data_ptr]);' % self.genindent(self.lindentlevel))

        print('%sfflush(NULL);' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile(data_mem[data_ptr] > 0) {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('; %s' % s)

    def multilineCommentStart(self):
        print('#|')

    def multilineCommentLine(self, s):
        print('   %s' % s)

    def multilineCommentEnd(self):
        print('|#')

    def emitProgramBootstrap(self, file):
        print(f'; This is a translation of "{file}".')
        print('(defvar *data_mem* (make-array \'(32768))')
        print('(defvar *data_ptr*)')
        print('')

        self.addComments(self.copyrightNotice)
        print('')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            print('(defun f%d()' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print(')')

        self.lindentlevel -= 1

    def emitMainFunction(self):
        self.lindentlevel += 1

        print('int main(int argc, char *argv[])')
        print('{')
        print('%sdata_mem = (uint8_t *)calloc(32768, 1);' % self.genindent(self.lindentlevel))
        print('')

        self.translate(0, len(self.allCode))

        print('')
        print('%sfree(data_mem);' % self.genindent(self.lindentlevel))
        print('')
        print('%sreturn 0;' % self.genindent(self.lindentlevel))
        print('}')

        self.lindentlevel -= 1
