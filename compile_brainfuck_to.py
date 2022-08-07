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
from compile_lisp import CompileToLisp
from compile_lua import CompileToLua
from compile_mips import CompileToMIPS
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

targets[CompileToAda.get_name()[0]] = (CompileToAda(), CompileToAda.get_name()[1])
targets[CompileToArduinoESP.get_name()[0]] = (CompileToArduinoESP(), CompileToArduinoESP.get_name()[1])
targets[CompileToArduino.get_name()[0]] = (CompileToArduino(), CompileToArduino.get_name()[1])
targets[CompileToARM.get_name()[0]] = (CompileToARM(), CompileToARM.get_name()[1])
targets[CompileToBash.get_name()[0]] = (CompileToBash(), CompileToBash.get_name()[1])
targets[CompileToC64.get_name()[0]] = (CompileToC64(), CompileToC64.get_name()[1])
targets[CompileToCOBOL.get_name()[0]] = (CompileToCOBOL(), CompileToCOBOL.get_name()[1])
targets[CompileToC.get_name()[0]] = (CompileToC(), CompileToC.get_name()[1])
targets[CompileToCSharp.get_name()[0]] = (CompileToCSharp(), CompileToCSharp.get_name()[1])
targets[CompileToGo.get_name()[0]] = (CompileToGo(), CompileToGo.get_name()[1])
targets[CompileToHLASM.get_name()[0]] = (CompileToHLASM(), CompileToHLASM.get_name()[1])
targets[CompileToJava.get_name()[0]] = (CompileToJava(), CompileToJava.get_name()[1])
targets[CompileToJavascript.get_name()[0]] = (CompileToJavascript(), CompileToJavascript.get_name()[1])
targets[CompileToLisp.get_name()[0]] = (CompileToLisp(), CompileToLisp.get_name()[1])
targets[CompileToLua.get_name()[0]] = (CompileToLua(), CompileToLua.get_name()[1])
targets[CompileToMSX.get_name()[0]] = (CompileToMSX(), CompileToMSX.get_name()[1])
targets[CompileToPascal.get_name()[0]] = (CompileToPascal(), CompileToPascal.get_name()[1])
targets[CompileToPDP11.get_name()[0]] = (CompileToPDP11(), CompileToPDP11.get_name()[1])
targets[CompileToPerl6.get_name()[0]] = (CompileToPerl6(), CompileToPerl6.get_name()[1])
targets[CompileToPerl.get_name()[0]] = (CompileToPerl(), CompileToPerl.get_name()[1])
targets[CompileToPHP.get_name()[0]] = (CompileToPHP(), CompileToPHP.get_name()[1])
targets[CompileToPL1.get_name()[0]] = (CompileToPL1(), CompileToPL1.get_name()[1])
targets[CompileToPython.get_name()[0]] = (CompileToPython(), CompileToPython.get_name()[1])
targets[CompileToRuby.get_name()[0]] = (CompileToRuby(), CompileToRuby.get_name()[1])
targets[CompileToRust.get_name()[0]] = (CompileToRust(), CompileToRust.get_name()[1])
targets[CompileToScala.get_name()[0]] = (CompileToScala(), CompileToScala.get_name()[1])
targets[CompileToSDLBasic.get_name()[0]] = (CompileToSDLBasic(), CompileToSDLBasic.get_name()[1])
targets[CompileToX86.get_name()[0]] = (CompileToX86(), CompileToX86.get_name()[1])

if len(sys.argv) != 2:
    print('Usage: %s target < file-in.bf > file-out.ext' % sys.argv[0])
    print('')
    print('Target being:')
    for target in targets:
        descr = targets[target][1]

        if descr != None:
            print(f'\t{target}\t({descr})')

        else:
            print(f'\t{target}')

    sys.exit(1)

which = sys.argv[1].lower()

if not which in targets:
    print(f'Error: {which} is not known')

    sys.exit(1)

targets[which][0].main()
