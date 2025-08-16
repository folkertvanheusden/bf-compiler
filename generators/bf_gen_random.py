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
        instruction_count = random.randint(1, 255)

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

        result += instruction * instruction_count

    return result


def run(program, max_run_time, target):
    end_time = time.time() + max_run_time

    program_len = len(program)
    pc = 0

    memory_len = 32000
    memory = [ 0 ] * memory_len
    memory_pointer = 0

    output = ''

    stack = []

    while pc < program_len and time.time() < end_time:
        instruction = program[pc]
        new_pc = pc + 1

        if instruction == '.':
            new_c = chr(memory[memory_pointer])
            output += new_c
            if len(output) > len(target) or output != target[0:len(output)]:
                return False
        elif instruction == '+':
            memory[memory_pointer] += 1
            memory[memory_pointer] &= 255
        elif instruction == '-':
            memory[memory_pointer] -= 1
            memory[memory_pointer] &= 255
        elif instruction == '>':
            memory_pointer += 1
            if memory_pointer >= memory_len:
                break
        elif instruction == '<':
            memory_pointer -= 1
            if memory_pointer < 0:
                break
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


if run('>++++++++[<+++++++++>-]<.>+++++[<+++++>-]<.+++++++++++..+++.>++++++[<----------->-]<-.------------.>++++++[<+++++++++++>-]<++.+++++.+++++++++++.>+++++++[<------------>-]<.>++++++++[<+++++++++>-]<+.++++++++++.>+++++++++[<--------->-]<--.>+++++++[<++++++++++>-]<-..+++++++++.>+++++++[<----------->-]<-.>+++++++[<++++++++++++>-]<.---------------.++++++++++++++.+.>+++++++[<---------->-]<.', 1.0, 'Hallo, dit is een test.') == True:
    print('Self test succeeded')
else:
    print('Self test FAILED')
    sys.exit(1)

print('Go!')

start = time.time()
pts = start
n = 0

while True:
    program = try_produce(target)
    verify = run(program, 0.5, target)
    if verify:
        print(f'Found {target}: {program}')
        break

    n += 1

    now = time.time()
    t_diff = now - start;
    if now - pts >= 1.0:
        print(f'Tried {n} in {t_diff:.2f} seconds or {n / t_diff:.2f} per second')
        pts = now
