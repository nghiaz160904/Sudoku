from pysat.solvers import Glucose3
from pysat.formula import CNF

class Map:
    def __init__(self, rows, cols, data):
        self.rows = rows
        self.cols = cols
        self.data = data


def sudoku_cnf(map_data):
    clauses = CNF()

    # Add clauses for each cell
    for i in range(1, map_data.rows + 1):
        for j in range(1, map_data.cols + 1):
            if map_data.data[i-1][j-1] != 0:  # If the cell already has a number
                k = map_data.data[i-1][j-1]
                # Add a clause to enforce that only this number is allowed in this cell
                clauses.append([i * 100 + j * 10 + k])
            else:
                # At least one number in each cell
                max_num = min(map_data.rows, map_data.cols)
                clause = [i * 100 + j * 10 + k for k in range(1, max_num + 1)]
                clauses.append(clause)

                # At most one number in each cell
                for k in range(1, max_num + 1):
                    for m in range(k + 1, max_num + 1):
                        clauses.append([- (i * 100 + j * 10 + k), - (i * 100 + j * 10 + m)])

    # Add clauses for each row
    for i in range(1, map_data.rows + 1):
        for k in range(1, map_data.rows + 1):
            # At least one occurrence of k in each row
            clause = [i * 100 + j * 10 + k for j in range(1, map_data.cols + 1)]
            clauses.append(clause)

            # At most one occurrence of k in each row
            for j in range(1, map_data.cols + 1):
                for m in range(j + 1, map_data.cols + 1):
                    clauses.append([- (i * 100 + j * 10 + k), - (i * 100 + m * 10 + k)])

    # Add clauses for each column
    for j in range(1, map_data.cols + 1):
        for k in range(1, map_data.cols + 1):
            # At least one occurrence of k in each column
            clause = [i * 100 + j * 10 + k for i in range(1, map_data.rows + 1)]
            clauses.append(clause)

            # At most one occurrence of k in each column
            for i in range(1, map_data.rows + 1):
                for m in range(i + 1, map_data.rows + 1):
                    clauses.append([- (i * 100 + j * 10 + k), - (m * 100 + j * 10 + k)])

    # Add clauses for each subgrid
    subgrid_size = int(map_data.rows ** 0.5)
    for r in range(0, map_data.rows, subgrid_size):
        for c in range(0, map_data.cols, subgrid_size):
            for k in range(1, map_data.rows + 1):
                # At least one occurrence of k in each subgrid
                clause = [i * 100 + j * 10 + k for i in range(1 + r, 1 + r + subgrid_size) for j in range(1 + c, 1 + c + subgrid_size)]
                clauses.append(clause)

                # At most one occurrence of k in each subgrid
                for i in range(1 + r, 1 + r + subgrid_size):
                    for j in range(1 + c, 1 + c + subgrid_size):
                        for m in range(i, 1 + r + subgrid_size):
                            for n in range(j + 1, 1 + c + subgrid_size):
                                clauses.append([- (i * 100 + j * 10 + k), - (m * 100 + n * 10 + k)])

    return clauses

def solve_sudoku(map_data):
    # Generate Sudoku CNF
    cnf = sudoku_cnf(map_data)

    # Initialize Glucose3 solver
    solver = Glucose3()

    # Add CNF to the solver
    for clause in cnf.clauses:
        solver.add_clause(clause)

    # Solve the SAT problem
    if solver.solve():
        # Get the model (assignment of variables)
        model = solver.get_model()

        # Extract the numbers from the model
        solution = [[0 for _ in range(map_data.cols)] for _ in range(map_data.rows)]
        for literal in model:
            if literal > 0:
                literal_str = str(literal)
                row = int(literal_str[:-2]) - 1
                col = int(literal_str[-2]) - 1
                num = int(literal_str[-1])
                solution[row][col] = num

        return solution
    else:
        return None

# Example usage
map_data = Map(4, 4, [
    [1, 0, 3, 4],
    [3, 4, 0, 2],
    [4, 0, 2, 0],
    [0, 3, 0, 1]
])


solution = solve_sudoku(map_data)
if solution:
    print("Sudoku Solution:")
    for row in solution:
        print(row)
else:
    print("No solution found.")