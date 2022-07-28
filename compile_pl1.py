# Written by Folkert van Heusden
# Released in the public domain

# www.vanheusden.com

import sys

from compile_ada import CompileToAda

class CompileToPL1(CompileToAda):
	loopNr = 0
	lnrs = []
	functionsFirst = False

	def header(self):
		print('Brainfuck to PL1 compiler.', file=sys.stderr)

        def addToDataPtr(self, n, dot):
		print('%sdata_ptr = data_ptr + %d;' % (self.genindent(self.lindentlevel), n))

        def subFromDataPtr(self, n, dot):
		print('%sdata_ptr = data_ptr - %d;' % (self.genindent(self.lindentlevel), n))

	def addToData(self, n, dot):
		print('%sdata_mem(data_ptr) = data_mem(data_ptr) + %d;' % (self.genindent(self.lindentlevel), n))

	def subFromData(self, n, dot):
		print('%sdata_mem(data_ptr) = data_mem(data_ptr) - %d;' % (self.genindent(self.lindentlevel), n))

        def invokeFunction(self, funcNr):
                print('%scall f%d(data_mem, data_ptr);' % (self.genindent(self.lindentlevel), funcNr))

	def emitCharacter(self, n, dot):
		ind = self.genindent(self.lindentlevel)
		ind2 = self.genindent(self.lindentlevel + 1)

		print('%sci = data_mem(data_ptr);' % ind)
		for i in range(0, n):
			print('%sif ci = 10 then' % ind)
			print('%sput skip;' % ind2)
			print('%selse' % ind)
			print('%sput edit (c) (A);' % ind2)

	def startLoop(self, n):
		for j in range(0, n):
			print('%sdo while (1 = 1);' % self.genindent(self.lindentlevel))
			self.lindentlevel += 1
			print('%sif data_mem(data_ptr) = 0 then' % self.genindent(self.lindentlevel))
			print('%sleave;' % self.genindent(self.lindentlevel + 1))

	def finishLoop(self, n, dot):
		for j in range(0, n):
			self.lindentlevel -= 1
			print('%send;' % self.genindent(self.lindentlevel))

	def emitProgramBootstrap(self):
		for i in self.copyrightNotice:
			print('/* %s */' % i)
		print('')

	def emitFunctions(self):
		for blkLoop in range(0, len(self.blocks)):
			print('f%d: proc(data_mem, data_ptr);' % blkLoop)
			self.lindentlevel += 1
			ind = self.genindent(self.lindentlevel)
			print('%sDCL data_mem(*) fixed decimal(4);' % ind)
			print('%sDCL data_ptr decimal;' % ind)
			print('%sdeclare 1 u union,' % ind)
			print('%s      2 c char(1),' % ind)
			print('%s      2 ci fixed binary(4) unsigned;' % ind)
			print('')

			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
			self.lindentlevel -= 1

			print('')
			#print 'end f%d;' % blkLoop
			print('end;')
			print('')

	def emitMainFunction(self):
		print('My_Brainfuck_application: proc options ( main );')
		print('')

		self.lindentlevel += 1
		ind = self.genindent(self.lindentlevel)

		print('%sDCL data_mem(0 : 32767) fixed decimal(4);' % ind)
		print('%sDCL data_ptr decimal;' % ind)
		print('%sDCL i decimal;' % ind)
		print('%sdeclare 1 u union,' % ind)
		print('%s      2 c char(1),' % ind)
		print('%s      2 ci fixed binary(4) unsigned;' % ind)
		print('')

		print('%sdata_ptr = 0;' % ind)
		print('')

		print('%sdo i = 0 to 32767;' % ind)
		self.lindentlevel += 1
		print('%sdata_mem(i) = 0;' % self.genindent(self.lindentlevel))
		self.lindentlevel -= 1
		print('%send;' % ind)
		print('')

		self.translate(0, len(self.allCode))

		print('%sreturn;' % ind)
		print('')

	def emitProgramTail(self):
		print('end My_Brainfuck_application;')

	def addComment(self, s):
		print('/* %s */' % s)

	def multilineCommentStart(self):
		print('/*')

	def multilineCommentLine(self, s):
		print(' * %s' % s)

	def multilineCommentEnd(self):
		print(' */')
