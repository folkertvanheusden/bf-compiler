# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_x86 import CompileToX86

class CompileToARM64(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False
    ind = '\t'

    def header(self):
        print('Brainfuck to ARM64 ASM compiler.', file=sys.stderr)

    def get_name():
        return ('arm64', 'ARM64 assembly, Raspberry Pi target')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('invoke function')
        print(f'{self.ind}str lr, [sp,#-16]!')  # push
        print('%sbl f%d' % (self.ind, funcNr))
        print(f'{self.ind}ldr lr, [sp], #16')  # pop

    def emitDebug(self, ind, position):
        print('%s.loc 1 %d %d' % (ind, position[0], position[1]))

    def addToDataPtr(self, n, dot, position):
        self.addComment('add value to data pointer')
        self.emitDebug(self.ind, position)
        print('%sadd x0, x0, #%d' % (self.ind, n))

    def subFromDataPtr(self, n, dot, position):
        self.addComment('sub value from data pointer')
        self.emitDebug(self.ind, position)
        print('%ssub x0, x0, #%d' % (self.ind, n))

    def addToData(self, n, dot, position):
        self.addComment('add to data')
        self.emitDebug(self.ind, position)
        print('%sldrb w1,[x0]' % self.ind)
        print('%sadd w1, w1, #%d' % (self.ind, n))
        print('%sstrb w1,[x0]' % self.ind)

    def subFromData(self, n, dot, position):
        self.addComment('sub from data')
        print('%sldrb w1,[x0]' % self.ind)
        print('%ssub w1, w1, #%d' % (self.ind, n))
        print('%sstrb w1,[x0]' % self.ind)

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')
        for i in range(0, n):
            print(f'{self.ind}str lr, [sp,#-16]!')  # push
            print('%sbl prtchr' % self.ind)
            print(f'{self.ind}ldr lr, [sp], #16')  # pop

        print('')

    def startLoop(self, n, position):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            self.emitDebug(self.ind, position)
            print('%s:' % (loopName,))
            print('%sldrb w1,[x0]' % self.ind)
            print('%stst w1,w1' % self.ind)
            print('%sbeq %s_e' % (self.ind, loopName))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        for j in range(0, n):
            self.emitDebug(self.ind, position)
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sb %s' % (self.ind, jb_label))

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
            print(f'{self.ind}.type   f{blkLoop}, %function')
            print(f'{self.ind}.global   f{blkLoop}')
            print('f%d:' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('%sret' % self.ind)
            print('.ltorg')

        self.lindentlevel -= 1

    def emitProgramBootstrap(self, file):
        print(f'.file 1 "{file}"')

    def emitProgramTail(self):
        print('.bss')

        print('%s.lcomm buffer, 2' % self.ind)
        print('%s.lcomm data_mem, 32000' % self.ind)

    def emitMainFunction(self):
        print('.list')
        print('.text')
        print('.global    _start')
        print('')
        self.addComments(self.copyrightNotice)
        print('_start:')
        print('%sbl init' % self.ind)
        # initialize print-buffer
        print('%smov w1,#0' % self.ind)
        print('%sstrb w1,[x2]' % self.ind)

        self.translate(0, len(self.allCode))

        print('')
        print('%smov x0, #0' %self.ind)
        print('%sldr x8, =93' % self.ind) # sys_exit
        print('%ssvc #0' % self.ind)

        print('prtchr:')
        print(f'{self.ind}str lr, [sp,#-16]!')  # push
        print(f'{self.ind}str x0, [sp,#-16]!')  # push
        print(f'{self.ind}str x1, [sp,#-16]!')
        print(f'{self.ind}str x2, [sp,#-16]!')

        print('%sldrb w1,[x0]' % self.ind)
        print('%sstrb w1,[x2]' % self.ind)

        print('%smov x0, #1 ' % self.ind)    # fd: STDOUT
        print('%sldr x1,=buffer' % self.ind)    # msg
        print('%smov x2, #1 ' % self.ind)    # count
        print('%sldr w8, =64 ' % self.ind)    # write is syscall #4
        print('%ssvc #0 ' % self.ind)        # syscall

        print(f'{self.ind}ldr x2, [sp], #16')  # pop
        print(f'{self.ind}ldr x1, [sp], #16')
        print(f'{self.ind}ldr x0, [sp], #16')
        print(f'{self.ind}ldr lr, [sp], #16')

        print('prtchr_end:')
        print('%sret' % self.ind)

        print('init:')
        print('%sldr x0,=data_mem' % self.ind)
        print('%sldr x2,=buffer' % self.ind)
        print('%sret' % self.ind)
