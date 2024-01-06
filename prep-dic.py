import sys

if len(sys.argv) != 3:
    print ("[ERR] Incorrect number of arguments.")
    print ("Usage: python3 script.py benchmark ISA")
    sys.exit(1)

benchmark = sys.argv[1]
benchmark = benchmark.strip().lower()
ISA = sys.argv[2]
ISA = ISA.strip().lower()

pc_file = f"../{ISA}-gem5/pc-address/{benchmark}.pc.txt"
inst_file = f"../{ISA}-gem5/outputs/dump-insts/{benchmark}.inst.txt"
dic_file = f"../{ISA}-gem5/outputs/{benchmark}.dic"

stack = []
dict = {}

with open(pc_file, 'r') as file:
    for line in file:
        words = line.strip().split()
        addr = words[0].strip()
        label = words[1].strip()
        func = words[2].strip()

        dict[addr] = (func, label)

# print (dict)

with open(inst_file, 'r') as file, open(dic_file, 'w') as dicfile:
    for line in file:
        words = line.strip().split()
        dic = words[0].strip()
        addr = words[1].strip()

        label = dict[addr][1]

        if label == "call":
            stack.append([dict[addr][0], int(dic)])
        elif label == "ret" and stack[-1][0] == dict[addr][0]:
            dic_count = int(dic) - stack[-1][1]
            print (f"{dict[addr][0]} {dic_count}", file=dicfile)
            stack.pop()

            for index, value in enumerate(stack):
                value[1] = value[1] + dic_count
        else:
            print ("[ERR] Top of stack does not match.")
            stack.pop()

