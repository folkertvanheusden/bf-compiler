# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_msx import CompileToMSX

class CompileToPDP11(CompileToMSX):
    loopNr = 0
    hlNr = 0
    lnrs = []
    functionsFirst = False

    def header(self):
        print('Brainfuck to PDP-11 compiler.', file=sys.stderr)

    def get_name():
        return ('pdp-11', '"bare bones" assembly for the PDP-11 with at least 64kB RAM')

    def genindent(self, level):
        return ' ' * (level * 4)

    def invokeFunction(self, funcNr):
        print('%sCALL f%d' % (self.genindent(1), funcNr))

    def addToDataPtr(self, n, dot, position):
        ind = self.genindent(1)

        while n > 0:
            print('; add to pointer')

            cur = min(n, 65535)

            print(f'{ind}ADD #{cur:o},R0')

            n -= cur

    def subFromDataPtr(self, n, dot):
        ind = self.genindent(1)

        while n > 0:
            print('; sub from pointer')

            cur = min(n, 65535)

            print(f'{ind}SUB #{cur:o},R0')

            n -= cur

    def addToData(self, n, dot, position):
        ind = self.genindent(1)

        print('; add to data')

        if n == 1:
            print(f'{ind}INCB (R0)')

        else:
            print(f'{ind}MOVB (R0),R1')
            print(f'{ind}ADD #{n:o},R1')
            print(f'{ind}MOVB R1,(R0)')

    def subFromData(self, n, dot):
        ind = self.genindent(1)

        print('; sub from data')

        if n == 1:
            print(f'{ind}DECB (R0)')

        else:
            print(f'{ind}MOVB (R0),R1')
            print(f'{ind}SUB #{n:o},R1')
            print(f'{ind}MOVB R1,(R0)')

    def emitCharacter(self, n, dot):
        ind = self.genindent(1)

        for i in range(0, n):
            print('; print char')
            print('%sCALL prtchr' % ind)

        print('')

    def startLoop(self, n):
        for j in range(0, n):
            print('; start loop')
            loopName = 'wloop_%d' % self.loopNr
            self.loopNr += 1
            self.lnrs.append(loopName)

            print('%s%s:' % (self.genindent(0), loopName))
            ind = self.genindent(1)

            print(f'{ind}TSTB (R0)')
            # this is a work around for loops > 254 bytes in length
            print(f'{ind}BNE {loopName}_e_not')
            print(f'{ind}JMP {loopName}_e')
            print(f'{loopName}_e_not:')

    def finishLoop(self, n, dot):
        for j in range(0, n):
            print('; end loop')
            jb_label = self.lnrs.pop(-1) # jump bakc label
            print(f'{self.genindent(1)}JMP {jb_label}')

            jb_label_e = jb_label + "_e" # break out of while label
            print(f'{jb_label_e}:')

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
            print('f%d:' % blkLoop)

            self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

            print(f'{self.genindent(1)}RET')

        self.lindentlevel -= 1

    def emitProgramTail(self):
        ind = self.genindent(1)
        print(f'{ind}data_mem: .BLKB   32768.')
        print('ending: .BLKB 1')
        print(f'{ind}make_raw')

    def emitMainFunction(self):
        ind = self.genindent(1)

        self.addComments(self.copyrightNotice)
        print('start:')
        print(f'{ind}MOV  #01000,R6')
        print()
        print('; clear memory')
        print(f'{ind}MOV  #data_mem,R0')
        print(f'{ind}MOV  #32768.,R1')
        print(f'clear: CLRB (R0)+')
        print(f'{ind}DEC  R1')
        print(f'{ind}BNE  clear')
        print('')
        print(f'{ind}MOV  #data_mem,R0')

        self.translate(0, len(self.allCode))

        print(f'{ind}HALT')

        print('prtchr:')
        print('; Get character to print')
        print(f'{ind}MOVB  (R0),R1')
        print('; Print character')
        print(f'{ind}CALL  emit_chr')
        print('; Was it a LF? then also emit CR.')
        print(f'{ind}CMPB  #10.,R1')
        print(f'{ind}BEQ   emit_cr')
        print(f'{ind}RET')
        print(f'emit_cr: MOV  #13.,R1')
        print(f'{ind}CALL  emit_chr')
        print(f'{ind}RET')

        print(f'emit_chr:')
        print('; Wait for TTY to become ready')
        print(f'{ind}MOV  #0177564,R2')
        print(f'wait_write: TSTB (R2)')
        print(f'{ind}bpl  wait_write')
        print('; Print character')
        print(f'{ind}MOV  #0177566,R2')
        print(f'{ind}MOV  R1,(R2)')
        print(f'{ind}RET')
        print('')
