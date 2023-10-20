# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToRust(CompileBase):
    loopNr = 0
    lnrs = []

    def header(self):
        print('Brainfuck to Rust compiler.', file=sys.stderr)

    def get_name():
        return ('rust', None)

    def genindent(self, level):
        return ' ' * (level * 3)

    def invokeFunction(self, funcNr):
        print('%sf%d();' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr = data_ptr.wrapping_add(%d);' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr = data_ptr.wrapping_sub(%d);' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] = data_mem[data_ptr].wrapping_add(%d);' % (ind, n))

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] = data_mem[data_ptr].wrapping_sub(%d);' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sprint!("{}", char::from(data_mem[data_ptr]));' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile data_mem[data_ptr] > 0 {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        for j in range(0, n):
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))

    def addComment(self, s):
        print('// %s' % s)

    def multilineCommentStart(self):
        print('/*')

    def multilineCommentLine(self, s):
        print(' * %s' % s)

    def multilineCommentEnd(self):
        print('*/')

    def emitProgramBootstrap(self, file):
        for i in self.copyrightNotice:
            print('// %s' % i)
        print('')
        print(f'// This is a translation of "{file}".')

        print('static mut data_ptr: usize = 0;')
        print('static mut data_mem: [u8; 32768] = [0; 32768];')
        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('%sfn f%d() {' % (self.genindent(self.lindentlevel), blkLoop))

            self.lindentlevel += 1
            print('%sunsafe {' % self.genindent(self.lindentlevel))
            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1
            print('%s}' % self.genindent(self.lindentlevel))
            self.lindentlevel -= 1

            print('%s}' % self.genindent(self.lindentlevel))

    def emitMainFunction(self):
        print('fn main() {')

        self.lindentlevel += 1
        print('%sunsafe {' % self.genindent(self.lindentlevel))
        self.lindentlevel += 1
        print('%s data_ptr = 0;' % self.genindent(self.lindentlevel))

        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
        print('%s}' % self.genindent(self.lindentlevel))
        self.lindentlevel -= 1

        print('}')
