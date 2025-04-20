import tkinter as tk


class GameLogic:
    @staticmethod
    def is_board_complete(board):
        """
        Kiểm tra xem bảng Sudoku đã được hoàn thành đúng hay chưa.
        :param board: Bảng Sudoku (danh sách 2D)
        :return: True nếu hoàn thành, False nếu không
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return False
        return True

    @staticmethod
    def handle_win(root):
        """
        Xử lý khi người chơi thắng trò chơi.
        :param root: Cửa sổ chính của ứng dụng
        """
        tk.messagebox.showinfo("YOU WIN", "Chúc mừng! Bạn đã hoàn thành Sudoku!")
        root.destroy()  # Đóng cửa sổ trò chơi

    @staticmethod
    def handle_loss(root):
        """
        Xử lý khi người chơi thua trò chơi.
        :param root: Cửa sổ chính của ứng dụng
        """
        tk.messagebox.showinfo("END GAME", "Bạn đã nhập sai 3 lần. Trò chơi kết thúc!")
        root.destroy()  # Đóng cửa sổ trò chơi