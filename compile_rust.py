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
        print('%s(data_ptr, data_mem) = f%d(data_ptr, data_mem);' % (self.genindent(self.lindentlevel), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr += %d;' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_ptr -= %d;' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] += %d;' % (ind, n))

    def subFromData(self, n, dot, position):
        ind = self.genindent(self.lindentlevel)

        print('%sdata_mem[data_ptr] -= %d;' % (ind, n))

    def emitCharacter(self, n, dot):
        for i in range(0, n):
            print('%sprint!("{}", String::from_utf8_lossy(&[data_mem[data_ptr].0]));' % self.genindent(self.lindentlevel))

    def startLoop(self, n, position):
        for j in range(0, n):
            print('%swhile data_mem[data_ptr] > std::num::Wrapping::<u8>(0) {' % self.genindent(self.lindentlevel))
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

        print('')

    def emitFunctions(self):
        for blkLoop in range(0, len(self.blocks)):
            print('%sfn f%d(mut data_ptr: usize, mut data_mem: Vec<std::num::Wrapping<u8>>) -> (usize, Vec<std::num::Wrapping<u8>>) {' % (self.genindent(self.lindentlevel), blkLoop))

            self.lindentlevel += 1
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            self.lindentlevel -= 1

            print('%s(data_ptr, data_mem)' % self.genindent(self.lindentlevel))
            print('%s}' % self.genindent(self.lindentlevel))

    def emitMainFunction(self):
        print('fn main_wrapper(mut data_ptr: usize, mut data_mem: Vec<std::num::Wrapping<u8>>) -> (usize, Vec<std::num::Wrapping<u8>>) {')
        self.lindentlevel += 1
        self.translate(0, len(self.allCode))
        self.lindentlevel -= 1
        print('%s(data_ptr, data_mem)' % self.genindent(self.lindentlevel))
        print('}')

        print('fn main() {')

        self.lindentlevel += 1
        print('%slet mut data_ptr: usize = 0;' % self.genindent(self.lindentlevel))
        print('%slet mut data_mem: Vec<std::num::Wrapping<u8>> = Vec::with_capacity(32768);' % self.genindent(self.lindentlevel))
        print('%sfor _i in 1..32768 {' % self.genindent(self.lindentlevel))
        print('%sdata_mem.push(std::num::Wrapping(0));' % self.genindent(self.lindentlevel + 1))
        print('%s}' % self.genindent(self.lindentlevel))
        print('%s(data_ptr, data_mem) = main_wrapper(data_ptr, data_mem);' % self.genindent(self.lindentlevel))

        self.lindentlevel -= 1

        print('}')
