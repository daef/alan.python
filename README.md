# Alan.Python

A small hack to run exports from

https://focs.ist.tugraz.at/turingmachine/

# Usage
Print help
```bash
python3 tu.py -h
usage: tu.py [-h] --json JSON [--debug] [--tape] [--testcases {4,6,8}]

Turing machine test-script by Daef (modified by Chr0x6eOs).

optional arguments:
  -h, --help            show this help message and exit
  --json JSON, -j JSON  Json file containing Turing machine settings
  --debug, -d           Turn on debug
  --tape , -t           Tape to test
  --testcases {4,6,8}, -tc {4,6,8}
                        Amount of bits create possible testcases for addition
```

## Tape

You can supply a tape to test using the `--tape` flag:
```bash
python3 tu.py --json addition.json --tape "1010+0101" | tail -n 2
_1111______
 ^- End
```

## Testcases

You can specify how many bit additions to test:
```bash
python3 tu.py --json addition.json --testcases 4
You are about to run 16 testcases! Continue? [Y/n] 
[1/16] Running testcase: 0000+0000:
...
_0000______
 ^- End
[2/16] Running testcase: 0001+0001:
  ...
_0010______
^- End
  ...
[16/16] Running testcase: 1111+1111:
  ...
_0000
^- Overflow
```

If you combine `--tape` with `--testcases` you can run a further testcase:
```bash
python3 tu.py --json addition.json --testcases 4 --tape "101011+00011"
You are about to run 17 testcases! Continue? [Y/n] 
[1/17] Running testcase: 101011+00011:
...
_101110_______
 ^- End
  ...
[17/17] Running testcase: 1111+1111:
  ...
_0000
^- Overflow
```

## TestAll

You can specify how many bit additions to test:
```bash
python3 tu.py --json addition.json --testall 4
TestAll Complete: Congratulations! There were no problems found!

python3 tu.py --json addition.json --testall 4
Error at ['1', '1', '1', '1'] + ['0', '0', '0', '0']: Did not terminate in state "End". Ended in state Overflow
TestAll Complete: See above for errors in your program!
```
Note that (depending on your hardware) your computer may not handle anything above ~6 bits, so start with less and work your way up! 
