#! /usr/bin/python3

import copy
import math
import os
import random
import sys
import time


target = sys.argv[1]

def fitness(target, output, program):
    l_t = len(target)
    l_o = len(output)
    score = len(program) / 10
    for i in range(max(l_t, l_o)):
        if i < l_t and i < l_o:
            score += math.pow(abs(ord(target[i]) - ord(output[i])), 1.5)
        elif i < l_o:
            score += math.pow(ord(output[i]), 2)
        else:
            score += math.pow(ord(target[i]), 1.9)
    return score


def run(program, max_run_time, target, stack_limit):
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
            if len(stack) > stack_limit:
                return None
        elif instruction == ']':
            if len(stack) == 0:
                return None
            if memory[memory_pointer] > 0:
                new_pc = stack.pop()

        pc = new_pc

    if output == '':
        return None

    return output


best_ratio = 10000000000000000000000000
best = None

target_len = len(target)
size = random.randint(1, target_len * target_len)

start = time.time()
pts = start
n = 0
pn = 0
max_t_per_s_i = 0  # transactions per second
n_restarts = 0

duplicates = 0
fails = 0

instructions = ('[', ']', '.', '>', '<', '+', '-')
n_instr = len(instructions)
while True:
    n_restarts += 1

    program = ''

    history = set()
    for i in range(10000):
        n += 1

        now = time.time()
        t_diff = now - start;
        if now - pts >= 1.0:
            t_per_s = n / t_diff
            pts = now
            print(f'Tried {n} in {t_diff:.2f} seconds or {t_per_s:.2f} per second, restarts: {n_restarts}, duplicates: {duplicates}, fails: {fails}')

        if len(program) >= 3:
            action = random.randint(1, 4)
        else:
            action = 2
        if action == 1:
            new_program = ''.join(random.sample(program, len(program)))
        elif action == 2:
            new_program = copy.copy(program)
            for i in range(random.randint(1, len(program) + 1)):
                new_program += random.choice(instructions)
        elif action == 3:
            new_program = copy.copy(program)
            do_n = random.randint(0, len(new_program) * 2 // 3)
            for k in range(do_n):
                idx = random.randint(0, len(new_program))
                new_program = new_program[0:idx] + new_program[idx+1:]
        elif action == 4:
            new_program = copy.copy(program)
            if random.randint(0, 1) == 0 or len(new_program) <= 3:
                for i in range(random.randint(1, len(new_program) + 1)):
                    idx = random.randint(0, len(new_program))
                    new_program = new_program[0:idx] + random.choice(instructions[2:]) + new_program[idx+1:]
            else:
                while True:
                    idx1 = random.randint(0, len(new_program))
                    idx2 = random.randint(0, len(new_program))
                    if idx1 < idx2:
                        break
                new_program = new_program[0:idx1] + '[' + new_program[idx1:]
                new_program = new_program[0:idx2] + ']' + new_program[idx2:]
                
        if new_program[-1] != ']' and new_program[-1] != '.':
            program = new_program
            continue

        loop_count = 0
        for i in new_program:
            if i == '[':
                loop_count += 1
            elif i == ']':
                loop_count -= 1

        if loop_count != 0:
            fails += 1
            continue

        if new_program in history:
            duplicates += 1
            continue
        history.add(new_program)

        output = run(new_program, 0.5, target, 255)
        if program == None or output == None:
            continue

        r = fitness(target, output, new_program)
        if best_ratio is None or r <= best_ratio:
            best = output
            best_ratio = r
            program = new_program
            print(best_ratio, program, best)
