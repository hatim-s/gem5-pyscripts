"""
Author: Hatim

Reads function names from benchmark's function-name file and extracts PC
addresses for specified ISA.
"""

import sys

if len(sys.argv) != 3:
    print("Usage: python3 script.py benchmark isa")
    print ("[ERR] Invalid usage. Refer the usage guidelines.")
    sys.exit(1)

benchmark = sys.argv[1].strip().lower()
isa = sys.argv[2].strip().lower()

functions = []

function_file = f"../specfunc/{benchmark}.func.names"

try:
    with open(function_file, 'r') as file:
        for line in file:
            line = line.strip()
            functions.append(line.strip())

except FileNotFoundError:
    print (f"[Err] {function_file} not found.\n")
except Exception as E:
    print (f"[Err] Unexpected error occurred: {E}\n")

source_file = f"../specbin/source/{benchmark}.{isa}.txt"
equi_points = []

try:
    with open(source_file, 'r') as file:
        last_function = None
        flag = False
        for line in file:
            line = line.strip()

            if (
                line == "Disassembly of section .text:" or
                line == " Disassembly of section .fini:"
            ):
                flag = True
                continue

            if flag == False:
                continue

            words = line.split()

            if len(words) == 2 and words[-1][-1] == ":":
                if words[1][1:-2] in functions:
                    last_function = words[1][1:-2]

                    pc_address = words[0]
                    label = "call"

                    if isa == "x86":
                        equi_points.append({
                            "pc_address": "{:0>16}".format(pc_address)[-16:],
                            "label": label,
                            "function_name": last_function
                        })
                    else: # isa == "arm"
                        equi_points.append({
                            "pc_address": "{:0>8}".format(pc_address)[-8:],
                            "label": label,
                            "function_name": last_function
                        })
                else:
                    last_function = None

            elif "ret" in words and last_function != None:
                pc_address = None

                if isa == "x86":
                    pc_address = "{:0>16}".format(words[0][:-1])
                else: # isa == "arm"
                    pc_address = "{:0>8}".format(words[0][:-1])

                label = "ret "

                equi_points.append({
                    "pc_address": pc_address,
                    "label": label,
                    "function_name": last_function
                })

except FileNotFoundError:
    print (f"[Err] {source_file} not found.")
except Exception as E:
    print (f"[Err] Unexpected error occurred: {E}")

output_file_path = f"../{isa}-gem5/pc-address/{benchmark}.pc.txt"
with open(output_file_path, "w") as file:
    for point in equi_points:
        for key, value in point.items():
            print (value, file=file, end=' ')
        print (file=file)
