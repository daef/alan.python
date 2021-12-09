#!/usr/bin/env python3

import json, sys

last_ts = ''
def print_tape(tape, only_if_new):
    global last_ts
    ts = ''.join(tape)
    if not only_if_new or last_ts != ts:
        print(ts)
    last_ts = ts

def print_cursor(cur, state):
    print(f'{" "*cur}^- {state}')

def usage(args):
    print(f'usage: {args[0]} my_awesome_touring_ding.json [debug] [tape]')
    exit(1)

def main(args):
    argl = len(args)
    if argl < 2:
        usage(args)
    j = json.load(open(args[1]))

    dbg = argl > 2 and args[2] == 'debug'
    init = j['initial_tape']
    null = init['blank_symbol']
    if argl > 3 or (not dbg and argl > 2):
        tape = [c for c in args[dbg and 3 or 2]]
        cur = len(tape)
        tape.append(null)
    else:
        tape = init['data']
        cur = init['cursor']
    state = j['initial_state']
    fin = j['final_states']
    prg = j['program']
    while not state in fin:
        r = tape[cur]
        matches = [x for x in prg if x[0] == r and x[1] == state]
        print_tape(tape, not dbg)
        if dbg:
            print_cursor(cur, state)
        if len(matches) != 1:
            print(f'{len(matches)} rules matching ({matches})')
            exit(1)
        m = matches[0][2]
        tape[cur] = m[0]
        if m[1] == 'Left':
            cur -= 1
            while cur < 0:
                tape.insert(0, null)
                cur += 1
        elif m[1] == 'Right':
            cur += 1
        state = m[2]
    print_cursor(cur, state)


if __name__ == "__main__":
    main(sys.argv)

