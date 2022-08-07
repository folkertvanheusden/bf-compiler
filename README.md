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
as -o myprogram.o myprogram.asm && ld -s -o myprogram myprogram.o


c++
---
g++ -Ofast -fomit-frame-pointer -march=native myprogram.cpp



(C) 2016-2022 by folkert@vanheusden.com
