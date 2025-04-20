# Trong file HintGenerator.py
import tkinter as tk
from tkinter import simpledialog, messagebox
# Giả sử bạn đặt Solver trong Solver.py
from AutoSolver import Solver
# Hoặc nếu đặt trong AutoSolver.py: from AutoSolver import Solver

class HintGenerator:
    @staticmethod
    def get_hint(board): # Bỏ tham số solved_board
        """
        Tìm một ô trống và trả về gợi ý giá trị đúng bằng cách giải bảng.
        :param board: Bảng Sudoku hiện tại (danh sách 2D)
        :return: Tuple (row, col, value) hoặc None nếu không có ô trống hoặc không giải được
        """
        # Tìm ô trống đầu tiên
        empty_cell = Solver.find_empty(board)
        if not empty_cell:
            return None # Không còn ô trống

        row, col = empty_cell

        # Tạo bản sao của bảng để chạy solver mà không ảnh hưởng bảng gốc
        board_copy = [r[:] for r in board]

        # Chạy thuật toán giải trên bản sao
        if Solver.solve(board_copy):
             # Nếu giải thành công, lấy giá trị tại ô trống đó từ bảng đã giải
            return row, col, board_copy[row][col]
        else:
            # Trường hợp này ít xảy ra nếu bảng ban đầu hợp lệ
            # nhưng có thể xảy ra nếu người dùng nhập sai trước đó
            messagebox.showerror("Lỗi", "Không thể tìm thấy lời giải từ trạng thái hiện tại!")
            return None