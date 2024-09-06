import argparse
import os
from xdcLib import *
import datetime

deviceCls = None

def strip_blank(line):
    return line.strip()

def parse_sugar(pins):
    ret = []
    #print(deviceCls)
    for pin in pins:
        if pin == "clk":
            ret += deviceCls.ClockMap()
        elif pin == "seg7":
            ret += deviceCls.Seg7Map()
        elif pin == "seg7en":
            ret += deviceCls.Seg7EnMap()
        else:
            ret.append(pin)
    return ret

def parse_expression(exp, isLeft): # an express mean a single or aggregated name of pins
    if not '|' in exp:
        # simple exp
        return [strip_blank(exp)]
    else:
        # complex exp
        # find the first | and the last | in the exp
        first_idx = exp.find("||")
        last_idx = exp.rfind("||")
        if first_idx == -1 or last_idx == -1: # actually, should be both or none
            # not Python expression
            first_idx, last_idx = exp.find('|'), exp.rfind('|')
            if last_idx - first_idx <= 1:
                print(f"Invalid expression: {exp}")
                return None
            exp = exp.split('|')
            name, rest = exp[0], exp[1]
            name = strip_blank(name)
            rest = rest.split(':')
            if len(rest) > 3 or len(rest) < 2:
                print(f"Invalid expression: {exp}")
                return None
            elif len(rest) == 3:
                start, end, step = rest[0], rest[1], rest[2]
                try:
                    start, end, step = int(start), int(end), int(step)
                except ValueError:
                    print(f"Invalid expression: {exp}")
                    return None
            elif len(rest) == 2:
                start, end = rest[0], rest[1]
                try:
                    start, end = int(start), int(end)
                except ValueError:
                    print(f"Invalid expression: {exp}")
                    return None
                step = 1
            if start > end:
                step = -step
            i = start
            ret = []
            while i >= start and i <= end:
                if isLeft:
                    ret.append(f"{name}{i}")
                else:
                    ret.append(f"{name}[{i}]")
                i += step
            return ret
        else:
            # Python expression
            if last_idx - first_idx <= 2:
                print(f"Invalid expression: {exp}")
                return None
            name, rest = exp[:first_idx], exp[first_idx+2:last_idx]
            try:
                rest = eval("list(" + rest + ")")
            except:
                print(f"Invalid expression: {exp}")
                return None
            ret = []
            for i in rest:
                if isLeft:
                    ret.append(f"{name}{i}")
                else:
                    ret.append(f"{name}[{i}]")
            return ret
    # should not be here

def parse_script_line(line):
    # find index of '~' in the line
    idx = line.find('~')
    if idx == -1:
        return False
    #split the line into two parts
    left, right = line[:idx], line[idx+1:]
    left_items = left.split(';')
    left_pins = []
    parsed = None
    for item in left_items:
        item = item.strip()
        if not item:
            continue
        parsed = parse_expression(item, True)
        if parsed:
            left_pins += parsed
        else:
            return False
    right_items = right.split(';')
    right_pins = []
    for item in right_items:
        item = item.strip()
        if not item:
            continue
        parsed = parse_expression(item, False)
        if parsed:
            right_pins += parsed
        else:
            return False
    left_pins = parse_sugar(left_pins)
    if len(left_pins) != len(right_pins):
        print(f"LHS and RHS have different sum of pins.")
        return False
    print(f"Left pins: {left_pins}")
    print(f"Right pins: {right_pins}")
    return left_pins, right_pins

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str)
    parser.add_argument('-n', type=str)
    parser.add_argument('-o', type=str)
    args = parser.parse_args()

    try:
        with open(args.file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File {args.file_path} not found.")
        return
    
    device = "Artix-7 100T"
    if args.n:
        device = args.n
    
    global deviceCls
    for cls in FPGAdevice.__subclasses__():
        if cls.name == device:
            deviceCls = cls
            break
    if not deviceCls:
        print(f"Device {device} not supported")
        print(f"Please check https://github.com/Jackcuii/xdcGenerator for latest version.")
        print(f"BTW, Your generous contribution is appreciated, too.")
        return
    
    print(f"Generating XDC file for {device}")
    #print(f"{deviceCls}")
    # split the content by lines
    content = content.split('\n')
    # parse each line
    output = ""
    for i in range(len(content)):
        line = content[i]
        if not strip_blank(line):
            continue
        parsed = parse_script_line(line)
        if not parsed:
            print(f"ERROR raised at line {i+1}")
            return
        left_pins, right_pins = parsed
        for j in range(len(left_pins)):
            output += f"{deviceCls.lookup(left_pins[j]).getStr(right_pins[j])}\n"
    # by default write to file named date and time
    output_path = args.o if args.o else os.path.join(os.getcwd(), f"xdcGen_{device}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xdc")
    with open(output_path, 'w') as output_file:
        output_file.write(output)
    print(f"XDC file generated at {output_path}")

if __name__ == "__main__":
    main()