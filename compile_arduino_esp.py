#! /usr/bin/python

# Written by Folkert van Heusden
# Released under AGPL v3.0

# This file was obtained from https://www.vanheusden.com/misc/blog/2016-05-19_brainfuck_compilers_compared.php

import sys

from compile_arduino import CompileToArduino

class CompileToArduinoESP(CompileToArduino):
	def header(self):
		print >>sys.stderr, 'Brainfuck to Arduino-for-ESP8266 compiler.'

	def emitCharacter(self, n, dot):
		ind = self.genindent(self.lindentlevel)

		print '%syield();' % ind

		for i in xrange(0, n):
			print '%sSerial.print((char)data_mem[data_ptr]);' % ind

	def emitProgramBootstrap(self):
		print '#include <stdint.h>'
		print ''

		print 'uint8_t data_mem[32768];'
		print 'uint16_t data_ptr = 0;'
		print ''

		self.addComments(self.copyrightNotice)
		print ''

		print 'void setup() {'
		self.lindentlevel += 1
		print '%sSerial.begin(115200);' % self.genindent(self.lindentlevel)
		print '%sSerial.println(F("Brainfuck for Arduino"));' % self.genindent(self.lindentlevel)
		self.lindentlevel -= 1
		print '}'
