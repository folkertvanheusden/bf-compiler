# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileTo8086(CompileBase):
    loopNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to 8086 ASM compiler.', file=sys.stderr)

    def get_name():
        return ('8086', '8086 assembly, NASM syntax')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        self.addComment('call function')
        print('%scall f%d' % (self.genindent(1), funcNr))

    def emitDebug(self, ind, position):
        pass

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to pointer')
        self.emitDebug(ind, position)

        if n == 1:
            print('%sinc bx' % ind)
        else:
            print('%sadd bx,%d' % (ind, n))

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        self.emitDebug(ind, position)

        if n == 1:
                print('%sdec bx' % ind)
        else:
                print('%ssub bx,%d' % (ind, n))

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to data')

        self.emitDebug(ind, position)

        if n == 1:
            print('%sinc byte ds:[bx]' % ind)
        else:
            print('%smov al, byte ds:[bx]' % (ind,))
            print('%sadd al,%d' % (ind, n))
            print('%smov byte ds:[bx],al' % (ind,))

    def subFromData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from data')

        self.emitDebug(ind, position)

        if n == 1:
            print('%sdec byte ds:[bx]' % ind)
        else:
            print('%smov al, byte ds:[bx]' % (ind,))
            print('%ssub al,%d' % (ind, n))
            print('%smov byte ds:[bx],al' % (ind,))

    def emitCharacter(self, n, dot):
        self.addComment('emit character(s)')

        for i in range(0, n):
            print('%scall prtchr' % self.genindent(1))

    def startLoop(self, n, position):
        self.emitDebug('\t', position)

        for j in range(0, n):
            self.addComment('start of while loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))
            ind = self.genindent(1)
            print('%scmp byte ds:[bx], 0' % ind)
            print('%sjz %s_e' % (ind, loopName))
            self.lindentlevel += 1

    def finishLoop(self, n, dot, position):
        self.emitDebug('\t', position)

        for j in range(0, n):
            self.addComment('end of while loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print('%sjmp %s' % (self.genindent(1), jb_label))

            jb_label_e = jb_label + "_e" # break out of while label
            print('%s:' % jb_label_e)

    def addComment(self, s):
        print('; %s' % s)

    def multilineCommentStart(self):
        print(';')

    def multilineCommentLine(self, s):
        print('; %s' % s)

    def multilineCommentEnd(self):
        print(';')

    def emitFunctions(self):
        self.lindentlevel += 1

        for blkLoop in range(0, len(self.blocks)):
            self.addComment('function')

            print('f%d:' % blkLoop)
            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
            print('%sret' % self.genindent(1))

        self.lindentlevel -= 1

    def emitProgramTail(self):
        print('times ( ( ($-$$ + 0xFFFF) & ~0xFFFF ) - ($-$$) ) db 0x90')
        print('')
        print('SEGMENT _DATA')
        print('data_mem resb 32000')

        print('section _STACK class=stack')
        print('resb 1000h')
        print('stack_end:')

    def emitProgramBootstrap(self, file):
        pass

    def emitMainFunction(self):
        ind = self.genindent(1)

        self.addComments(self.copyrightNotice)
        print('    bits 16')
        print('    cpu 8086')
        print('SEGMENT _TEXT')
        print('GLOBAL start')
        print('start:')
        print('%scli' % ind)
        print('%smov ax,seg stack_end' % ind)
        print('%smov ss,ax' % ind)
        print('%smov sp,stack_end' % ind)

        print('%smov ax,seg data_mem' % ind)
        print('%smov es,ax' % ind)
        print('%smov bx,data_mem' % ind)
        print('%smov di,bx' % ind)
        print('%sxor al, al' % ind)
        print('%smov cx, 32000' % ind)
        print('%srep stosb' % ind)

        print('%smov ax,seg data_mem' % ind)
        print('%smov ds,ax' % ind)
        print('%smov bx,data_mem' % ind)

        self.translate(0, len(self.allCode))

        print('')
        print(f'{ind}mov ah,0x4C')
        print(f'{ind}int 0x21')

        ind = self.genindent(1)
        print('prtchr:')
        print(f'{ind}push bx')
        print(f'{ind}push ds')
        print(f'{ind}push dx')
        print(f'{ind}mov al, byte ds:[bx]')
        print(f'{ind}mov dl, al')
        print(f'{ind}mov  ah, 02h')
        print(f'{ind}int  21h')
        print(f'{ind}pop dx')
        print(f'{ind}pop ds')
        print(f'{ind}pop bx')
        print(f'{ind}ret')
