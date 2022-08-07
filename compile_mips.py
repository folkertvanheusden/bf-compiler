# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_x86 import CompileToX86

class CompileToMIPS(CompileToX86):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to MIPS ASM compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('call function')

        print('%sjal f%d' % (self.genindent(1), funcNr))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to pointer')

        print(f'{ind}addiu $gp, $gp, {n}')

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        print(f'{ind}subu $gp, $gp, {n}')

    def addToData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to data')

        print(f'{ind}lb $t0,($gp)')
        print(f'{ind}add $t0, $t0, {n}')
        print(f'{ind}sb $t0,($gp)')

    def subFromData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from data')

        print(f'{ind}lb $t0,($gp)')
        print(f'{ind}sub $t0, $t0, {n}')
        print(f'{ind}sb $t0,($gp)')

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            print(f'{self.genindent(1)}jal prtchr')

    def startLoop(self, n):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))

            ind = self.genindent(1)

            print(f'{ind}lb $t0,($gp)')
            print(f'{ind}beq $t0,0,{loopName}_e')

            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sj %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('# %s' % s)

    def multilineCommentStart(self):
        print('#')

    def multilineCommentLine(self, s):
        print('# %s' % s)

    def multilineCommentEnd(self):
        print('#')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')
            print('f%d:' % blkLoop)

            ind = self.genindent(1)

            print(f'{ind}addi $sp,$sp,-4')
            print(f'{ind}sw $ra,($sp)')

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print(f'{ind}lw $ra,($sp)')
            print(f'{ind}addi $sp,$sp,4')

            print(f'{self.genindent(1)}jr $ra')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        print('.bss')

        ind = self.genindent(1)
        print('%s.lcomm data_mem, 32000' % ind)
        print('%s.lcomm buffer, 2' % ind)

    def emitMainFunction(self):
        ind = self.genindent(1)

        print('.global    __start')
        print('')
        self.addComments(self.copyrightNotice)
        print('.text')
        print('__start:')
        print('%sla $gp, buffer' % ind)

        self.translate(0, len(self.allCode))

        print('')
        print(f'{ind}li $v0, 10') # exit
        print(f'{ind}syscall')

        ind = self.genindent(1)

        print('prtchr:')
        print(f'{ind}li $v0, 11')
        print(f'{ind}lb $a0,($gp)')
        print(f'syscall')

        print(f'{self.genindent(1)}jr $ra')
