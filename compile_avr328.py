# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_base import CompileBase

class CompileToAVR328(CompileBase):
    loopNr = 0
    lnrs = []
    functionsFirst = False
    reg_nul = 'r17'
    reg_tmp1 = 'r0'
    reg_tmp2 = 'r16'

    def header(self):
        print('Brainfuck to AVR328 ASM compiler.', file=sys.stderr)

    def get_name():
        return ('avr328', 'AVR328 assembly')

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

        print(f'{ind}ldi {self.reg_tmp2},%d' % (n,))
        print(f'{ind}add xL,{self.reg_tmp2}')
        print(f'{ind}adc xH,{self.reg_nul}')

    def subFromDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from pointer')

        self.emitDebug(ind, position)

        print(f'{ind}ldi {self.reg_tmp2},%d' % (n,))
        print(f'{ind}sub xL,{self.reg_tmp2}')
        print(f'{ind}sbc xH,{self.reg_nul}')

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('add to data')

        self.emitDebug(ind, position)

        print(f'{ind}ld {self.reg_tmp1},x')
        if n == 1:
            print(f'{ind}inc {self.reg_tmp1}')
        else:
            print(f'{ind}ldi {self.reg_tmp2},{n}')
            print(f'{ind}add {self.reg_tmp1},{self.reg_tmp2}')
        print(f'{ind}st x,{self.reg_tmp1}')

    def subFromData(self, n, dot, position):
        ind = self.genindent(1)

        self.addComment('sub from data')

        self.emitDebug(ind, position)

        print(f'{ind}ld {self.reg_tmp1},x')
        if n == 1:
            print(f'{ind}dec {self.reg_tmp1}')
        else:
            print(f'{ind}ldi {self.reg_tmp2},{n}')
            print(f'{ind}sub {self.reg_tmp1},{self.reg_tmp2}')
        print(f'{ind}st x,{self.reg_tmp1}')

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
            print(f'{ind}ld {self.reg_tmp1},x')
            print(f'{ind}cp {self.reg_tmp1},{self.reg_nul}')
            print('%sbrne %s_e_skip' % (ind, loopName))
            print('%sjmp %s_e' % (ind, loopName))
            print('%s_e_skip:' % (loopName,))
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
        print('')
        print('.dseg')
        print('data_mem: .byte 1024')

    def emitProgramBootstrap(self, file):
        self.addComments(self.copyrightNotice)

        ind = self.genindent(1)
        print('.nolist')
        print('.INCLUDE "m328Pdef.inc"')
        print('.list')
        print(f'{ind}.cseg')
        print(f'{ind}.org 0x0')
        print('rjmp    Init')
        print('Init:')
        print('; init uart')
        print(f'{ind}.equ F_CPU           = 16000000')
        print(f'{ind}.equ BAUD_RATE       = 9600')
        print(f'{ind}.equ BAUD_PRESCALER  = (F_CPU/(BAUD_RATE * 16)) - 1')
        print(f'{ind}ldi R16, LOW (BAUD_PRESCALER)')
        print(f'{ind}ldi R17, HIGH (BAUD_PRESCALER)')
        print(f'{ind}sts UBRR0L, R16')
        print(f'{ind}sts UBRR0H, R17')
        print(f'{ind}ldi R16, (1<<TXEN0) ; enable transmitter')
        print(f'{ind}sts UCSR0B, R16')
        print(';')
        print(f'{ind}clr {self.reg_nul}')
        print('; init memory')
        print(f'{ind}ldi xL, low(data_mem) ; load pointer to data into Y pointer')
        print(f'{ind}ldi xH, high(data_mem)')
        print(f'{ind}ldi r24,LOW(1024)')
        print(f'{ind}ldi r25,HIGH(1024)')
        print(f'{ind}ldi {self.reg_tmp2},1')
        print('cloop:')
        print(f'{ind}st x,{self.reg_nul}')
        print(f'{ind}add xL,{self.reg_tmp2}')
        print(f'{ind}adc xH,{self.reg_nul}')
        print(f'{ind}sbiw r24,1')
        print(f'{ind}cp r24,{self.reg_nul}')
        print(f'{ind}breq fin1')
        print(f'{ind}rjmp cloop')
        print('fin1:')
        print(f'{ind}cp r25,{self.reg_nul}')
        print(f'{ind}breq fin2')
        print(f'{ind}rjmp cloop')
        print('fin2:')
        print('; init memory pointers')
        print(f'{ind}ldi xL, low(data_mem) ; load pointer to data into Y pointer')
        print(f'{ind}ldi xH, high(data_mem)')
        print('; init stack')
        print(f'{ind}ldi {self.reg_tmp2},LOW(RAMEND)')
        print(f'{ind}out SPL,{self.reg_tmp2}')
        print(f'{ind}ldi {self.reg_tmp2},HIGH(RAMEND)')
        print(f'{ind}out SPH,{self.reg_tmp2}')

    def emitMainFunction(self):
        ind = self.genindent(1)

        self.translate(0, len(self.allCode))

        # end
        print(f'End:')
        print(f'{ind}rjmp End')

        # print a character
        print('prtchr:')
        print(f'{ind}push {self.reg_tmp2}')
        print('UART_WRITE_CHAR_LOOP:')
        print('; wait for the write buffer to become empty (bit UDRE0 of UCSR0A register should be set)')
        print(f'{ind}lds  {self.reg_tmp2}, UCSR0A')
        print(f'{ind}sbrs {self.reg_tmp2}, UDRE0')
        print(f'{ind}rjmp UART_WRITE_CHAR_LOOP')
        print(f'{ind}ld   {self.reg_tmp2},x')
        print(f'{ind}sts  UDR0, {self.reg_tmp2}')
        print(f'{ind}pop  {self.reg_tmp2}')
        print(f'{ind}RET')
