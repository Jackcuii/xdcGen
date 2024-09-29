# xdcGen
This is a lite generator of the constraint file for the Xilinx Vivado (namely `.xdc`). 

This tool allows you to use minimum script language to generate a `.xdc`. 

It only works for Nexys A7-100T up till now, which is used in Nanjing University *Digitial Logic & Computer Organization Lab* course. 

Room for expansion has been left out. Welcome to add support for other demo boards and raise PR~


## User Guide
You could run the configure.sh, it will set the alias in your .bashrc.
Then you could run **xdcGen** with
``` shell
xdcgen your_script.xg
```

Otherwise (e.g. you are not in Linux, bash env...), you could run **xdcGen** with
```
python3 path/to/the/repo/xdcGen.py
```
### CLI Parameters
`-n` set the device.(Default it is Nexys A7-100T)

`-o` set the output file(and path). (Default is an auto-generated unique name)
### Script Syntax
The `.xg` script is composed of multiple lines.

Each line is in the form of `left exp1; exp2; ... ~ right exp1; exp2;`.

Left exp is the *real pins* on the board, and right exp is the module ports.

all the exps will be expanded, and the expanded form should have the same sum of pins.

Then each pin on the right will be bonded to the corresponding pin on the left.

exps could be in 4 forms:

#### 1. atomic expression

  a single pin: `SW1` (at left), `in[0]`(at right).
  
#### 2. range expression

  `XX|x:y:z|`or`XX|x:y|` means a range of pins, from x to y, with step z.(`y` is included)
  
  `z` is optional, and `x > y` is allowed.
  
  e.g. `SW|1:4:2|` means `SW1, SW3`, `SW|4:1:2|` means `SW4, SW2`, `SW|1:4|` means `SW1, SW2, SW3, SW4`, `SW|1:5:2|` means `SW1, SW3, SW5`.(at left)
  
  if at right, then `in|0:3|` means `in[0], in[1], in[2], in[3]` and so on.

#### 3. python expression
  
  In `XX||python||`, `python` means a python expression, which should be passed to the `list()` constructor in python and return a list of integers.
  
  e.g. `SW||i for i in range(1, 6) if i % 2 == 0||` means `SW2, SW4`.

  Expanation: `list(i for i in range(1, 6) if i % 2 == 0)` is `[2, 4]`.

#### 4. syntax sugar
Now we support 3 syntax sugars:
- `seg7` will be expanded to `CA, CB, CC, CD, CE, CF, CG, DP`.
- `clk` will be expanded to `CLK100`.
- `seg7en` will be expanded to `AN0, AN1, AN2, AN3, AN4, AN5, AN6, AN7`.

syntax sugar could only be used at left.

You should not add range expression or python expression to syntax sugar.

If you need to assign them seperately, you should write them seperately, like
`CA, CB, CC ~ out|0:2|`

---

See more examples at [/sample/demo.xg](https://github.com/Jackcuii/xdcGen/blob/main/sample/demo.xg)

Annotations are after `#`(like python).

Extra empty line is allowed.

#### Special Notice
- `~` is not allowed in the python expression, for it will cause parsing process to crash.
- Bonding a real pin to multiple module ports is UB. (actually it may not cause an error in **xdcGen**, but it will definitely cause a synthesis error.)  

## Appendix
now the *real pins* below is supported.
### Nexys A7-100T
- `SW0 - SW15` 16 switches
- `BC, BU, BD, BL, BR` 5 buttons (means button center, up, down, left, right)
- `LED0 - LED15` 16 LEDs
- `CA - CG, DP`  7seg display
- `AN0 - AN7` 8 anodes of 7seg display
- `LED16R, LED16G, LED16B, LED17R, LED17G, LED17B` 6 RGB LEDs
- `CLK100, RST` clock and reset
- `PS2CLK, PS2DAT` PS2 keyboard
