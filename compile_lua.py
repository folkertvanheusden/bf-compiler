#! /usr/bin/python

# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_base import CompileBase

class CompileToLua(CompileBase):
	def header(self):
		print >>sys.stderr, 'Brainfuck to Lua compiler.'

	def genindent(self, level):
		return ' ' * (level * 4)

	def invokeFunction(self, funcNr):
		print '%sf%d()' % (self.genindent(self.lindentlevel), funcNr)

	def addToDataPtr(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_ptr = data_ptr + %d' % (ind, n)

	def subFromDataPtr(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_ptr = data_ptr - %d' % (ind, n)

	def addToData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_mem[data_ptr] = data_mem[data_ptr] + %d' % (ind, n)

	def subFromData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_mem[data_ptr] = data_mem[data_ptr] - %d' % (ind, n)

	def emitCharacter(self, n, dot):
		for i in xrange(0, n):
			print '%sio.write(string.char(data_mem[data_ptr]))' % self.genindent(self.lindentlevel)

	def startLoop(self, n):
		for j in xrange(0, n):
			print '%swhile data_mem[data_ptr] > 0 do' % self.genindent(self.lindentlevel)
			self.lindentlevel += 1

	def finishLoop(self, n, dot):
		for j in xrange(0, n):
			self.lindentlevel -= 1
			print '%send' % self.genindent(self.lindentlevel)

	def addComment(self, s):
		print '-- %s' % s

	def multilineCommentStart(self):
		print '--'

	def multilineCommentLine(self, s):
		print '-- %s' % s

	def multilineCommentEnd(self):
		print '--'

	def emitProgramBootstrap(self):
		self.addComments(self.copyrightNotice)
		print ''
		print 'data_ptr = 1'
		print ''
		print 'memory_size = 32768'
		print 'data_mem = { }'
		print 'for i=1, memory_size do'
		print '%sdata_mem[i] = 0' % self.genindent(1)
		print 'end'
		print ''

	def emitFunctions(self):
		self.lindentlevel += 1

		for blkLoop in xrange(0, len(self.blocks)):
			print 'function f%d()' % blkLoop

			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])

			print 'end'

		self.lindentlevel -= 1

	def emitMainFunction(self):
		self.lindentlevel += 1

		self.translate(0, len(self.allCode))

		self.lindentlevel -= 1
