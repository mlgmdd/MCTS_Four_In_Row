import random
import copy
import numpy as np

from four_in_row import FourInRow

PLAYERS = ("white", "black")


class Node:
    def __init__(self, game_state: FourInRow, player: int, parent=None, action="Root"):
        self.game_state = game_state  # 游戏状态
        self.parent = parent  # 父节点
        self.children = []  # 子节点
        self.wins = 0  # 获胜次数
        self.visits = 0  # 访问次数
        self.untried_actions = self.game_state.get_legal_actions()  # 未尝试的动作

        self.player = player

        self.c = 1.4

        self.depth = 0
        self.action = action

    def rollout(self) -> int:
        """单次随机结果"""
        current_game_state = copy.deepcopy(self.game_state)
        while not current_game_state.is_terminal():
            legal_moves = current_game_state.get_legal_actions()
            action = random.choice(legal_moves)
            current_game_state.apply_action(action)
        # if current_game_state.get_winner() == self.player:
        #     return 1  # 胜利
        # return 0  # 失败
        if current_game_state.winner is None:
            return 0
        return current_game_state.winner

    def select_child(self):
        """选择最佳子节点(UCT)"""
        best_child = None
        best_score = -1
        for child in self.children:
            uct_score = (child.wins / child.visits) + self.c * np.sqrt(np.log(self.visits) / child.visits)
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    def expand(self):
        """将所有未尝试的动作加入子节点"""
        action = random.choice(self.untried_actions)
        new_game_state = copy.deepcopy(self.game_state)
        new_game_state.apply_action(action)
        new_child = Node(new_game_state, player=self.player, parent=self, action=action)

        self.children.append(new_child)
        self.untried_actions.remove(action)

        return new_child

    def back_propagate(self, result, deep=0):
        # 回溯更新节点信息
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.back_propagate(result, deep+1)
        else:
            if deep > self.depth:
                self.depth = deep

    def is_fully_expended(self):
        return not self.untried_actions

    def __str__(self):
        return f"[{self.action}]({self.wins}/{self.visits})"


def print_tree(root, blanks=0):
    if root.visits <= 5:
        return
    print('   '*blanks+"├─", root)
    children = sorted(root.children, key=lambda x: x.visits, reverse=True)
    for child in children:
        print_tree(child, blanks=blanks+1)


class MCTSApp:
    def __init__(self, game, max_iterations):
        self.game = game

    @staticmethod
    def monte_carlo_tree_search(root_state: FourInRow, max_iterations: int):
        if root_state.is_terminal():
            return root_state

        root = Node(root_state, player=root_state.last_player)
        for i in range(max_iterations):
            node = root

            while node.is_fully_expended():
                node = node.select_child()
            if not node.game_state.is_terminal():
                node = node.expand()

            simulation_result = node.rollout()
            node.back_propagate(simulation_result)
            print(f"\rSteps:\t{i + 1}, Depth:\t{root.depth}", end='')
        print()

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.game_state

    def start(self):
        self.game.print_board()
        while True:
            action = input('Enter a move: ')
            if action == 'q':
                exit()
            is_input_legal = self.game.user_move(action)
            if is_input_legal:
                self.game.print_board()
                self.game = self.monte_carlo_tree_search(self.game, max_iterations=10000)
                self.game.print_board()

                if self.game.is_terminal():
                    print(PLAYERS[self.game.get_winner()], "Win!")
                    break



def monte_carlo_tree_search(root_state: FourInRow, max_iterations: int):
    if root_state.is_terminal():
        return root_state

    root = Node(root_state, player=root_state.last_player)
    for i in range(max_iterations):
        node = root

        while node.is_fully_expended():
            node = node.select_child()
        if not node.game_state.is_terminal():
            node = node.expand()

        simulation_result = node.rollout()
        node.back_propagate(simulation_result)
        print(f"\rSteps:\t{i+1}, Depth:\t{root.depth}", end='')
    print()

    # print_tree(root)

    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.game_state


def test(game):
    game.print_board()
    while True:
        move = int(input())
        game.apply_action(move-1)
        game.print_board()
        game = monte_carlo_tree_search(game, max_iterations=10000)
        game.print_board()
        if game.is_terminal():
            print(PLAYERS[game.get_winner()], "Win!")
            break


if __name__ == '__main__':
    four_in_row = FourInRow(7, 5)
    app = MCTSApp(four_in_row, max_iterations=10000)
    app.start()


