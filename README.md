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
Each line is in the form of `[Left exp] ~ [Right exp]`
Left exp is the real pins on the 
Annotations are after `#`(like python).
Extra empty line is allowed.

Special Notice
- `~` is not allowed in the python expression, for it will cause parsing process to crash.
- Bonding a real pin to multiple module ports is UB. (actually it may not cause an error in **xdcGen**, but it will definitely cause a synthesis error.)  
