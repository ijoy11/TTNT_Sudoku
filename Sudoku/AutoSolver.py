
from SudokuValidator import SudokuValidator

class Solver: # Đặt class Solver ở đây hoặc import
    @staticmethod
    def find_empty(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    @staticmethod
    def solve(board):
        find = Solver.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if SudokuValidator.is_valid_move(board, row, col, num):
                board[row][col] = num
                if Solver.solve(board):
                    return True
                board[row][col] = 0 # Backtrack

        return False

class AutoSolver:
    @staticmethod
    def auto_fill(board):
        # Hàm này có thể giữ lại hoặc bỏ đi
        changed = True
        while changed:
            changed = False
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        possible_values = []
                        for value in range(1, 10):
                            if SudokuValidator.is_valid_move(board, row, col, value):
                                possible_values.append(value)
                        if len(possible_values) == 1:
                            board[row][col] = possible_values[0]
                            changed = True
        return board

    @staticmethod
    def auto_solve(board): # *** SỬA Ở ĐÂY: Bỏ tham số solved_board ***
        """
        Tự động hoàn thành trò chơi bằng cách sử dụng thuật toán giải Backtracking.
        :param board: Bảng Sudoku hiện tại (danh sách 2D)
        :return: True nếu giải thành công, False nếu không
        """
        # (Tùy chọn) Có thể gọi auto_fill trước
        # AutoSolver.auto_fill(board)

        # Gọi thuật toán giải chính (Solver.solve)
        if Solver.solve(board):
            return True
        else:
            # Ít khi xảy ra nếu bảng ban đầu hợp lệ
            # Có thể thêm messagebox báo lỗi ở đây nếu muốn
            print("Bảng không có lời giải!") # Hoặc dùng messagebox
            return False

# --- END OF FILE AutoSolver.py ---