# Jogo da Velha || TicTacToe Game
# by FELIPE MAION
# 21/02/2018
import os

class Player:
    def __init__(self, name: str, symbol: str, score=0):
        self.name = name
        self.symbol = symbol
        self.color = bcolors.OKBLUE if symbol == "X" else bcolors.OKGREEN# Define a color to each player

    def __str__(self):
        return "{} ('{}')".format(self.name, self.symbol)

class Grid:
    def __init__(self): # Create the board with the 9 spaces.
        self.grid = [" "] * 9

    def mark(self, player, position): # Draw the mark in the position, if available!
        if self.grid[position] == " ":
            self.grid[position] = player.color + player.symbol + bcolors.ENDC
            return True
        else:
            print(bcolors.BOLD + bcolors.FAIL + "\tPosição já ocupada!" + bcolors.ENDC)
            return False

    def draw(self):
        # 0   1   2
        # 3   4   5
        # 6   7   8
        print("0|1|2 \t\t {} | {} | {}".format(*self.grid[:3]))
        print("----- \t\t ----------")
        print("3|4|5 \t\t {} | {} | {}".format(*self.grid[3:6]))
        print("----- \t\t ----------")
        print("6|7|8 \t\t {} | {} | {}".format(*self.grid[6:9]))

    def check(self, win): # Check if the 3 positions has the same value, and not empty.
        if self.grid[win[0]] == self.grid[win[1]] and \
           self.grid[win[1]] == self.grid[win[2]] and\
           self.grid[win[0]] != " ":
            return True
        return False


class Game:
    def __init__(self, player1, player2, matches = 1):
        self.player1 = Player(player1, "X")
        self.player2 = Player(player2, "O")
        self.grid = Grid() # The board
        self.current_player, self.next_player = self.player1, self.player2# X starts, and next is to help swap players
        self.count_marks = 0 # Count number of marks
        self.matches = matches # How many matches will be played?
        self.current_match = 0 # Current match (games played).
        self.score = {self.player1:0, self.player2:0, 'VELHA':0}

    def play(self):
        while self.current_match != self.matches:
            winner = False
            while not winner:
                self.draw_game()
                print("\n{}, sua vez de jogar com o '{}'".format(self.current_player, self.current_player.symbol))
                self.get_position(self.current_player)
                self.draw_game()
                self.count_marks += 1
                if self.check_winner(self.grid): # Do we have a winner??
                    print("Fim da partida! - Ponto para {}".format(self.current_player))
                    self.score[self.current_player] += 1
                    winner = self.reset()
                else: # No player won, may be it is tied
                    if self.count_marks == 9:
                        print(bcolors.FAIL + "DEU VELHA!!" + bcolors.ENDC)
                        self.score['VELHA'] += 1
                        winner = self.reset()
                    else: # If not tied, change player and keep playing.
                        self.alternate_player()
        # End of all matches!!
        self.draw_scores()
        print(bcolors.WARNING + bcolors.BOLD + "\t\tFim de Jogo!!\n\n" + bcolors.ENDC)

    def draw_game(self):
        self.draw_scores()
        self.grid.draw()

    def draw_scores(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Não funciona no Pycharm.
        print("Placar: {}/{}".format(self.current_match,self.matches))
        for player, points in self.score.items():
            cor = player.color if player != 'VELHA' else bcolors.FAIL
            print( cor + str(points) + " pts :\t" + str(player) +  bcolors.ENDC)
        print("\n")

    def reset(self):
        self.grid = Grid()
        self.count_marks = 0
        self.current_match += 1
        input(bcolors.WARNING + "\nPressione ENTER para continuar, e atualizar placar." + bcolors.ENDC)
        return True

    def get_position(self, player):
        valid = False
        position = None
        while not valid:
            try: # Be nice and input a number or 'Q' otherwise you will be trapped.
                position = input("'Q' para finalizar\nPosição [0-8]:>> ")
                if position.upper() == 'Q':
                    os._exit(1) # Not sure how to end all loops... so... kill it!!!
                position = int(position)
                valid = True if self.grid.mark(player,position) else False
            except:
                print(bcolors.BOLD + bcolors.FAIL + "\tPosição inválida" + bcolors.ENDC)
                valid = False
        return position

    def check_winner(self, grid):
        all_wins = [[0,4,8], [2,4,6], [0,3,6], [1,4,7], [2,5,8],[0,1,2],[3,4,5],[6,7,8]]
        for win in all_wins:
            if grid.check(win):
                print("Parabéns {}, venceu com '{}'".format(self.current_player.name, self.current_player.symbol))
                return True
        return False

    def alternate_player(self): # swap players
        self.current_player, self.next_player = self.next_player, self.current_player

class bcolors: # let's make it more colorful!!!
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__": # Calling from shell: python tictactoe.py ??
    player1 = input("Nome do Jogador 1 (X) [Enter = Rafael]: ") or "Rafael"
    player2 = input("Nome do Jogador 2 (O) [Enter = Luiz]: ") or "Luiz"
    try:
        partidas = int(input("Número de partidas [Enter = 3]: "))
    except:
        partidas = 3
    tictactoe = Game(player1, player2, partidas)
    tictactoe.play()

