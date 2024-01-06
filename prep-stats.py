import sys
import csv

if len(sys.argv) != 3:
    print ("[ERR] Incorrect number of arguments")
    print ("Usage: python3 script.py benchmark ISA")
    sys.exit(1)

benchmark = sys.argv[1]
benchmark = benchmark.strip().lower()

ISA = sys.argv[2]
ISA = ISA.strip().lower()

stat_file = f"../{ISA}-gem5/m5out/o3/{benchmark}.stat.txt"
inst_file = f"../{ISA}-gem5/outputs/dump-insts/{benchmark}.inst.txt"
pcaddr_file = f"../{ISA}-gem5/pc-address/{benchmark}.pc.txt"
output_file = f"../{ISA}-gem5/m5out/o3/{benchmark}.csv"

functions = {}

with open(pcaddr_file, 'r') as addr_file:
    for line in addr_file:
        line = line.strip().split()

        addr = line[0]
        label = line[1]
        name = line[2]

        functions[addr] = (name, label)

with open(stat_file, 'r') as statf, open(inst_file, 'r') as instf, open(output_file, 'w') as outf:
    statline = statf.readline()
    stack = []
    csvwriter = csv.writer(outf)

    while True:
        statline = statf.readline()
        if not statline:
            break

        # 1. Extracting one set of stats
        stats = []
        while statline.strip() != "":
            if "Begin" in statline or "End" in statline:
                statline = statf.readline()
                continue

            statline = statline.strip().split()
            stat = int(statline[1]) if not '.' in statline[1] else float(statline[1])
            stats.append(stat)

            statline = statf.readline()
        # print (stats)

        # 2. Extracting corresponding inst
        instline = instf.readline()

        if not instline:
            break

        instline = instline.strip().split()

        # print (instline)

        inst_value = int(instline[0])
        addr = instline[1]

        # 3. Getting Function Details
        func_name = functions[addr][0]
        label = functions[addr][1]

        if label == "call":
            stack.append([func_name, stats])
        elif label == "ret" and stack[-1][0] == func_name:
            top = stack.pop()
            final_stats = [a-b for a, b in zip(stats, top[1])]

            row = [func_name]
            row.extend(final_stats[1:])
            csvwriter.writerow(row)

            for index, value in enumerate(stack):
                value[1] = [a+b for a, b in zip(value[1], final_stats)]
        else:
            print ("[ERR] Top of stack does not match.")
            stack.pop()
