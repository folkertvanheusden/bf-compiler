brainfuck to * compiler
-----------------------

Invoke with:

    python compile_brainfuck_to.py language myprogram.bf > myprogram.ext

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


PDP11
-----
    pdpy11 myprogram.asm -o myprogram.raw

Pdpy11 (the assembler) can be obtained from https://github.com/pdpy11/pdpy11


Rust
----

rustc -C opt-level=3 program.rs


SPARC
-----
In Solaris:

    as -Q n -b -L myprogram.s
    ld a.out -o myprogram
    ./myprogram


(C) 2016-2024 by folkert@vanheusden.com
