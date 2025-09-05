class GameLogic:

    def __init__(self, word_manager):
        self.word_manager = word_manager
        "把单词管理封装为一个类"
        self.target_word = ""
        "???????????"
        self.current_row = 0
        self.current_col = 0
        self.max_attempts = 6
        self.word_length = 5
        self.guesses = [["" for _ in range(self.word_length)] for _ in
                        range(self.max_attempts)]
        self.game_over = False
        self.win = False

    def new_game(self):
        """开始新游戏"""
        self.target_word = self.word_manager.get_random_word()
        self.current_row = 0
        self.current_col = 0
        self.guesses = [["" for _ in range(self.word_length)] for _ in
                        range(self.max_attempts)]
        self.game_over = False
        self.win = False
        return self.target_word

    def add_letter(self, letter):
        """添加字母到当前猜测位置"""
        if self.game_over or self.current_row >= self.max_attempts:
            return False

        if self.current_col < self.word_length:
            self.guesses[self.current_row][
                self.current_col] = letter.upper()
            self.current_col += 1
            return True
        return False

    def remove_letter(self):
        """从当前猜测位置移除字母"""
        if self.game_over or self.current_row >= self.max_attempts:
            return False

        if self.current_col > 0:
            self.current_col -= 1
            self.guesses[self.current_row][self.current_col] = ""
            return True
        return False

    def submit_guess(self):
        """提交当前行的猜测"""
        if self.game_over:
            return None

        if self.current_col != self.word_length:
            return False  # 单词未完成

        guess = "".join(self.guesses[self.current_row])

        if not self.word_manager.is_valid_word(guess):
            return None  # 无效单词

        # 检查游戏状态
        if guess == self.target_word:
            self.win = True
            self.game_over = True
        elif self.current_row == self.max_attempts - 1:
            self.game_over = True

        # 计算字母状态
        result = self.evaluate_guess(guess)

        self.current_row += 1
        self.current_col = 0

        return result

    def evaluate_guess(self, guess):
        """评估猜测结果，返回每个字母的状态"""
        result = []
        target_list = list(self.target_word)
        guess_list = list(guess)

        # 第一遍：检查正确位置（绿色）
        for i in range(self.word_length):
            if guess_list[i] == target_list[i]:
                result.append(2)  # 2表示正确位置
                target_list[i] = None  # 标记已匹配
                guess_list[i] = None  # 标记已处理
            else:
                result.append(0)  # 0表示暂时未知

        # 第二遍：检查错误位置（黄色）
        for i in range(self.word_length):
            if guess_list[i] is not None and guess_list[i] in target_list:
                result[i] = 1  # 1表示错误位置
                target_list[
                    target_list.index(guess_list[i])] = None  # 标记已匹配

        return result

    def get_game_state(self):
        """返回当前游戏状态"""
        return {
            "current_row": self.current_row,
            "current_col": self.current_col,
            "game_over": self.game_over,
            "win": self.win,
            "target_word": self.target_word if self.game_over else None
        }