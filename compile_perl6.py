#! /usr/bin/python

# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_perl import CompileToPerl

class CompileToPerl6(CompileToPerl):
	def header(self):
		print >>sys.stderr, 'Brainfuck to Perl6 compiler.'

	def addToData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		if n == 1:
			print '%s++@data_mem[$data_ptr];' % ind
		else:
			print '%s@data_mem[$data_ptr] += %d;' % (ind, n)

	def subFromData(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		if n == 1:
			print '%s--@data_mem[$data_ptr];' % ind
		else:
			print '%s@data_mem[$data_ptr] -= %d;' % (ind, n)

	def emitCharacter(self, n, dot):
		for i in xrange(0, n):
			print '%sprint chr(@data_mem[$data_ptr]);' % self.genindent(self.lindentlevel)

	def startLoop(self, n):
		for j in xrange(0, n):
			print '%swhile @data_mem[$data_ptr] {' % self.genindent(self.lindentlevel)
			self.lindentlevel += 1

	def emitProgramBootstrap(self):
		for i in self.copyrightNotice:
			print '# %s' % i
		print ''

		print 'my int32 $data_ptr = 0;'
		print 'my uint8 @data_mem;';
