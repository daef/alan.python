#!/usr/bin/env python3

# Credit: daef
# Modified by Chr0x6eOs, ThiemoD

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
  
def test_tape(prg, tape = [], cur = 0):
  null = '_'
  state = 'Start'
  fin = ['End','Overflow']
  n = 0
  
  while not state in fin:
    if n > 100000:
      print(f'Error:  Exceeded maximum algorithm steps (100000)')
      return False
    else: 
      n += 1
    r = tape[cur]
    matches = [x for x in prg if x[0] == r and x[1] == state]
    if len(matches) != 1:
      print(f'Error:  {len(matches)} rules matching (looking at: {r}, state: {state}, matches: {matches})')
      return False
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
  return [tape,cur,state]

def testall(json_data, bit_count=4):
  if json_data['initial_tape']['blank_symbol']!='_':
    print('Your blank symbol must be "_"!')
    return 0
  if json_data['final_states']!=['End','Overflow']:
    print('Your final states must be "End" and "Overflow"!')
    return 0
  if json_data['initial_state'] != 'Start':
    print('Your blank symbol must be "Start"!')
    return 0
    
  prg = json_data['program']
  c01 = ['0','1']
  error = False
  init_cur = 2*bit_count+1
  for i in range(2**bit_count):
    lefttape = []
    for t in range(bit_count-1,-1,-1):
      lefttape.append(c01[(i>>t)&1])
    for j in range(2**bit_count):
      righttape = []
      for t in range(bit_count-1,-1,-1):
        righttape.append(c01[(j>>t)&1])    
      tape = lefttape + ['+'] + righttape + ['_']
      
      result = test_tape(prg,tape,init_cur)
      
      if not result:
        error = True;
        print(f'       occured at {lefttape} + {righttape}!')
        break;
      elif j+i >= 2**bit_count:
        if result[2] != 'Overflow':
          print(f'Error at {lefttape} + {righttape}: Overflow not detected')
          error = True;
      else:
        if result[2] != 'End':
          print(f'Error at {lefttape} + {righttape}: Did not terminate in state "End". Ended in state {result[2]}')
          error = True;
        resTape = result[0]
        cur = result[1]
        while cur>0 and resTape[0]=='_':
          cur-=1
          resTape.pop(0)
        if cur >0:
          print(f'Error at {lefttape} + {righttape}: there are non-empty-cells before the cursor position!')
          error = True
        else:
          while len(resTape)>bit_count and resTape[len(resTape)-1] == '_':
            resTape.pop()
          if len(resTape)>bit_count:
            print(f'Error at {lefttape} + {righttape}: there are non-empty-cells at least bit_count places after the cursor position!')
            error = True
          else:
            expectedtape = []
            result = j+i
            for t in range(bit_count-1,-1,-1):
              expectedtape.append(c01[(result>>t)&1])
            if resTape != expectedtape:
              print(f'Error at {lefttape} + {righttape}: Wrong result: {resTape} instead of {expectedtape}')
              error = True
  if not error:
    print('TestAll Complete: Congratulations! There were no problems found!')
  else:
    print('TestAll Complete: See above for errors in your program!')
  
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
  parser.add_argument('--testall', '-ta', help='Amount of bits to test every single combination with', choices=[1,2,3,4,5,6,7,8,9,10], type=int)
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

  if args.testall:
    testall(json_data, args.testall)
  elif args.testcases:
    run_testcases(json_data, args.debug, int(args.testcases / 2), tape)
  else:
    solve(json_data, args.debug, tape)

if __name__ == "__main__":
    main(sys.argv)
