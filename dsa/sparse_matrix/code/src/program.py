#!/usr/bin/python3

class SparseMatrix:
    def __init__(self, filepath=None, rows=0, cols=0):
        self.matrix = {}
        self.rows = rows
        self.cols = cols
        if filepath:
            self._load(filepath)

    def _load(self, filename):
        with open(filename, 'r') as f:
            try:
                self.rows = int(f.readline().split('=')[1])
                self.cols = int(f.readline().split('=')[1])
                for line in f:
                    if line.strip():
                        line = line.strip()
                        if not (line.startswith('(') and line.endswith(')')):
                            raise ValueError("Input file has wrong format")
                        parts = line[1:-1].split(',')
                        if len(parts) != 3:
                            raise ValueError("Input file has wrong format")
                        r, c, v = map(int, parts)
                        self.set(r, c, v)
            except:
                raise ValueError("Input file has wrong format")

    def get(self, r, c):
        return self.matrix.get(r, {}).get(c, 0)

    def set(self, r, c, v):
        if v != 0:
            if r not in self.matrix:
                self.matrix[r] = {}
            self.matrix[r][c] = v

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(f"rows={self.rows}\ncols={self.cols}\n")
            for r in self.matrix:
                for c in self.matrix[r]:
                    f.write(f"({r}, {c}, {self.matrix[r][c]})\n")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for r in set(self.matrix) | set(other.matrix):
            for c in set(self.matrix.get(r, {})) | set(other.matrix.get(r, {})):
                val = self.get(r, c) + other.get(r, c)
                result.set(r, c, val)
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for r in set(self.matrix) | set(other.matrix):
            for c in set(self.matrix.get(r, {})) | set(other.matrix.get(r, {})):
                val = self.get(r, c) - other.get(r, c)
                result.set(r, c, val)
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Invalid dimensions for multiplication.")
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        for i in self.matrix:
            for k in self.matrix[i]:
                if k in other.matrix:
                    for j in other.matrix[k]:
                        val = self.get(i, k) * other.get(k, j)
                        result.set(i, j, result.get(i, j) + val)
        return result

def main():
    f1 = input("Enter first matrix file path: ")
    f2 = input("Enter second matrix file path: ")
    operation = input("Choose operation (add, subtract, multiply): ").strip().lower()
    output_file = input("Enter output file name: ")

    m1 = SparseMatrix(f1)
    m2 = SparseMatrix(f2)

    if operation == "add":
        result = m1.add(m2)
    elif operation == "subtract":
        result = m1.subtract(m2)
    elif operation == "multiply":
        result = m1.multiply(m2)
    else:
        print("Invalid operation.")
        return

    result.save(output_file)
    print(f"Result saved to {output_file}")


if __name__ == "__main__":
    main()