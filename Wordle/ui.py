import tkinter as tk
from tkinter import messagebox


class WordleUI:
    def __init__(self, root, game_logic):
        self.root = root
        self.game = game_logic
        self.root.title("Wordle")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # 颜色定义
        self.colors = {
            "background": "#121213",
            "empty": "#3a3a3c",
            "wrong": "#3a3a3c",
            "present": "#b59f3b",
            "correct": "#538d4e",
            "text": "#ffffff",
            "key": "#818384"
        }

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg=self.colors["background"])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="WORDLE",
            font=("Arial", 36, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        title_label.pack(pady=20)

        # 游戏网格框架
        self.grid_frame = tk.Frame(main_frame,
                                   bg=self.colors["background"])
        self.grid_frame.pack(pady=20)

        # 创建游戏网格
        self.cells = []
        for row in range(6):
            cell_row = []
            for col in range(5):
                cell = tk.Label(
                    self.grid_frame,
                    text="",
                    width=2,
                    height=1,
                    font=("Arial", 24, "bold"),
                    fg=self.colors["text"],
                    bg=self.colors["empty"],
                    relief="raised",
                    borderwidth=2
                )
                cell.grid(row=row, column=col, padx=5, pady=5)
                cell_row.append(cell)
            self.cells.append(cell_row)

        # 键盘框架
        self.keyboard_frame = tk.Frame(main_frame,
                                       bg=self.colors["background"])
        self.keyboard_frame.pack(pady=20)

        # 创建键盘
        self.setup_keyboard()

        # 绑定键盘事件
        self.root.bind("<Key>", self.handle_key_press)

    def setup_keyboard(self):
        """设置虚拟键盘"""
        keyboard_layout = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        self.key_buttons = {}

        for row, keys in enumerate(keyboard_layout):
            key_row = tk.Frame(self.keyboard_frame,
                               bg=self.colors["background"])
            key_row.pack(pady=2)

            # 第一行添加Enter键
            if row == 0:
                enter_btn = tk.Button(
                    key_row,
                    text="Enter",
                    width=4,
                    height=2,
                    font=("Arial", 10, "bold"),
                    bg=self.colors["key"],
                    fg=self.colors["text"],
                    command=self.submit_guess
                )
                enter_btn.pack(side=tk.LEFT, padx=1)
                self.key_buttons["ENTER"] = enter_btn

            for key in keys:
                btn = tk.Button(
                    key_row,
                    text=key,
                    width=2,
                    height=2,
                    font=("Arial", 12, "bold"),
                    bg=self.colors["key"],
                    fg=self.colors["text"],
                    command=lambda k=key: self.add_letter(k)
                )
                btn.pack(side=tk.LEFT, padx=1)
                self.key_buttons[key] = btn

            # 最后一行添加Backspace键
            if row == 2:
                backspace_btn = tk.Button(
                    key_row,
                    text="⌫",
                    width=4,
                    height=2,
                    font=("Arial", 12, "bold"),
                    bg=self.colors["key"],
                    fg=self.colors["text"],
                    command=self.remove_letter
                )
                backspace_btn.pack(side=tk.LEFT, padx=1)
                self.key_buttons["BACKSPACE"] = backspace_btn

    def new_game(self):
        """开始新游戏"""
        self.game.new_game()
        self.update_display()

    def update_display(self):
        """更新界面显示"""
        # 更新网格
        for row in range(6):
            for col in range(5):
                letter = self.game.guesses[row][col]
                self.cells[row][col].config(text=letter)

        # 更新键盘颜色
        for key, button in self.key_buttons.items():
            if key not in ["ENTER", "BACKSPACE"]:
                button.config(bg=self.colors["key"])

    def add_letter(self, letter):
        """添加字母处理"""
        if self.game.add_letter(letter):
            row, col = self.game.current_row, self.game.current_col - 1
            self.cells[row][col].config(text=letter.upper())

    def remove_letter(self):
        """删除字母处理"""
        if self.game.remove_letter():
            row, col = self.game.current_row, self.game.current_col
            self.cells[row][col].config(text="")

    def submit_guess(self):
        """提交猜测处理"""
        result = self.game.submit_guess()

        if result is False:
            # 单词未完成
            self.shake_row(self.game.current_row)
            return
        elif result is None:
            # 无效单词
            messagebox.showinfo("无效单词",
                                "这不是一个有效的单词，请重新尝试。")
            return

        # 更新颜色
        self.update_row_colors(self.game.current_row - 1, result)
        self.update_keyboard_colors(
            self.game.guesses[self.game.current_row - 1], result)

        # 检查游戏是否结束
        state = self.game.get_game_state()
        if state["game_over"]:
            if state["win"]:
                messagebox.showinfo("恭喜",
                                    f"你赢了！答案是 {state['target_word']}")
            else:
                messagebox.showinfo("游戏结束",
                                    f"游戏结束！答案是 {state['target_word']}")

            # 询问是否开始新游戏
            if messagebox.askyesno("新游戏", "是否开始新游戏？"):
                self.new_game()

    def update_row_colors(self, row, result):
        """更新行颜色"""
        for col, status in enumerate(result):
            if status == 2:  # 正确位置
                color = self.colors["correct"]
            elif status == 1:  # 错误位置
                color = self.colors["present"]
            else:  # 不存在
                color = self.colors["wrong"]

            self.cells[row][col].config(bg=color)

    def update_keyboard_colors(self, guess, result):
        """更新键盘颜色"""
        for col, letter in enumerate(guess):
            key_btn = self.key_buttons[letter]
            current_bg = key_btn.cget("bg")

            # 只更新为更高级别的颜色状态（正确 > 存在 > 不存在）
            if result[col] == 2:  # 正确位置 - 最高优先级
                key_btn.config(bg=self.colors["correct"])
            elif result[col] == 1 and current_bg != self.colors[
                "correct"]:  # 错误位置
                key_btn.config(bg=self.colors["present"])
            elif result[col] == 0 and current_bg not in [
                self.colors["correct"], self.colors["present"]]:  # 不存在
                key_btn.config(bg=self.colors["wrong"])

    def shake_row(self, row):
        """抖动行动画（单词未完成时）"""
        for i in range(5):
            for col in range(5):
                self.cells[row][col].place(x=5 if i % 2 == 0 else -5)
            self.root.update()
            self.root.after(50)
        for col in range(5):
            self.cells[row][col].place(x=0)

    def handle_key_press(self, event):
        """处理键盘事件"""
        key = event.char.upper()

        if key.isalpha() and len(key) == 1:
            self.add_letter(key)
        elif event.keysym == "BackSpace":
            self.remove_letter()
        elif event.keysym == "Return":
            self.submit_guess()