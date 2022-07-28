#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_c import CompileToC

class CompileToArduino(CompileToC):
	def header(self):
		print >>sys.stderr, 'Brainfuck to Arduino compiler.'

	def genindent(self, level):
		return ' ' * (level * 4)

	def emitCharacter(self, n, dot):
		for i in xrange(0, n):
			print '%sSerial.print((char)data_mem[data_ptr]);' % self.genindent(self.lindentlevel)

	def emitProgramBootstrap(self):
		print '#include <stdint.h>'
		print ''

		print 'uint8_t data_mem[1536];'
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

	def emitMainFunction(self):
		self.lindentlevel += 1

		print 'void loop()'
		print '{'
		print '%sunsigned long int start = millis();' % self.genindent(self.lindentlevel)

		self.translate(0, len(self.allCode))

		print ''
		print '%sunsigned long int end = millis();' % self.genindent(self.lindentlevel)
		print '%sSerial.print(F("Took: "));' % self.genindent(self.lindentlevel)
		print '%sSerial.println(end - start);' % self.genindent(self.lindentlevel)
		print ''
		print '%sfor(;;)' % self.genindent(self.lindentlevel)
		print '%sdelay(1);' % self.genindent(self.lindentlevel + 1)

		print '}'

		self.lindentlevel -= 1
