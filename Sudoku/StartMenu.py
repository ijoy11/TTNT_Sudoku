import tkinter as tk
from SudokuGUI import SudokuGUI  # Import giao diện trò chơi Sudoku

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.main_menu()

    def main_menu(self):
        """
        Hiển thị menu chính với nút "BẮT ĐẦU TRÒ CHƠI".
        """
        # Xóa tất cả các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Giao diện menu chính
        tk.Label(self.root, text="Chào mừng đến với Sudoku!", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="BẮT ĐẦU TRÒ CHƠI", font=("Arial", 16), command=self.show_difficulty_menu).pack(pady=10)
        tk.Button(self.root, text="Thoát", font=("Arial", 16), command=self.root.quit).pack(pady=10)

    def show_difficulty_menu(self):
        """
        Hiển thị menu chọn mức độ khó sau khi nhấn "BẮT ĐẦU TRÒ CHƠI".
        """
        # Xóa tất cả các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Giao diện chọn mức độ khó
        tk.Label(self.root, text="Chọn mức độ:", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Dễ", font=("Arial", 16), command=lambda: self.start_game("easy")).pack(pady=10)
        tk.Button(self.root, text="Trung bình", font=("Arial", 16), command=lambda: self.start_game("medium")).pack(pady=10)
        tk.Button(self.root, text="Khó", font=("Arial", 16), command=lambda: self.start_game("hard")).pack(pady=10)
        tk.Button(self.root, text="Quay lại", font=("Arial", 16), command=self.main_menu).pack(pady=10)

    def start_game(self, difficulty):
        """
        Chuyển sang giao diện trò chơi Sudoku với mức độ khó được chọn.
        """
        # Xóa tất cả các widget hiện tại
        for widget in self.root.winfo_children():
            widget.destroy()

        # Khởi tạo giao diện trò chơi Sudoku với mức độ khó
        SudokuGUI(self.root, difficulty)