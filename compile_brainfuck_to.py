#! /usr/bin/python

# Written by Folkert van Heusden
# Released in the public domain

import sys

from compile_ada import CompileToAda
from compile_arduino import CompileToArduino
from compile_arduino_esp import CompileToArduinoESP
from compile_arm import CompileToARM
from compile_bash import CompileToBash
from compile_cobol import CompileToCOBOL
from compile_c import CompileToC
from compile_c64 import CompileToC64
from compile_csharp import CompileToCSharp
from compile_go import CompileToGo
from compile_hlasm import CompileToHLASM
from compile_java import CompileToJava
from compile_javascript import CompileToJavascript
from compile_lua import CompileToLua
from compile_msx import CompileToMSX
from compile_pascal import CompileToPascal
from compile_perl import CompileToPerl
from compile_perl6 import CompileToPerl6
from compile_php import CompileToPHP
from compile_pl1 import CompileToPL1
from compile_python import CompileToPython
from compile_ruby import CompileToRuby
from compile_rust import CompileToRust
from compile_scala import CompileToScala
from compile_sdlbasic import CompileToSDLBasic
from compile_x86 import CompileToX86

if len(sys.argv) != 2:
	print('Usage: %s target' % sys.argv[0])
	print('')
	print('Target being:')
	print('\tAda')
	print('\tArduino')
	print('\tArduinoESP')
	print('\tARM')
	print('\tBash')
	print('\tCOBOL')
	print('\tC')
	print('\tC64')
	print('\tC#')
	print('\tGo')
	print('\tHLASM')
	print('\tJava')
	print('\tJavascript')
	print('\tLua')
	print('\tMSX (z80 assembly code)')
	print('\tPascal')
	print('\tPerl')
	print('\tPerl6')
	print('\tPHP')
	print('\tPL/1')
	print('\tPython')
	print('\tRuby')
	print('\tRust')
	print('\tScala')
	print('\tSDLBasic')
	print('\tx86 (assembly, at&t notation)')
	sys.exit(1)

which = sys.argv[1].lower()

obj = None
if which == 'ada':
	obj = CompileToAda()

elif which == 'arduino':
	obj = CompileToArduino()

elif which == 'arduinoesp':
	obj = CompileToArduinoESP()

elif which == 'arm':
	obj = CompileToARM()

elif which == 'bash':
	obj = CompileToBash()

elif which == 'cobol':
	obj = CompileToCOBOL()

elif which == 'c':
	obj = CompileToC()

elif which == 'c64':
	obj = CompileToC64()

elif which == 'c#':
	obj = CompileToCSharp()

elif which == 'go':
	obj = CompileToGo()

elif which == 'hlasm':
       obj = CompileToHLASM()

elif which == 'java':
	obj = CompileToJava()

elif which == 'javascript':
	obj = CompileToJavascript()

elif which == 'lua':
	obj = CompileToLua()

elif which == 'msx':
	obj = CompileToMSX()

elif which == 'pascal':
	obj = CompileToPascal()

elif which == 'perl':
	obj = CompileToPerl()

elif which == 'perl6':
	obj = CompileToPerl6()

elif which == 'php':
	obj = CompileToPHP()

elif which == 'pl1' or which == 'pl/1':
	obj = CompileToPL1()

elif which == 'python':
	obj = CompileToPython()

elif which == 'ruby':
	obj = CompileToRuby()

elif which == 'rust':
	obj = CompileToRust()

elif which == 'scala':
	obj = CompileToScala()

elif which == 'sdlbasic':
	obj = CompileToSDLBasic()

elif which == 'x86':
	obj = CompileToX86()

else:
	print('Error: %s is not known' % which)
	sys.exit(1)

obj.main()
