# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToX86(CompileBase):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to x86 ASM compiler.', file=sys.stderr)

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('call function')
        print('%scall f%d' % (self.genindent(1), funcNr))

    def addToDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to pointer')

        if n == 1:
            print('%sinc %%esi' % ind)
        else:
            print('%saddl $%d, %%esi' % (ind, n))

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        if n == 1:
                print('%sdec %%esi' % ind)
        else:
                print('%ssubl $%d, %%esi' % (ind, n))

    def addToData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('add to data')

        if n == 1:
            print('%sincb (%%esi)' % ind)
        else:
            print('%saddb $%d, (%%esi)' % (ind, n))

    def subFromData(self, n, dot):
        ind = self.genindent(1)

        self.addComment('sub from data')

        if n == 1:
            print('%sdecb (%%esi)' % ind)
        else:
            print('%ssubb $%d, (%%esi)' % (ind, n))

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            print('%scall prtchr' % self.genindent(1))

    def startLoop(self, n):
        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))
            ind = self.genindent(1)
            print('%scmpb $0, (%%esi)' % ind)
            print('%sjz %s_e' % (ind, loopName))
            self.lindentlevel += 1

    def finishLoop(self, n, dot):
        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sjmp %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('/ %s' % s)

    def multilineCommentStart(self):
        print('/')

    def multilineCommentLine(self, s):
        print('/ %s' % s)

    def multilineCommentEnd(self):
        print('/')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')
            print('f%d:' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print('%sret' % self.genindent(1))

        self.lindentlevel -= 1

    def emitProgramTail(self):
        print('.bss')

        ind = self.genindent(1)
        print('%s.lcomm data_mem, 32000' % ind)
        print('%s.lcomm buffer, 2' % ind)

    def emitMainFunction(self):
        ind = self.genindent(1)

        print('.global    _start')
        print('')
        self.addComments(self.copyrightNotice)
        print('.text')
        print('_start:')
        print('%smovl $data_mem, %%esi' % ind)
        # initialize print-buffer
        print('%smovw $0, buffer' % ind)

        self.translate(0, len(self.allCode))

        print('')
        print('%smovl $1, %%eax' % ind) # sys_exit system call
        print('%smovl $0, %%ebx' % ind)
        print('%sint  $0x80' % ind)

        ind = self.genindent(1)
        print('prtchr:')
        print('%smovb (%%esi), %%al' % ind)
        print('%smovb %%al, buffer' % ind)
        print('%smovl $4, %%eax' % ind) # system call number sys_write
        print('%smovl $1, %%ebx' % ind) # fd
        print('%smovl $buffer, %%ecx' % ind) # pointer to text
        print('%smovl $1, %%edx' % ind) # length of text
        print('%sint  $0x80' % ind) # call kernel
        print('%sret' % ind)
