# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

# With help from http://www2.latech.edu/~acm/helloworld/asm370.html

import sys

from compile_x86 import CompileToX86

# R6 work register
# R7 pointer

class CompileToHLASM(CompileToX86):
	loopNr = 0
	lnrs = []
	functionsFirst = False
	doOptimize = False

	def header(self):
		print >>sys.stderr, 'Brainfuck to HLASM compiler.'

	def genindent(self, level):
		return ' ' * (level * 9)

	def emitLInstr(self, label, instr, pars):
		print '%-8s %-5s %s' % (label, instr, pars)

	def emitInstr(self, instr, pars):
		print '%s%-5s %s' % (self.genindent(1), instr, pars)

	def invokeFunction(self, funcNr):
		self.emitInstr('LA', 'R15,f%d' % funcNr)
		self.emitInstr('BALR', 'R14,R15') # branch and link register

	def addToDataPtr(self, n, dot):
                ind = self.genindent(1)

		# load address, LA = 12 bit max, LAY = 20 bit max
		print '* add to data ptr'
		self.emitInstr('AHI', 'R7,%d' % n)

	def subFromDataPtr(self, n, dot):
                ind = self.genindent(1)

		print '* sub from data ptr'
		self.emitInstr('L', "R6,=F'%d'" % n)
		self.emitInstr('SR', 'R7,R6') # FIXME SR werkt niet zoals verwacht

	def addToData(self, n, dot):
		ind = self.genindent(1)

		print '* add to data'
		self.emitInstr('LLGC', 'R6,0(R7)')
		self.emitInstr('AHI', 'R6,%d' % n)
		self.emitInstr('STC', 'R6,0(R7)')

	def subFromData(self, n, dot):
		ind = self.genindent(1)

		print '* sub from data'
		self.emitInstr('LLGC', 'R6,0(R7)')
		self.emitInstr('L', "R5,=F'%d'" % n)
		self.emitInstr('SR', 'R6,R5')
		self.emitInstr('STC', 'R6,0(R7)')

	def emitCharacter(self, n, dot):
		ind = self.genindent(1)

		print '* emit character'
		self.emitInstr('LLGC', 'R6,0(R7)')
		self.emitInstr('LA', 'R5,BUFFER')
		self.emitInstr('STC', 'R6,0(R5)')
		self.emitInstr('LA', 'R1,MSGAREA')

		for i in xrange(0, n):
			self.emitInstr('SVC', '35')

	def startLoop(self, n):
		for j in xrange(0, n):
			print '* start loop'
			loopName = 'wloop_%d' % self.loopNr
			self.loopNr += 1
			self.lnrs.append(loopName)

			ind = self.genindent(1)
			#self.emitInstr('LA', 'R15,%s_e' % loopName)
			self.emitLInstr(loopName, 'LLGC', 'R6,0(R7)')
			self.emitInstr('C', "R6,=F'0'")
			#self.emitInstr('BZR', 'R15')
			self.emitInstr('BE', '%s_e' % loopName)

	def finishLoop(self, n, dot):
		for j in xrange(0, n):
			print '* end loop'
			jb_label = self.lnrs.pop(-1) # jump bakc label
			self.emitInstr('J', '%s' % jb_label)
			self.emitInstr('LTORG', '')

			jb_label_e = jb_label + "_e" # break out of while label
			self.emitLInstr(jb_label_e, 'NOP', '')

	def addComment(self, s):
		print '* %s' % s

	def multilineCommentStart(self):
		print '*'

	def multilineCommentLine(self, s):
		print '* %s' % s

	def multilineCommentEnd(self):
		print '*'

	def emitFunctions(self):
		for blkLoop in xrange(0, len(self.blocks)):
			print 'f%d NOP' % blkLoop

			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

			print '%sPR' % self.genindent(1)

	def emitProgramTail(self):
		print '* program tail'
		print '         LTORG'
		print 'SAVE     DS    18A'
		print 'MSGAREA  EQU   *'
		print '         DC    AL2(5)'
		print "         DC    XL2'00'"
		print "BUFFER   DC    C'!'"
		print 'data_mem DS    32000C'
		print '         END BEGIN'

        def emitProgramBootstrap(self):
		print 'R0 EQU 0'
		print 'R1 EQU 1'
		print 'R2 EQU 2'
		print 'R3 EQU 3'
		print 'R4 EQU 4'
		print 'R5 EQU 5'
		print 'R6 EQU 6'
		print 'R7 EQU 7'
		print 'R8 EQU 8'
		print 'R9 EQU 9'
		print 'R10 EQU 10'
		print 'R11 EQU 11'
		print 'R12 EQU 12'
		print 'R13 EQU 13'
		print 'R14 EQU 14'
		print 'R15 EQU 15'
                print ''

                self.addComments(self.copyrightNotice)
                print ''


	def emitMainFunction(self):
                ind = self.genindent(1)

		print 'BF       START 0'
		print '%sPRINT NOGEN' % ind
		print 'BEGIN    SAVE  (14,12)'
		print '%sLR    R12,R15' % ind
		print '%sBALR  R2,0' % ind
		print '%sUSING *,R2' % ind
		print '%sST    R13,SAVE+4' % ind
		print '%sLA    R11,SAVE' % ind
		print '%sST    R11,8(13)' % ind
		print '%sLR    R13,R11' % ind

		print '%sLA    R7,data_mem' % ind

		self.translate(0, len(self.allCode))

		print '%sL     R13,SAVE+4' % ind
		print '%sRETURN (14,12),RC=0' % ind
