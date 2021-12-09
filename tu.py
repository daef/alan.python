#!/usr/bin/env python3

# Credit: daef
# Modified by Chr0x6eOs

import json, sys, argparse, itertools

last_ts = ''
def print_tape(tape, only_if_new):
  global last_ts
  ts = ''.join(tape)
  if not only_if_new or last_ts != ts:
      print(ts)
  last_ts = ts

def print_cursor(cur, state):
  print(f'{" "*cur}^- {state}')

def run_testcases(json_data, dbg, bit_count, tape=""):
  testcases = []
  binary_num = []

  for count in range(2, bit_count + 1):
    binary_num.append(["".join(i) for i in itertools.product(["0", "1"], repeat=count)])

  for binary_range in binary_num:
    for binary in ["".join(i) for i in itertools.product(binary_range, repeat=2)]:
      testcases.append(f"{binary}+{binary}")

  if tape != "":
    testcases.insert(0, tape)

  count = 0

  run = input(f"You are about to run {len(testcases)} testcases! Continue? [Y/n] ").lower()
  if(run in ["no","n"]):
    print("OK! Stopping...")
    return

  for testcase in testcases:
    count += 1
    print(f"[{count}/{len(testcases)}] Running testcase: {testcase}:\n")
    solve(json_data, tape=testcase)

def solve(json_data, dbg=False, tape = ""):
  results = []

  init = json_data['initial_tape']
  null = init['blank_symbol']
  if tape != "":
    tape = [c for c in tape]
    cur = len(tape)
    tape.append(null)
  else:
      tape = init['data']
      cur = init['cursor']
  state = json_data['initial_state']
  fin = json_data['final_states']
  prg = json_data['program']

  while not state in fin:
    r = tape[cur]
    matches = [x for x in prg if x[0] == r and x[1] == state]
    print_tape(tape, not dbg)
    if dbg:
        results.append(print_cursor(cur, state))
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
  results.append(print_cursor(cur, state))
  return results

def log_results(results):
  pass

def main(args):
  parser = argparse.ArgumentParser(description='Turing machine test-script by Daef (modified by Chr0x6eOs).')
  parser.add_argument('--json', '-j', required=True, help='Json file containing Turing machine settings', type=str)
  parser.add_argument('--debug', '-d', help='Turn on debug', default=False, action='store_true')
  parser.add_argument('--tape', '-t', help='Tape to test', metavar="", type=str)
  parser.add_argument('--testcases', '-tc', help='Amount of bits create possible testcases for addition', choices=[4, 6, 8], type=int)
  args = parser.parse_args()

  if not any(vars(args).values()):
      parser.print_help()
      exit(1)

  json_data = None
  tape = ""

  try:
    json_data = json.load(open(args.json))
  except Exception as ex:
    print(f"[-] Error while loading json: {ex}")
    exit(1)

  if args.tape:
    tape = args.tape

  if args.testcases:
    run_testcases(json_data, args.debug, int(args.testcases / 2), tape)
  else:
    solve(json_data, args.debug, tape)

if __name__ == "__main__":
    main(sys.argv)