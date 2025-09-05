from tkinter import Tk
from words import WordManager
from game_logic import GameLogic
from ui import WordleUI


def main():
    # 创建根窗口
    root = Tk()

    # 初始化游戏组件
    word_manager = WordManager()
    game_logic = GameLogic(word_manager)

    # 初始化用户界面
    app = WordleUI(root, game_logic)

    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    main()