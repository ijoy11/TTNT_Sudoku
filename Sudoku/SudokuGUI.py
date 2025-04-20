import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from GameLogic import GameLogic  # Import lớp xử lý logic trò chơi
from HintGenerator import HintGenerator  # Import lớp tạo gợi ý
from SudokuValidator import SudokuValidator  # Import lớp kiểm tra Sudoku
from AutoSolver import AutoSolver, Solver  # Import lớp giải Sudoku tự động


class SudokuGUI:
    def __init__(self, root, difficulty):
        self.root = root
        self.root.title("Sudoku")
        self.difficulty = difficulty  # Lưu mức độ khó
        self.board = self.generate_board()  # Tạo bảng Sudoku tự động
        self.original_board = [row[:] for row in self.board]  # Lưu bảng gốc để cố định các số ban đầu
        self.cell_size = 60
        self.notes = [[set() for _ in range(9)] for _ in range(9)]  # Lưu ghi chú cho từng ô
        self.canvas = tk.Canvas(root, width=9 * self.cell_size, height=9 * self.cell_size)
        self.canvas.pack()

        # Tạo frame để chứa các nút
        button_frame = tk.Frame(root)
        button_frame.pack()

        # Thêm nút "Tự động hoàn thành"
        self.auto_solve_button = tk.Button(button_frame, text="Tự động hoàn thành", command=self.auto_solve)
        self.auto_solve_button.pack(side=tk.LEFT, padx=5)

        # Thêm nút "Gợi ý"
        self.hint_button = tk.Button(button_frame, text="Gợi ý", command=self.show_hint)
        self.hint_button.pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.on_click)  # Thêm sự kiện click chuột
        self.wrong_attempts = 0  # Biến đếm số lần nhập sai
        self.draw_board()

    def show_hint(self):
        """
        Hiển thị gợi ý cho người chơi bằng cách sử dụng HintGenerator.
        """
        hint = HintGenerator.get_hint(self.board)
        if hint:
            row, col, value = hint
            self.board[row][col] = value  # Điền giá trị gợi ý vào bảng
            self.draw_board()  # Vẽ lại bảng sau khi điền gợi ý
            messagebox.showinfo("Gợi ý", f"Gợi ý: Ô ({row + 1}, {col + 1}) nên điền số {value}.")
        else:
            messagebox.showinfo("Gợi ý", "Không còn ô trống để gợi ý!")
        
    def auto_solve(self):
        """
        Tự động hoàn thành trò chơi bằng cách sử dụng AutoSolver.
        """
        success = AutoSolver.auto_solve(self.board)
        if success:
            self.draw_board() # Vẽ lại bảng sau khi hoàn thành
            messagebox.showinfo("YOU WIN", "Chúc mừng! Bạn đã hoàn thành Sudoku!")

    def generate_board(self):
        """
        Tạo bảng Sudoku hợp lệ và xóa một số ô để tạo thử thách.
        """
        base = 3
        side = base * base

        # Mẫu hàng và cột
        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        # Xáo trộn hàng, cột và số
        def shuffle(s): return random.sample(s, len(s))

        rows = [g * base + r for g in shuffle(range(base)) for r in shuffle(range(base))]
        cols = [g * base + c for g in shuffle(range(base)) for c in shuffle(range(base))]
        nums = shuffle(range(1, side + 1))

        # Tạo bảng Sudoku đầy đủ
        solved_board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Lưu bảng hoàn chỉnh
        # self.solved_board = [row[:] for row in solved_board]

        # Xóa một số ô để tạo bảng Sudoku chưa hoàn chỉnh
        squares = side * side
        if self.difficulty == "easy":
            empties = squares * 7 // 10  # Xóa 25% số ô
        elif self.difficulty == "medium":
            empties = squares * 8 // 10  # Xóa 50% số ô
        elif self.difficulty == "hard":
            empties = squares * 9 // 10  # Xóa 75% số ô
        else:
            empties = squares * 8 // 10  # Mặc định là trung bình

        for _ in range(empties):
            x, y = random.randint(0, side - 1), random.randint(0, side - 1)
            solved_board[x][y] = 0

        return solved_board

    def draw_board(self):
        """
        Vẽ lại bảng Sudoku trên canvas.
        """
        self.canvas.delete("all")  # Xóa canvas trước khi vẽ lại
        for i in range(9):
            for j in range(9):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Kiểm tra nếu ô trống thì tô màu trắng, nếu không thì tô màu xám (cố định)
                fill_color = "white" if self.original_board[i][j] == 0 else "lightgray"
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=fill_color)

                # Vẽ số trong ô nếu có
                if self.board[i][j] != 0:
                    text_x = (x1 + x2) // 2
                    text_y = (y1 + y2) // 2
                    self.canvas.create_text(text_x, text_y, text=str(self.board[i][j]), font=("Arial", 20))
                elif self.notes[i][j]:
                    # Hiển thị ghi chú nếu có
                    note_text = " ".join(map(str, sorted(self.notes[i][j])))
                    text_x = (x1 + x2) // 2
                    text_y = (y1 + y2) // 2
                    self.canvas.create_text(text_x, text_y, text=note_text, font=("Arial", 10), fill="gray")

    def on_click(self, event):
        """
        Xử lý sự kiện khi người chơi nhấp vào một ô.
        """
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Kiểm tra nếu click vào trong bảng và ô không phải là ô cố định
        if 0 <= row < 9 and 0 <= col < 9 and self.original_board[row][col] == 0:
            # Hiển thị hộp thoại để chọn chế độ
            mode = simpledialog.askstring("Chế độ", "Nhập 'f' để ghi chú hoặc 'r' để nhập số:")
            if mode == "f":
                # Ghi chú: Cho phép người chơi nhập các số có thể là đáp án
                note_value = simpledialog.askinteger("Ghi chú", "Nhập số (1-9):", minvalue=1, maxvalue=9)
                if note_value is not None:
                    if note_value in self.notes[row][col]:
                        self.notes[row][col].remove(note_value)  # Xóa ghi chú nếu đã tồn tại
                    else:
                        self.notes[row][col].add(note_value)  # Thêm ghi chú
                    self.draw_board()  # Vẽ lại bảng với ghi chú
            elif mode == "r":
                # Nhập số chính thức
                value = simpledialog.askinteger("Nhập giá trị", "Nhập số (1-9):", minvalue=1, maxvalue=9)
                if value is not None:  # Nếu người dùng nhập giá trị
                    is_valid = SudokuValidator.is_valid_move(self.board, row, col, value)
                    if is_valid:
                        # Nếu giá trị khớp với số đúng, cập nhật bảng và vẽ lại
                        self.board[row][col] = value
                        self.notes[row][col].clear()  # Xóa ghi chú khi nhập số chính thức
                        self.draw_board()  # Vẽ lại bảng với giá trị mới
                        
# KIỂM TRA THẮNG: Kiểm tra xem còn ô trống không
                        if Solver.find_empty(self.board) is None: # <--- SỬA Ở ĐÂY
                            GameLogic.handle_win(self.root) # Gọi hàm xử lý thắng từ GameLogic
                            # messagebox.showinfo("YOU WIN", "Chúc mừng! Bạn đã hoàn thành Sudoku!")
                            # self.root.destroy() # handle_win đã làm việc này

                    else:
                        # Nếu không hợp lệ, tô đỏ và xử lý sai                                
                        x1 = col * self.cell_size
                        y1 = row * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        # Vẽ lại ô với màu nền trắng trước khi tô đỏ để không bị đè màu cũ
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                        # Tô đỏ và hiển thị số sai
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="red")
                        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(value), font=("Arial", 20), fill="white")
                        
                        self.wrong_attempts += 1  # Tăng số lần nhập sai
                        if self.wrong_attempts >= 3:
                            GameLogic.handle_loss(self.root) # Gọi hàm xử lý thua từ GameLogic
                            # messagebox.showinfo("Thông báo", "Bạn đã nhập sai 3 lần. Trò chơi kết thúc!")
                            # self.root.destroy() # handle_loss đã làm việc này
