# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_x86 import CompileToX86

class CompileToARM(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to ARM ASM compiler.', file=sys.stderr)

    def get_name():
        return ('arm', 'ARM assembly, Raspberry PI target')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('invoke function')
        print('%sbl f%d' % (self.genindent(1), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add value to data pointer')
        print('%sadd r0, r0, #%d' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub value from data pointer')
        print('%ssub r0, r0, #%d' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to data')
        print('%sldrb r1,[r0]' % ind)
        print('%sadd r1, r1, #%d' % (ind, n))
        print('%sstrb r1,[r0]' % ind)

    def subFromData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from data')
        print('%sldrb r1,[r0]' % ind)
        print('%ssub r1, r1, #%d' % (ind, n))
        print('%sstrb r1,[r0]' % ind)

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')
        for i in range(0, n):
            print('%sbl prtchr' % self.genindent(1))

        print('')

    def startLoop(self, n):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))
            ind = self.genindent(1)
            print('%sldrb r1,[r0]' % ind)
            print('%stst r1,r1' % ind)
            print('%sbeq %s_e' % (ind, loopName))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sb %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('// %s' % s)

    def multilineCommentStart(self):
        print('//')

    def multilineCommentLine(self, s):
        print('// %s' % s)

    def multilineCommentEnd(self):
        print('//')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')
            print('f%d:' % blkLoop)
            i = self.genindent(1)
            print('%spush { lr }' % i)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('%spop { lr }' % i)
            print('%sbx lr' % i)
            print('.ltorg')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        print('.bss')

        ind = self.genindent(1)
        print('%s.lcomm buffer, 2' % ind)
        print('%s.lcomm data_mem, 32000' % ind)

    def emitMainFunction(self):
        ind = self.genindent(1)

        print('.global    _start')
        print('')
        self.addComments(self.copyrightNotice)
        print('.text')
        print('_start:')
        print('%sbl init' % ind)
        # initialize print-buffer
        print('%smov r1,#0' % ind)
        print('%sstrb r1,[r2]' % ind)

        self.translate(0, len(self.allCode))

        print('')
        print('%smov r0, $0' %ind)
        print('%smov r7, $1' % ind) # sys_exit
        print('%sswi $0' % ind)

        ind = self.genindent(1)
        print('prtchr:')
        print('%spush { r0, r1, r2 }' % ind)

        print('%sldrb r1,[r0]' % ind)
        print('%sstrb r1,[r2]' % ind)

        print('%smov r0, #1 ' % ind)    # fd: STDOUT
        print('%sldr r1,=buffer' % ind)    # msg
        print('%smov r2, #1 ' % ind)    # count
        print('%smov r7, #4 ' % ind)    # write is syscall #4
        print('%sswi $0 ' % ind)        # syscall

        print('%spop { r0, r1, r2 }' % ind)

        print('%sbx lr' % ind)

        print('init:')
        print('%sldr r0,=data_mem' % ind)
        print('%sldr r2,=buffer' % ind)
        print('%sbx lr' % ind)
