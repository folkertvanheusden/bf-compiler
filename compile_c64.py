# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

# Written with help of http://joriszwart.nl/

import sys

from compile_x86 import CompileToX86

class CompileToC64(CompileToX86):
	loopNr = 0
	hlNr = 0
	lnrs = []
	functionsFirst = False

	def header(self):
		print >>sys.stderr, 'Brainfuck to C64-ASM compiler.'

	def genindent(self, level):
		return ' ' * (level * 4)

	def invokeFunction(self, funcNr):
		print '%sJSR f%d' % (self.genindent(1), funcNr)

	def addToDataPtr(self, n, dot):
                ind = self.genindent(1)

		while n > 0:
			cur = min(n, 255)

			self.hlNr += 1

			if cur == 1:
				print '; inc pointer'
				print '%sinc $fb' % ind
				print '%sbne skip%d' % (ind, self.hlNr)
				print '%sinc $fc' % ind
				print 'skip%d' % self.hlNr

			else:
				print '; inc pointer'
				print '%sclc' % ind
				print '%slda $fb' % ind
				print '%sadc #%d' % (ind, cur)
				print '%ssta $fb' % ind
				print '%slda $fc' % ind
				print '%sadc #0' % ind
				print '%ssta $fc' % ind

			n -= cur

	def subFromDataPtr(self, n, dot):
                ind = self.genindent(1)

		while n > 0:
			cur = min(n, 255)

			self.hlNr += 1

			if cur == 1:
				print '; dec pointer'
				print '%sdec $fb' % ind
				print '%sbne skip%d' % (ind, self.hlNr)
				print '%sdec $fc' % ind
				print 'skip%d' % self.hlNr

			else:
				print '; dec pointer'
				print '%ssec' % ind
				print '%slda $fb' % ind
				print '%ssbc #%d' % (ind, cur)
				print '%ssta $fb' % ind
				print '%slda $fc' % ind
				print '%ssbc #0' % ind
				print '%ssta $fc' % ind

			n -= cur

	def addToData(self, n, dot):
		ind = self.genindent(1)

		print '; inc memory pointed to'
		print '%sldy #0' % ind
		print '%slda ($fb),y' % ind
		print '%sclc' % ind
		print '%sadc #%d' % (ind, n)
		print '%ssta ($fb),y' % ind

	def subFromData(self, n, dot):
		ind = self.genindent(1)

		print '; dec memory pointed to'
		print '%sldy #0' % ind
		print '%slda ($fb),y' % ind
		print '%ssec' % ind
		print '%ssbc #%d' % (ind, n)
		print '%ssta ($fb),y' % ind

	def emitCharacter(self, n, dot):
		ind = self.genindent(1)

		print '; print char'
		for i in xrange(0, n):
			print '%sJSR prtchr' % ind

		print ''

	def startLoop(self, n):
		for j in xrange(0, n):
			print '; start loop'
			loopName = 'wloop_%d' % self.loopNr
			self.loopNr += 1
			self.lnrs.append(loopName)

			self.hlNr += 1

			print '%s%s' % (self.genindent(0), loopName)
			ind = self.genindent(1)
			print '%sLDY #$0' % ind
			print '%sLDA ($fb),y' % ind
			print '%sBNE over_%d' % (ind, self.hlNr)
			print '%sJMP %s_e' % (ind, loopName)
			print 'over_%d' % self.hlNr

	def finishLoop(self, n, dot):
		for j in xrange(0, n):
			jb_label = self.lnrs.pop(-1) # jump bakc label
			print '; end of loop'
			print '%sJMP %s' % (self.genindent(1), jb_label)

			jb_label_e = jb_label + "_e" # break out of while label
			print '%s' % jb_label_e

	def addComment(self, s):
		print '; %s' % s

	def multilineCommentStart(self):
		print ';'

	def multilineCommentLine(self, s):
		print '; %s' % s

	def multilineCommentEnd(self):
		print ';'

	def emitFunctions(self):
		self.lindentlevel += 1

		for blkLoop in xrange(0, len(self.blocks)):
			print 'f%d' % blkLoop

			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

			print '%srts' % self.genindent(1)

		self.lindentlevel -= 1

	def emitProgramTail(self):
                ind = self.genindent(1)
		# 32KB actually
		print 'data_mem .byte 0'

	def emitMainFunction(self):
                ind = self.genindent(1)

		self.addComments(self.copyrightNotice)
		print "*=$0801"
		print '%s.BYTE    $0B, $08, $0A, $00, $9E, $32, $30, $36, $31, $00, $00, $00' % ind

		print '; cls'
		print '%sjsr $e544' % ind
		print ''

		print '; get pointer to work area'
		print '%slda #<data_mem' % ind
		print '%ssta $fb' % ind
		print '%slda #>data_mem' % ind
		print '%ssta $fc' % ind
		print

		print '; clear work area'
		print '%slda #0' % ind
		print '%sldx #(30000/256)-1' % ind
		print '%sldy #0' % ind
		print '%stya' % ind
		print 'clear sta ($fb),y'
		print '%siny' % ind
		print '%sbne clear' % ind
		print '%sdex' % ind
		print '%sbne clear' % ind
		print

		print '%sLDA #14' % ind
		print '%sjsr $ffd2' % ind
		print

		print '%slda #<data_mem' % ind
		print '%ssta $fb' % ind
		print '%slda #>data_mem' % ind
		print '%ssta $fc' % ind
		print

		self.translate(0, len(self.allCode))

		print '%srts' % ind
		print

		print 'prtchr'
		print '%sLDY #$0' % ind
		print '%sLDA ($fb),y' % ind
		print '%sjsr $ffd2' % ind
		print '%srts' % ind
