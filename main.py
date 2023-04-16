import random
import curses


class Game:
    def __init__(self):
        # Initialize the board
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # Add two random tiles to the board
        self.new_title()
        self.new_title()
        # Set game state to playing
        self.play = True
        # Score starts at 0
        self.score = 0

    def new_title(self):
        # Choose a random empty tile on the board
        # Find all emtpy tiles on board so we know where to add new tiles
        empty_tiles = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    empty_tiles.append((i, j))
        if len(empty_tiles) != 0:
            x, y = random.choice(empty_tiles)
            # Add a new tile (either 2 or 4)
            # Has a 1/10 chance of it being 4 and 9/10 chance of being a 2
            two_or_four = random.randint(1, 10)
            if (two_or_four == 1):
                self.board[x][y] = 4
            else:
                self.board[x][y] = 2

    def move(self, direction):
        if direction == "up":
            # for each column (j) in the top 3 rows (i), move the tile upwards if possible and merge with same value tile
            for j in range(4):
                for i in range(1, 4):
                    if self.board[i][j] != 0:
                        k = i
                        while k > 0 and self.board[k-1][j] == 0:
                            k -= 1
                        if k != i:
                            self.board[k][j] = self.board[i][j]
                            self.board[i][j] = 0
                        if k > 0 and self.board[k-1][j] == self.board[k][j]:
                            self.board[k-1][j] *= 2
                            self.board[k][j] = 0
        elif direction == "down":
            # for each column (j) in the bottom 3 rows (i), move the tile downwards if possible and merge with same value tile
            for j in range(4):
                for i in range(2, -1, -1):
                    if self.board[i][j] != 0:
                        k = i
                        while k < 3 and self.board[k+1][j] == 0:
                            k += 1
                        if k != i:
                            self.board[k][j] = self.board[i][j]
                            self.board[i][j] = 0
                        if k < 3 and self.board[k+1][j] == self.board[k][j]:
                            self.board[k+1][j] *= 2
                            self.board[k][j] = 0
        elif direction == "left":
            # for each row (i) in the left 3 columns (j), move the tile to the left if possible and merge with same value tile
            for i in range(4):
                for j in range(1, 4):
                    if self.board[i][j] != 0:
                        k = j
                        while k > 0 and self.board[i][k-1] == 0:
                            k -= 1
                        if k != j:
                            self.board[i][k] = self.board[i][j]
                            self.board[i][j] = 0
                        if k > 0 and self.board[i][k-1] == self.board[i][k]:
                            self.board[i][k-1] *= 2
                            self.board[i][k] = 0
        elif direction == "right":
            # for each row (i) in the right 3 columns (j), move the tile to the right if possible and merge with same value tile
            for i in range(4):
                for j in range(2, -1, -1):
                    if self.board[i][j] != 0:
                        k = j
                        while k < 3 and self.board[i][k+1] == 0:
                            k += 1
                        if k != j:
                            self.board[i][k] = self.board[i][j]
                            self.board[i][j] = 0
                        if k < 3 and self.board[i][k+1] == self.board[i][k]:
                            self.board[i][k+1] *= 2
                            self.board[i][k] = 0
        else:
            # if an invalid move is entered, print error message and return nothing
            print("Error: Invalid move")
            return
        # Add a new tile at the end of the turn
        self.new_title()
        # Updates score
        self.get_score()
        self.play = self.is_game_over()

    def is_game_over(self):
        # Check if there are any empty tiles left
        for row in self.board:
            if 0 in row:
                return False
        # Check if there are any adjacent tiles with the same value
        for i in range(4):
            for j in range(4):
                if j < 3 and self.board[i][j] == self.board[i][j+1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i+1][j]:
                    return False
        # No more moves available
        return True

    def print_board(self):
        for row in self.board:
            print(row)

    def get_score(self):
        score = 0
        # Goes through each index to get the value and adds it up for the total score
        for i in self.board:
            for j in i:
                score += j
        # Updates Score
        self.score = score


'''def main():
    game = Game()
    print("Starting game\nGood Luck\n\n")
    while not game.is_game_over():
        game.print_board()
        # user = random.choice(["up", "down", "left", "right"])
        user = input(f"Score = {game.score}\nEnter (Up,Down,Left,Right) :")
        game.move(user)
    print("Your final score was ", game.score)'''


def main():
    game = Game()
    print("Starting game\nGood Luck\n\n")
    while not game.is_game_over():
        # game.print_board()
        user_input = curses.initscr()
        user_input.keypad(True)
        curses.noecho()
        curses.cbreak()
        user = None
        while user not in ["up", "down", "left", "right"]:
            user_input.clear()
            user_input.addstr(
                f"{game.board[0]}\n{game.board[1]}\n{game.board[2]}\n{game.board[3]}\nScore = {game.score}\nEnter (Up,Down,Left,Right) :")
            key = user_input.getch()
            if key == curses.KEY_UP:
                user = "up"
            elif key == curses.KEY_DOWN:
                user = "down"
            elif key == curses.KEY_LEFT:
                user = "left"
            elif key == curses.KEY_RIGHT:
                user = "right"
        curses.endwin()
        game.move(user)
    print("Your final score was ", game.score)


if __name__ == '__main__':
    main()
