#! /usr/bin/python

# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_java import CompileToJava

class CompileToCSharp(CompileToJava):
	def header(self):
		print >>sys.stderr, 'Brainfuck to C# compiler.'

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
			print '%sConsole.Write((char)data_mem[data_ptr]);' % ind

	def addComment(self, s):
		print '/* %s */' % s

	def multilineCommentStart(self):
		print '/*'

	def multilineCommentLine(self, s):
		print ' * %s' % s

	def multilineCommentEnd(self):
		print ' */'

	def emitProgramBootstrap(self):
		print 'using System;'
		print ''

		for i in self.copyrightNotice:
			print '// %s' % i
		print ''

		print 'class BrainfuckProgram {'
		self.lindentlevel += 1
		ind = self.genindent(self.lindentlevel)

		print '%sint data_ptr = 0;' % ind
		print '%sint memory_size = 32768;' % ind
		print '%sshort [] data_mem;' % ind
		print ''

	def emitMainFunction(self):
		print '%spublic void run() {' % self.genindent(self.lindentlevel)
		self.lindentlevel += 1
		print '%sdata_mem = new short[memory_size];' % self.genindent(self.lindentlevel)
		print ''
		self.translate(0, len(self.allCode))
		self.lindentlevel -= 1
		print '%s}' % self.genindent(self.lindentlevel)
		print ''

		print '%sstatic void Main() {' % self.genindent(self.lindentlevel)
		self.lindentlevel += 1
		print '%sBrainfuckProgram bp = new BrainfuckProgram();' % self.genindent(self.lindentlevel)
		print '%sbp.run();' % self.genindent(self.lindentlevel)
		self.lindentlevel -= 1

		print '%s}' % self.genindent(self.lindentlevel)

		self.lindentlevel -= 1
		print '%s}' % self.genindent(self.lindentlevel)
