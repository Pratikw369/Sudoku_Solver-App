from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Function to check if a number can be placed in a given position
def is_safe(board, row, col, num):
    # Check the row
    if num in board[row]:
        return False
    # Check the column
    if num in board[:, col]:
        return False
    # Check the 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    if num in board[box_row_start:box_row_start + 3, box_col_start:box_col_start + 3]:
        return False
    return True

# Function to solve the Sudoku puzzle
def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Reset on backtrack

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the Sudoku grid from the form
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                cell_value = request.form.get(f'row{i}_{j}')  # Change to unique key for each cell
                row.append(int(cell_value) if cell_value else 0)  # Convert to int if not empty
            board.append(row)
        board = np.array(board)

        if solve_sudoku(board):
            solved = board.tolist()
        else:
            solved = None

        return render_template('index.html', solved=solved)

    return render_template('index.html', solved=None)

if __name__ == '__main__':
    app.run(debug=True)
