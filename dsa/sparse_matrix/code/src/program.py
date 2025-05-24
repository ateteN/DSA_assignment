#!/usr/bin/python3
class sparse_matrix:
    def __init__(self, filepath=None, rows=0, cols=0):
        self.matrix = {}
        self.rows = rows
        self.cols = cols
        if filepath:
            self.load_file(filepath)
# Load matrix from the text file 
    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.rows = int(file.readline().split('=')[1])
                self.cols = int(file.readline().split('=')[1])
                for line in file:
                    line = line.strip()
                    if line and line.startswith('(') and line.endswith(')'):
                        row, col, value = map(int, line[1:-1].split(','))
                        self.set_value(row, col, value)
                    else:
                        raise ValueError
        except:
            print("couldn't find the file.")
            exit()

    def get_value(self, row, col):
        return self.matrix.get(row, {}).get(col, 0)

    def set_value(self, row, col, value):
        if value != 0:
            if row not in self.matrix:
                self.matrix[row] = {}
            self.matrix[row][col] = value

    def save_file(self, filename):
        with open(filename, 'w') as f:
            f.write(f"rows={self.rows}\ncols={self.cols}\n")
            for row in self.matrix:
                for col in self.matrix[row]:
                    f.write(f"({row}, {col}, {self.matrix[row][col]})\n")
# Addition
    def addition(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Addition couldn't work because matrix dimensions must match.")
            exit()
        result = sparse_matrix(rows=self.rows, cols=self.cols)
        for row in set(self.matrix) | set(other.matrix):
            for col in set(self.matrix.get(row, {})) | set(other.matrix.get(row, {})):
                value = self.get_value(row, col) + other.get_value(row, col)
                result.set_value(row, col, value)
        return result
# Substraction
    def subtraction(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Failed. Matrix dimensions must match")
            exit()
        result = sparse_matrix(rows=self.rows, cols=self.cols)
        for row in set(self.matrix) | set(other.matrix):
            for col in set(self.matrix.get(row, {})) | set(other.matrix.get(row, {})):
                value = self.get_value(row, col) - other.get_value(row, col)
                result.set_value(row, col, value)
        return result
# Multiplication
    def multiply(self, other):
        if self.cols != other.rows:
            print("failed. Matrix dimensions must match")
            exit()
        result = sparse_matrix(rows=self.rows, cols=other.cols)
        for i in self.matrix:
            for k in self.matrix[i]:
                if k in other.matrix:
                    for j in other.matrix[k]:
                        val = self.get_value(i, k) * other.get_value(k, j)
                        result.set_value(i, j, result.get_value(i, j) + val)
        return result
# Run 
def main():
    try:
        f1 = input("Enter the file path for the first file: ")
        f2 = input("Enter the file path for the second file: ")
        operation = input("Choose operation (addition, subtract, multiply): ").strip().lower()
        output = input("what should the output file be named?: ")
        output_path = "../../sample_results/" + output

        m1 = sparse_matrix(f1)
        m2 = sparse_matrix(f2)

        if operation == "addition":
            result = m1.addition(m2)
        elif operation == "subtract":
            result = m1.subtraction(m2)
        elif operation == "multiply":
            result = m1.multiply(m2)
        else:
            print("Sorry, the operation you chose was not found")
            return

        result.save_file(output_path)
        print("Done! Saved to", output_path)

    except FileNotFoundError:
        print("files was not found")
    except Exception as e:
        print("Error, try again", e)

if __name__ == "__main__":
    main()