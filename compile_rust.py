# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_base import CompileBase

class CompileToRust(CompileBase):
	loopNr = 0
	lnrs = []

	def header(self):
		print >>sys.stderr, 'Brainfuck to Rust compiler.'

	def genindent(self, level):
		return ' ' * (level * 3)

	def invokeFunction(self, funcNr):
		print '%sf%d();' % (self.genindent(self.lindentlevel), funcNr)

	def addToDataPtr(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_ptr = data_ptr.wrapping_add(%d);' % (ind, n)

	def subFromDataPtr(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_ptr = data_ptr.wrapping_sub(%d);' % (ind, n)

	def addToData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_mem[data_ptr] = data_mem[data_ptr].wrapping_add(%d);' % (ind, n)

	def subFromData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%sdata_mem[data_ptr] = data_mem[data_ptr].wrapping_sub(%d);' % (ind, n)

	def emitCharacter(self, n, dot):
		for i in xrange(0, n):
                    print '%sprint!("{}", char::from(data_mem[data_ptr]));' % self.genindent(self.lindentlevel)

	def startLoop(self, n):
		for j in xrange(0, n):
                    print '%swhile data_mem[data_ptr] > 0 {' % self.genindent(self.lindentlevel)
                    self.lindentlevel += 1

	def finishLoop(self, n, dot):
		for j in xrange(0, n):
                    self.lindentlevel -= 1
                    print '%s}' % self.genindent(self.lindentlevel)

	def addComment(self, s):
		print '// %s' % s

	def multilineCommentStart(self):
		print '//*'

	def multilineCommentLine(self, s):
		print ' * %s' % s

	def multilineCommentEnd(self):
		print '//*'

	def emitProgramBootstrap(self):
		for i in self.copyrightNotice:
			print '// %s' % i
		print ''

                print 'static mut data_ptr: usize = 0;'
                print 'static mut data_mem: [u8; 32768] = [0; 32768];'
		print ''

	def emitFunctions(self):
		for blkLoop in xrange(0, len(self.blocks)):
			print '%sfn f%d() {' % (self.genindent(self.lindentlevel), blkLoop)

			self.lindentlevel += 1
			print '%sunsafe {' % self.genindent(self.lindentlevel)
			self.lindentlevel += 1
			self.translate(self.blocks[blkLoop][0], self.blocks[blkLoop][1])
			self.lindentlevel -= 1
			print '%s}' % self.genindent(self.lindentlevel)
			self.lindentlevel -= 1

			print '%s}' % self.genindent(self.lindentlevel)

	def emitMainFunction(self):
		print 'fn main() {'

		self.lindentlevel += 1
		print '%sunsafe {' % self.genindent(self.lindentlevel)
		self.lindentlevel += 1
		print '%s data_ptr = 0;' % self.genindent(self.lindentlevel)

		self.translate(0, len(self.allCode))
		self.lindentlevel -= 1
		print '%s}' % self.genindent(self.lindentlevel)
		self.lindentlevel -= 1

		print '}'
