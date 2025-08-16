#! /usr/bin/python3

import random
import sys
import time


target = sys.argv[1]

def try_produce(target):
    target_len = len(target)
    dot_count = 0
    loop_counter = 0

    result = ''

    while dot_count < target_len:
        instruction = random.choice(('>', '<', '+', '-', '.', '[', ']'))
        instruction_count = random.randint(0, target_len)

        if instruction == ']':
            instruction_count = min(instruction_count, loop_counter)
            if instruction_count == 0:
                continue
            loop_counter -= instruction_count

        elif instruction == '[':
            loop_counter += instruction_count

        elif instruction == '.':
            instruction_count = min(instruction_count, target_len - dot_count)
            if instruction_count == 0:
                continue
            dot_count += instruction_count

        for i in range(0, instruction_count):
            result += instruction

    return result


def run(program, max_run_time, target):
    start = time.time()

    program_len = len(program)
    pc = 0

    memory_len = 32000
    memory = [ 0 ] * memory_len
    memory_pointer = 0

    output = ''

    stack = []

    while pc < program_len and output != target and time.time() - start < max_run_time:
        instruction = program[pc]
        new_pc = pc + 1

        if instruction == '.':
            output += chr(memory[memory_pointer])
        elif instruction == '+':
            memory[memory_pointer] += 1
            memory[memory_pointer] &= 255
        elif instruction == '-':
            memory[memory_pointer] -= 1
            memory[memory_pointer] &= 255
        elif instruction == '>':
            memory_pointer += 1
            memory_pointer %= memory_len
        elif instruction == '<':
            memory_pointer -= 1
            if memory_pointer < 0:
                memory_pointer += memory_len
        elif instruction == '[':
            stack.append(pc)
            if len(stack) > memory_len:
                return False
        elif instruction == ']':
            if len(stack) == 0:
                return False
            if memory[memory_pointer] > 0:
                new_pc = stack.pop()

        pc = new_pc

    return output == target


assert run('>++++++++[<+++++++++>-]<.>+++++[<+++++>-]<.+++++++++++..+++.>++++++[<----------->-]<-.------------.>++++++[<+++++++++++>-]<++.+++++.+++++++++++.>+++++++[<------------>-]<.>++++++++[<+++++++++>-]<+.++++++++++.>+++++++++[<--------->-]<--.>+++++++[<++++++++++>-]<-..+++++++++.>+++++++[<----------->-]<-.>+++++++[<++++++++++++>-]<.---------------.++++++++++++++.+.>+++++++[<---------->-]<.', 1.0, 'Hallo, dit is een test.') == True

print('Go!')

while True:
    program = try_produce(target)
    verify = run(program, 0.5, target)

    if verify:
        print(f'Found {target}: {program}')
        break
