# /dsa/hw01/code/src/UniqueInt.py

import time

class UniqueInt:
    @staticmethod
    def processFile(inputFilePath, outputFilePath):
        start_time = time.time()

        unique_map = [False] * 2047  # index from -1023 to 1023 → 0 to 2046
        seen = []

        with open(inputFilePath, 'r') as infile:
            for line in infile:
                value = UniqueInt.readNextItemFromLine(line)
                if value is not None:
                    index = value + 1023
                    if not unique_map[index]:
                        unique_map[index] = True
                        seen.append(value)

        # Manual bubble sort (no built-in sort allowed)
        for i in range(len(seen)):
            for j in range(0, len(seen)-i-1):
                if seen[j] > seen[j+1]:
                    seen[j], seen[j+1] = seen[j+1], seen[j]

        with open(outputFilePath, 'w') as outfile:
            for number in seen:
                outfile.write(f"{number}\n")

        end_time = time.time()
        print(f"Processed {inputFilePath}")
        print(f"Runtime: {round((end_time - start_time) * 1000)} ms")
        print(f"Memory used: {len(seen) * 4} bytes (assuming 4 bytes per integer)")

    @staticmethod
    def readNextItemFromLine(line):
        line = line.strip()
        if line.startswith("(") and line.endswith(")"):
            parts = line[1:-1].split(',')
            if len(parts) == 3:
                try:
                    return int(parts[2].strip())
                except ValueError:
                    return None
        return None

if __name__ == "__main__":
    UniqueInt.processFile(
        "../../sample_inputs/sample_input_01.txt",
        "../../sample_results/sample_input_01.txt_results.txt"
    )
