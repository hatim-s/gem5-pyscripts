import sys

if len(sys.argv) != 2:
    print ("[ERR] Incorrect number of arguments")
    print ("Usage: python3 script.py benchmark_name")
    sys.exit(1)

benchmark = sys.argv[1]
benchmark = benchmark.strip()

# print (benchmark, isa)

raw_file = f"../specfunc/{benchmark}.func.txt"
out_file = f"../specfunc/{benchmark}.func.names"

with open(raw_file, 'r') as rawf, open(out_file, 'w') as outf:
    for line in rawf:
        line = line.strip()
        if line == "":
            continue

        if line[-1] == ';':
            words = line.split()
            for word in words:
                if "(" in word:
                    word = word.split("(")
                    name = word[0].replace("*", "")
                    print (name, file=outf)
                    break


