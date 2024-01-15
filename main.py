import random

from four_in_row import FourInRow


class Node:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state  # 游戏状态
        self.parent = parent  # 父节点
        self.children = []  # 子节点
        self.wins = 0  # 获胜次数
        self.visits = 0  # 访问次数
        self.untried_actions = self.game_state.get_legal_actions()  # 未尝试的动作


if __name__ == '__main__':
    tree = None

