import numpy as np


PLAYERS = ("White", "Black")


class FourInRow:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.board = np.zeros((height, width), dtype=int)

        self.last_player = None  # 轮到的玩家 1: white, 2: black
        self.last_move = None  # (row, col)

        self.winner = None

    def get_legal_actions(self) -> list:
        actions = []
        for column in range(self.width):
            if self.board[-1][column] == 0:
                actions.append(column)
        return actions

    def apply_action(self, action: int) -> None:
        self.last_player = 1 if self.last_player != 1 else 2

        for row in range(self.height):
            if self.board[row][action] == 0:
                self.board[row][action] = self.last_player
                self.last_move = (row, action)
                return

    def is_terminal(self):
        return (self.get_winner() is not None) or (not self.get_legal_actions())  # 游戏结束条件：有玩家胜出或棋盘已满

    def get_winner(self):
        if self.winner is not None:
            return self.winner

        if self.is_move_win(self.last_move):
            self.winner = self.last_player
            return self.winner

        return None  # 若没有胜利者，返回None表示平局或游戏未结束
    
    def is_pos_win(self, r: int, c: int, debug=False) -> bool:
        if self.board[r][c] == 0:
            return False
        lines = []
        
        if c + 3 < self.width: 
            lines.append([self.board[r][c+i] for i in range(4)])
        if r + 3 < self.height:
            lines.append([self.board[r+i][c] for i in range(4)])
        if c + 3 < self.width and r + 3 < self.height:
            lines.append([self.board[r+i][c+i] for i in range(4)])
        if c - 3 >= 0 and r + 3 < self.height:
            lines.append([self.board[r+i][c-i] for i in range(4)])
        
        for line in lines:
            if 0 not in line and (1 not in line or 2 not in line):
                return True
        return False

    def is_move_win(self, move: (int, int)) -> bool:
        r, c = move
        player = self.board[r][c]
        print(f"checking move {move} by {player}")

        # 相对距离
        top = 3 if r + 3 <= self.height - 1 else self.height - 1 - r
        bottom = 3 if r - 3 >= 0 else r
        right = 3 if c + 3 <= self.width - 1 else self.width - 1 - c
        left = 3 if c - 3 >= 0 else c
        top_right = min(top, right)
        bottom_right = min(bottom, right)
        top_left = min(top, left)
        bottom_left = min(bottom, right)

        # 需要检查的点列（相对位置）
        lines = [[], [], [], []]

        lines[0] = [(x, 0) for x in range(-left, right+1)]
        lines[1] = [(0, y) for y in range(-bottom, top + 1)]
        lines[2] = [(i, i) for i in range(-bottom_left, top_right + 1)]
        lines[3] = [(-i, i) for i in range(-top_left, bottom_right + 1)]

        for line in lines:
            count = 0
            for point in line:
                if self.board[r + point[1]][c + point[0]] == player:
                    count += 1
                else:
                    count = 0
                if count >= 4:
                    return True

    def print_board(self) -> None:
        self._print_line()
        for r in range(self.height - 1, -1, -1):
            print(' ', end='')
            for c in range(self.width):
                if self.board[r][c] == 0:
                    print("  ", end='')
                elif self.board[r][c] == 1:
                    print("□ ", end='')
                elif self.board[r][c] == 2:
                    print("■ ", end='')
            print()
        self._print_line()

    def _print_line(self) -> None:
        line = ""
        for i in range(self.width):
            line += f"-{i + 1}"
        line += "-"
        print(line)


def test(game):
    while True:
        game.print_board()
        move = int(input())
        game.apply_action(move-1)
        if game.is_terminal():
            game.print_board()
            print(game.get_winner(), "Win!")
            break


if __name__ == "__main__":
    game = FourInRow(7, 5)
    test(game)






