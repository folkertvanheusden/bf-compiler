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

    def get_name():
        return ('mips', 'Linux')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('call function')

        print('%sjal f%d' % (self.genindent(1), funcNr))

    def push_reg(self, reg):
        ind = self.genindent(1)
        print(f'{ind}addi $sp,$sp,-4  # push register {reg} on stack')
        print(f'{ind}sw ${reg},($sp)')

    def pop_reg(self, reg):
        ind = self.genindent(1)
        print(f'{ind}lw ${reg},($sp)  # pop register {reg} from stack')
        print(f'{ind}addi $sp,$sp,4')

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to pointer')

        print(f'{ind}addiu $s0, $s0, {n}')

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        print(f'{ind}subu $s0, $s0, {n}')

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to data')

        print(f'{ind}lb $t0,($s0)')
        print(f'{ind}add $t0, $t0, {n}')
        print(f'{ind}sb $t0,($s0)')

    def subFromData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from data')

        print(f'{ind}lb $t0,($s0)')
        print(f'{ind}sub $t0, $t0, {n}')
        print(f'{ind}sb $t0,($s0)')

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            print(f'{self.genindent(1)}jal prtchr')

    def startLoop(self, n, position):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))

            ind = self.genindent(1)

            print(f'{ind}lb $t0,($s0)')
            print(f'{ind}beq $t0,0,{loopName}_e')
            print(f'{ind}nop')

            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
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

            print(f'.ent f{blkLoop}')
            print(f'f{blkLoop}:')

            ind = self.genindent(1)

            self.push_reg('ra')

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            self.pop_reg('ra')

            print(f'{self.genindent(1)}jr $ra')
            print(f'.end f{blkLoop}')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        print('.bss')

        ind = self.genindent(1)
        print('%s.lcomm data_mem, 32000' % ind)

        print('.data')
        print('buffer: .word 0')

    def emitMainFunction(self):
        ind = self.genindent(1)

        print('.globl    __start')
        print('')
        self.addComments(self.copyrightNotice)
        print('.text')
        print('.ent __start')
        print('__start:')
        print(f'{ind}la $s0, data_mem')

        self.translate(0, len(self.allCode))

        print('')
        print(f'{ind}li $a0, 0')    # exit code
        print(f'{ind}li $v0, 4001') # exit command
        print(f'{ind}syscall')
        print('.end __start')

        ind = self.genindent(1)

        print('.globl prtchr')
        print('.ent prtchr')
        print('prtchr:')
        self.push_reg('ra')
        self.push_reg('s0')
        print(f'{ind}lb $a0,($s0)')  # get character
        print(f'{ind}la $a1, buffer')
        print(f'{ind}sb $a0,($a1)')  # put in buffer

        print(f'{ind}li $a0, 1')  # stdout
        print(f'{ind}la $a1, buffer')  # get address of buffer
        print(f'{ind}li $a2, 1')  # length
        print(f'{ind}li $v0, 4004')  # system call for write
        print(f'{ind}syscall')
        self.pop_reg('s0')
        self.pop_reg('ra')

        print(f'{ind}jr $ra')
        print('.end prtchr')
