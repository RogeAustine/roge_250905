import random


class WordManager:
    def __init__(self):
        # 常见5字母单词列表 (实际应用中可以从文件读取)
        self.word_list = [
            "APPLE", "BRAVE", "CLIMB", "DREAM", "EAGLE", "FLAIR", "GLASS",
            "HEART",
            "IGLOO", "JUMBO", "KNIFE", "LEMON", "MAGIC", "NIGHT", "OCEAN",
            "PIANO",
            "QUART", "RIVER", "SMILE", "TIGER", "ULTRA", "VIVID", "WATER",
            "XENON",
            "YACHT", "ZEBRA", "BEACH", "CANDY", "DANCE", "EMAIL", "FRUIT",
            "GHOST",
            "HOUSE", "IMAGE", "JAZZY", "KITTY", "LEARN", "MUSIC", "NEWLY",
            "OLIVE",
            "PEACH", "QUICK", "ROBIN", "SPACE", "TRAIN", "UNITY", "VOICE",
            "WORLD"
        ]

        # 有效猜测单词列表 (可以比答案列表更广泛)
        "这里实际上我想使用判断函数进行优化，列表不如直接复制一份"

        self.valid_guesses = self.word_list + [
            "ALPHA", "LOGIC", "GAMMA", "DELTA", "THETA", "KAPPA", "SIGMA",
            "OMEGA"
        ]

    def get_random_word(self):
        """从单词列表中随机选择一个单词作为答案"""
        return random.choice(self.word_list)

    def is_valid_word(self, word):
        """检查单词是否为有效猜测"""
        return word.upper() in self.valid_guesses