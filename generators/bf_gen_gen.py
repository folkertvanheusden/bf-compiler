#! /usr/bin/python3

import multiprocessing as mp
import jellyfish
import random
import sys
import time


target = sys.argv[1]

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

def checker(q_in, q_out):
    while True:
        program = q_in.get()
        try:
            output = run(program, 0.5, target, 255)
            q_out.put((program, output))
        except Exception as e:
            print(f'Exception: {e}')
            q_out.put((None, None))

best_ratio = None
best = None

target_len = len(target)
size = random.randint(1, target_len * target_len)

start = time.time()
pts = start
n = 0
pn = 0
max_t_per_s_i = 0  # transactions per second
n_restarts = 0

q_in = mp.Queue()
q_out = mp.Queue()
procs = []
for proc in range(32):
    p = mp.Process(target=checker, args=(q_out, q_in))
    p.start()
    procs.append(p)

instructions = ('[', ']', '.', '>', '<', '+', '-')
n_instr = len(instructions)
while True:
    n_restarts += 1

    sizes = [ 0 ] * n_instr
    to_do_size = size
    while to_do_size > 0:
        idx = random.randint(0, n_instr - 1)
        if idx == 0 or idx == 1:
            if to_do_size == 1:
                continue
            sizes[0] += 1
            sizes[1] += 1
            to_do_size -= 2
        else:
            sizes[idx] += 1
            to_do_size -= 1

    program = ''
    for i in range(n_instr):
        program += instructions[i] * sizes[i]

    history = set()
    for i in range(10000):
        q_out.put(program)
        if program in history:
            break
        history.add(program)
        program = ''.join(random.sample(program, len(program)))

    for i in range(len(history)):
        program, output = q_in.get()
        if program == None or output == None:
            continue

        n += 1

        r = jellyfish.jaro_similarity(target, output)
        if best_ratio is None or r > best_ratio:
            best_ratio = r
            best = program, output
            print(best_ratio, program, output[0:25])

        now = time.time()
        t_diff = now - start;
        if now - pts >= 1.0:
            t_per_s = n / t_diff
            pts = now
            print(f'Tried {n} in {t_diff:.2f} seconds or {t_per_s:.2f} per second, restarts: {n_restarts}')
