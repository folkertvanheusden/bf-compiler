#! /usr/bin/python3

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
from compile_pdp11 import CompileToPDP11
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

targets = dict()

targets[CompileToAda.get_name()] = CompileToAda()
targets[CompileToArduino.get_name()] = CompileToArduino()
targets[CompileToArduinoESP.get_name()] = CompileToArduinoESP()
targets[CompileToARM.get_name()] = CompileToARM()
targets[CompileToBash.get_name()] = CompileToBash()
targets[CompileToCOBOL.get_name()] = CompileToCOBOL()
targets[CompileToC.get_name()] = CompileToC()
targets[CompileToC64.get_name()] = CompileToC64()
targets[CompileToCSharp.get_name()] = CompileToCSharp()
targets[CompileToGo.get_name()] = CompileToGo()
targets[CompileToHLASM.get_name()] = CompileToHLASM()
targets[CompileToJava.get_name()] = CompileToJava()
targets[CompileToJavascript.get_name()] = CompileToJavascript()
targets[CompileToLua.get_name()] = CompileToLua()
targets[CompileToMSX.get_name()] = CompileToMSX()
targets[CompileToPascal.get_name()] = CompileToPascal()
targets[CompileToPerl.get_name()] = CompileToPerl()
targets[CompileToPerl6.get_name()] = CompileToPerl6()
targets[CompileToPDP11.get_name()] = CompileToPDP11()
targets[CompileToPHP.get_name()] = CompileToPHP()
targets[CompileToPL1.get_name()] = CompileToPL1()
targets[CompileToPython.get_name()] = CompileToPython()
targets[CompileToRuby.get_name()] = CompileToRuby()
targets[CompileToRust.get_name()] = CompileToRust()
targets[CompileToScala.get_name()] = CompileToScala()
targets[CompileToSDLBasic.get_name()] = CompileToSDLBasic()
targets[CompileToX86.get_name()] = CompileToX86()

if len(sys.argv) != 2:
    print('Usage: %s target' % sys.argv[0])
    print('')
    print('Target being:')
    for target in targets:
        print(f'\t{target}')
    sys.exit(1)

which = sys.argv[1].lower()

if not which in targets:
    print(f'Error: {which} is not known')

    sys.exit(1)

targets[which].main()
