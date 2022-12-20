import numpy as np
import pickle


class State:
    def __init__(self, p1, p2):
        # creating a board and game over state
        # 3-d numpy array
        self.board = np.zeros((6, 7))
        # p1 and p2 are any Inputs
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        # hashing the board which is fast way to
        # search for a value
        self.boardHash = None
        # playerSymbol starts out at 1
        self.playerSymbol = 1

    def getHash(self):
      # this is the board tranposed and then the
      # array is returned as a string of the array
        return str(self.board.reshape(42))

    def findRowIndice(self, column):
        "given a column find the space that a piece can be dropped in"
        row = 0
        # we can reference self.board with some shorthand 'brd'

        brd = self.board
        # note that if row is returned as -1 that means the column is filled
        while row < 6:
            if brd[row][column] in [-1, 1]:
                row -= 1
                return row
            elif brd[row][column] == 0 and row == 5:
                return row
            elif brd[row][column] == 0:
                row += 1

    # available positions function

    def availablePositions(self):
        "find all available moves based on self.board"
        positions = []
        for column in range(7):
            row = self.findRowIndice(column)
            if row != -1:
                positions.append((row, column))
        return positions

    def updateState(self, row, col):  # a move is made
        self.board[row][col] = self.playerSymbol
        # change whose turn it is
        self.playerSymbol *= -1

    def checkHorizontal(self, row, col, player):
        "check if the player has won horizontally based on the position and the player"
        # we can reference self.board with some shorthand 'brd'
        brd = self.board

        # the position given is filled by the player
        if brd[row][col] == player:
            matches = 1
            index = col
            # this while loop handles checking the spaces to the left of the given position
            while index > 0:
                if brd[row][index-1] == player:
                    matches += 1
                    index -= 1
                else:
                    break
            index = col
            # this while loop handles checking the spaces to the right of the given position
            while index < 6:
                if brd[row][index+1] == player:
                    matches += 1
                    index += 1
                else:
                    break
            # if there were four or more matches horizontally then return True for the player has won
            if matches >= 4:
                return True
            else:
                return False

        # the position given isn't filled by the player
        else:
            return False

    def checkVertical(self, row, col, player):
        "check if the player has won vertically"
        # we can reference self.board with some shorthand 'brd'
        brd = self.board
        # the position given is filled by the player
        if brd[row][col] == player:
            matches = 1
            index = row
            # this while loop handles checking the spaces above the given position
            while index > 0:
                if brd[index-1][col] == player:
                    matches += 1
                    index -= 1
                else:
                    break
            index = row
            # this while loop handles checking the spaces below the given position
            while index < 5:
                if brd[index+1][col] == player:
                    matches += 1
                    index += 1
                else:
                    break
            # if the player has 4 or more matches than return True for the player has won
            if matches >= 4:
                return True
            else:
                return False
        else:
            return False

    def checkDiagnonal(self, row, col, player):
        "check if the player has won diagonally"
        # we can reference self.board with some shorthand 'brd'
        brd = self.board
        # check if the position given is filled by the player
        if brd[row][col] == player:
            # theres two 'matches' variables as a player can win diagonally in two ways
            # one way is a ray traveling from the bottom left direction to the top right direction ('upperRightMathces')
            # the other way is a ray traveling from the top left direction to the bottom right direction ('upperLeftMathces')
            upperRightMatches = 1
            upperLeftMatches = 1

            # ro and cl are copies of arguments that will be manipulated in while loop
            ro = row
            cl = col

            # these next two while loops are for checking 'upperRightMatches'
            while ro > 0 and cl < 6:
                if brd[ro-1][cl+1] == player:
                    upperRightMatches += 1
                    ro -= 1
                    cl += 1
                else:
                    break
            # reset ro and cl
            ro = row
            cl = col
            while ro < 5 and cl > 0:
                if brd[ro+1][cl-1] == player:
                    upperRightMatches += 1
                    ro += 1
                    cl -= 1
                else:
                    break
            # reset ro and cl
            ro = row
            cl = col
            # these next 2 while loops are for checking 'upperLeftMatches'
            while ro > 0 and cl > 0:
                if brd[ro-1][cl-1] == player:
                    upperLeftMatches += 1
                    ro -= 1
                    cl -= 1
                else:
                    break
            # reset ro and cl
            ro = row
            cl = col
            while ro < 5 and cl < 6:
                if brd[ro+1][cl+1] == player:
                    upperLeftMatches += 1
                    ro += 1
                    cl += 1
                else:
                    break
        # if there was 4 or more matches in any diagonal direction then return true for the player has won
            if upperLeftMatches >= 4:
                return True
            elif upperRightMatches >= 4:
                return True
            else:
                return False
        # the position was not filled by the player
        else:
            return False

    def isGameTie(self):
        "Check if the game is a tie"
        Istie = True
        # we can reference self.board with some shorthand 'brd'
        brd = self.board

        # Note: since this function is only called after checking if
        # a player has won, it is true that if no player has won and
        # the board has no empty spaces then the game is a tie
        for row in brd:
            for mark in row:
                if mark == 0:
                    Istie = False
                    break
        return Istie

    def winner(self):
        player = 1
        for i in range(2):
            for row in range(6):
                for col in range(7):
                    if ((self.checkHorizontal(row, col, player)) or
                            (self.checkDiagnonal(row, col, player)) or (self.checkVertical(row, col, player))):
                        self.isEnd = True
                        return player
            player *= -1
        if self.isGameTie():
            self.isEnd = True
            return 0
        else:
            return None

    # only when the game ends (but should we do it per move?)
    def giveReward(self):

        result = self.winner()
        # backpropagate reward
        # boards leading to previous winning board
        # are given percentages of winning reward
        # so like 0.10 ... 0.9, 1

        # if player 1 wins the game
        if result == 1:
          # give player 1 a reward of 1
          # give player 2 a reward of 0
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        # if player 2 wins the game
        elif result == -1:
          # give player 1 a reward of 0
          # give player 2 a reward of 1
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        # the game is a tie
        else:
          # give both players a reward of 0.1
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.1)

    def reset(self):
        self.board = np.zeros((6, 7))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self, rounds=10000):
      # simulate games
        for i in range(rounds):
            print("Round {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                # need to manipulate chooseAction function
                p1_action = self.p1.chooseAction(
                    positions, self.board, self.playerSymbol)
                # take action and update board state
                self.updateState(p1_action[0], p1_action[1])
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(
                        positions, self.board, self.playerSymbol)
                    self.updateState(p2_action[0], p2_action[1])
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # play with a human

    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(
                positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action[0], p1_action[1])
            print(self.showBoard())
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                print(self.showBoard())
                p2_action = self.p2.chooseAction(positions, self.board)

                self.updateState(p2_action[0], p2_action[1])
                print(self.showBoard())
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def playTrained(self, rounds):
        p1_wins = 0
        p2_wins = 0
        ties = 0
        for i in range(rounds):
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(
                    positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action[0], p1_action[1])
                self.showBoard()
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    if win == 1:
                        print(self.p1.name, "wins!")
                        p1_wins += 1
                    else:
                        print("tie!")
                        ties += 1
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    print(self.showBoard())
                    p2_action = self.p2.chooseAction(
                        positions, self.board, self.playerSymbol)

                    self.updateState(p2_action[0], p2_action[1])
                    print(self.showBoard())
                    win = self.winner()
                    if win is not None:
                        if win == -1:
                            print(self.p2.name, "wins!")
                            p2_wins += 1
                        else:
                            print("tie!")
                            ties += 1
                        self.reset()
                        break

        print(p1_wins)
        print(p2_wins)
        print("Player One Won {}% of the time".format(
            round((p1_wins/rounds)*100, 2)))
        print("Player Two Won {}% of the time".format(
            round((p2_wins/rounds)*100, 2)))
        print("There were {} ties".format(ties))

    def playRandom(self, rounds):
        p1_wins = 0
        p2_wins = 0
        ties = 0
        for i in range(rounds):
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(
                    positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action[0], p1_action[1])
                self.showBoard()
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    if win == 1:
                        print(self.p1.name, "wins!")
                        p1_wins += 1
                    else:
                        print("tie!")
                        ties += 1
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    print(self.showBoard())
                    p2_action = self.p2.chooseAction(positions, self.board)

                    self.updateState(p2_action[0], p2_action[1])
                    print(self.showBoard())
                    win = self.winner()
                    if win is not None:
                        if win == -1:
                            print(self.p2.name, "wins!")
                            p2_wins += 1
                        else:
                            print("tie!")
                            ties += 1
                        self.reset()
                        break

        print(p1_wins)
        print(p2_wins)
        print("Player One Won {}% of the time".format(
            round((p1_wins/rounds)*100, 2)))
        print("Player Two Won {}% of the time".format(
            round((p2_wins/rounds)*100, 2)))
        print("There were {} ties".format(ties))

    def showBoard(self):
        game_display = "1. |"
        row_count = 1
        for row in self.board:

            for mark in row:
                # the piece is X
                if mark == 1:
                    game_display += "X" + "|"
                # the piece is O
                elif mark == -1:
                    game_display += "O" + "|"
                else:
                    # empty space
                    game_display += "-" + "|"
            row_count += 1
            if row_count < 7:
                game_display += "\n" + str(row_count)+". |"
        game_display += "\n    1 2 3 4 5 6 7"
        return game_display

# player object inputted into State class


class Player:
    def __init__(self, name, exp_rate=0.3):  # exp_rate = 0.3 means 70% of the time, our agent will take a greedy action, which is choosing the baction based on our current estimation of states-value, and 30% of the time our agent will take a random action; this is the exploration/explotation tradeoff
        self.name = name
        self.states = []  # records all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        # give 90% to previous board and then 0.9**2 and so forth
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        return str(board.reshape(42))

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
          # exploitation method
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p[0]][p[1]] = symbol
                next_boardHash = self.getHash(next_board)
                if self.states_value.get(next_boardHash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_boardHash)
                # print("value", value)
                if value > value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        # this seems like the function that needs to be understood; it updates the rewards throughout the game
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * \
                (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions, brd):
        while True:
            col = int(input("Input your action column:")) - 1
            row = self.findRowIndice(col, brd)
            action = (row, col)
            if action in positions:
                return action

    def findRowIndice(self, column, brd):
        "given a column find the space that a piece can be dropped in"
        row = 0
        # we can reference self.board with some shorthand 'brd'

        # note that if row is returned as -1 that means the column is filled
        while row < 6:
            if brd[row][column] in [-1, 1]:
                row -= 1
                return row
            elif brd[row][column] == 0 and row == 5:
                return row
            elif brd[row][column] == 0:
                row += 1


class RandomPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions, brd):
        while True:
            col = np.random.choice(7)
            row = self.findRowIndice(col, brd)
            action = (row, col)
            if action in positions:
                return action

    def findRowIndice(self, column, brd):
        "given a column find the space that a piece can be dropped in"
        row = 0
        # we can reference self.board with some shorthand 'brd'

        # note that if row is returned as -1 that means the column is filled
        while row < 6:
            if brd[row][column] in [-1, 1]:
                row -= 1
                return row
            elif brd[row][column] == 0 and row == 5:
                return row
            elif brd[row][column] == 0:
                row += 1


if __name__ == "__main__":
    # training
    p1 = Player("X")
    p2 = Player("O")

    # create boards
    st = State(p1, p2)
    print("training....")
    # train with 10,000 games
    st.play(10_000)
    # save both policies
    p1.savePolicy()
    p2.savePolicy()

    # see how q-learning computer plays against random player
    # percentage of won games will be printed
    # p1 = Player("computer", exp_rate=0)
    # p1.loadPolicy("policy_X")
    # p2 = RandomPlayer("Random")
    # st = State(p1, p2)
    # st.playRandom(50)
    # input("Continue? ")

    # have Q-Learning players play against each other
    p2 = Player("computer2", exp_rate=0)
    p2.loadPolicy("policy_O")
    st = State(p1, p2)
    st.playTrained(1000)

    input("Continue? ")

    # play with a human
    p2 = HumanPlayer("Human")
    st = State(p1, p2)
    st.play2()
