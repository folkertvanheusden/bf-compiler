# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_ada import CompileToAda

class CompileToPascal(CompileToAda):
	loopNr = 0
	lnrs = []

	def header(self):
		print('Brainfuck to Pascal compiler.', file=sys.stderr)

	def addToData(self, n, dot):
		print('%sdata_mem[data_ptr] := data_mem[data_ptr] + %d;' % (self.genindent(self.lindentlevel), n))

	def subFromData(self, n, dot):
		print('%sdata_mem[data_ptr] := data_mem[data_ptr] - %d;' % (self.genindent(self.lindentlevel), n))

	def emitCharacter(self, n, dot):
		for i in range(0, n):
			print('%sWrite(chr(data_mem[data_ptr]));' % self.genindent(self.lindentlevel))

	def startLoop(self, n):
		for j in range(0, n):
			ind = self.genindent(self.lindentlevel)
			print('%sWhile data_mem[data_ptr] > 0 do' % ind)
			print('%sBegin' % ind)
			self.lindentlevel += 1

	def finishLoop(self, n, dot):
		for j in range(0, n):
			self.lindentlevel -= 1
			print('%sEnd;' % self.genindent(self.lindentlevel))

	def emitProgramBootstrap(self):
		print('Program My_Brainfuck_application;')
		print('Uses Crt;')
		print('')

		for i in self.copyrightNotice:
			print('(* %s *)' % i)
		print('')

	def emitFunctions(self):
		print('Var')
		ind = self.genindent(self.lindentlevel)
		print('%sdata_mem : Array[0..32767] of Byte;' % ind)
		print('%sdata_ptr : Integer;' % ind)
		print('%si : Integer;' % ind)
		print('')

		for blkLoop in range(0, len(self.blocks)):
			print('Procedure f%d;' % blkLoop)
			print('Begin')

			self.lindentlevel += 1
			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
			self.lindentlevel -= 1

			print('End;')
			print('')

	def emitMainFunction(self):
		print('Begin')

		self.lindentlevel += 1
		ind = self.genindent(self.lindentlevel)

		print('%sdata_ptr := 0;' % ind)

		print('%sfor i := 0 to 32767 do' % ind)
		print('%sbegin' % ind)
		self.lindentlevel += 1
		print('%sdata_mem[i] := 0;' % self.genindent(self.lindentlevel))
		self.lindentlevel -= 1
		print('%send;' % ind)

		self.lindentlevel -= 1

		self.translate(0, len(self.allCode))

		print('End.')

	def addComment(self, s):
		print('(* %s *)' % s)

	def multilineCommentStart(self):
		print('(*')

	def multilineCommentLine(self, s):
		print(' * %s' % s)

	def multilineCommentEnd(self):
		print(' *)')
