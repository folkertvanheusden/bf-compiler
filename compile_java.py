#! /usr/bin/python

# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_c import CompileToC

class CompileToJava(CompileToC):
	def header(self):
		print >>sys.stderr, 'Brainfuck to Java compiler.'

	def addToData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		if n == 1:
			print '%sdata_mem[data_ptr]++;' % ind
		else:
			print '%sdata_mem[data_ptr] += %d;' % (ind, n)

		print '%sdata_mem[data_ptr] &= 255;' % ind

	def subFromData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		if n == 1:
			print '%sdata_mem[data_ptr]--;' % ind
		else:
			print '%sdata_mem[data_ptr] -= %d;' % (ind, n)

		print '%sdata_mem[data_ptr] &= 255;' % ind

	def emitCharacter(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		for i in xrange(0, n):
			print '%sSystem.out.print((char)data_mem[data_ptr]);' % ind

		print '%sSystem.out.flush();' % ind

	def emitProgramBootstrap(self):
		for i in self.copyrightNotice:
			print '// %s' % i
		print ''

		print 'class BrainfuckProgram {'
		self.lindentlevel += 1
		ind = self.genindent(self.lindentlevel)

		print '%sint data_ptr = 0;' % ind
		print '%sint memory_size = 32768;' % ind
		print '%sshort [] data_mem = new short[memory_size];' % ind
		print ''

	def emitMainFunction(self):
		print '%spublic void run() {' % self.genindent(self.lindentlevel)
		self.lindentlevel += 1
		self.translate(0, len(self.allCode))
		self.lindentlevel -= 1
		print '%s}' % self.genindent(self.lindentlevel)
		print ''

		print '%spublic static void main(String [] args) {' % self.genindent(self.lindentlevel)
		self.lindentlevel += 1
		print '%sBrainfuckProgram bp = new BrainfuckProgram();' % self.genindent(self.lindentlevel)
		print '%sbp.run();' % self.genindent(self.lindentlevel)
		self.lindentlevel -= 1

		print '%s}' % self.genindent(self.lindentlevel)

		self.lindentlevel -= 1
		print '%s}' % self.genindent(self.lindentlevel)
