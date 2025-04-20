class SudokuValidator:
    @staticmethod
    def is_valid_move(board, row, col, value):
        """
        Kiểm tra xem giá trị nhập vào có hợp lệ không.
        :param board: Bảng Sudoku (danh sách 2D)
        :param row: Hàng của ô
        :param col: Cột của ô
        :param value: Giá trị cần kiểm tra
        :return: True nếu hợp lệ, False nếu không
        """
        # Kiểm tra hàng
        if value in board[row]:
            return False

        # Kiểm tra cột
        if value in [board[i][col] for i in range(9)]:
            return False

        # Kiểm tra ô 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == value:
                    return False

        return True