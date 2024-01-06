# Author : Arif/Hatim
# Used to remove duplicates from inst-count.txt files

import sys

def remove_duplicate_lines(input_file_path):
    prev_line = None

    output_file = f"../{ISA}-gem5/outputs/dump-insts/{benchmark}.inst.txt"
    with open(input_file_path, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            current_line = line.strip()

            if current_line != prev_line:
                outfile.write(line)
                prev_line = current_line

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py benchmark")
        sys.exit(1)

    benchmark = sys.argv[1]
    benchmark = benchmark.strip().lower()

    ISA = sys.argv[2]
    ISA = ISA.strip().lower()

    input_file_path = f"../{ISA}-gem5/outputs/inst-count.txt"
    remove_duplicate_lines(input_file_path)
