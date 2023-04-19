brainfuck to * compiler
-----------------------

Invoke with:

	python compile_brainfuck_to.py language < myprogram.bf > myprogram.ext

Replace language with the target language and 'ext' by the appropriate extension.

Run:

	python compile_brainfuck_to.py

to see a list of target languages.


compiling the result
--------------------

ARM / X86
---------
as --64 -g --gstabs+ -o myprogram.o myprogram.asm && ld -o myprogram myprogram.o


c++
---
g++ -Ofast -fomit-frame-pointer -march=native myprogram.cpp


Java
----
javac myprogram.java

This produces a "BrainfuckProgram.class"-file which can be executed by:

java BrainfuckProgram


(C) 2016-2023 by folkert@vanheusden.com
