# Steps Toward Creating a Connect 4 AI
After trying to find a machine learning algorithm to simulate and train from games of
Connect 4, I found the most success through a reinforcement learning technique called,
Q-learning. Before creating a Python program that uses Q-learning, I first wrote a starter
program that would contain the functions needed to play a game for Connect 4 such as a game
state evaluation function, and that program would allow for basic simulations between random
players and display results of those simulations. Connect 4 is played through a game board, so I
parametrized this board as one Python list that would contain 6 lists, and each of those lists
would contain 7 elements. This creates a 6x7 2-D Python list similar to a 6x7 Connect 4 board.
As humans, we can see pieces on the Connect 4 Boards as X’s and O’s or Red’s and Blue’s, and
we can parametrize those pieces with numbers mapped to those human-readable values. In my
program, I parametrized an empty space as 0, an X piece as 1, and an O piece as -1. Hence, when
initializing the python list serving as a game board, all of the elements in the lists will be 0s. The
next step to simulate Connect 4 was to create functions that found all the available moves for a
player and evaluate the game state. Finding all the viable moves based on the game board wasn’t
very difficult, but I did run into trouble when it came to evaluating the game state because I
created multiple functions to complete this task, and a few of those functions had unnoticed bugs
that were not easily fixed. After all these functions were successfully programmed, I was able to
simulate games between random players and compute some interesting results where after
10,000 games, player one won 55.41% of the time, player 2 won 44.33% of the time, and ties
occurred 0.26% of the time. From these results, one can see how the first player to move has an
advantage and ties are rare in the case of two players playing randomly.
Professor Shulman showed us an example of a Q-learning program for Tic Tac Toe, and it
was clear that a Connect 4 program could be created by using that program for Tic Tac Toe as a
template. Many of the functions needed to make a Q-learning program for Connect 4 were
conjured from just copying and pasting the code from the Connect 4 starter program with some
tweaks, For example, the variable serving as the parameterized game board in this new program
was a 2-D NumPy array, whereas the original variable was a 2-D Python list. From there, the

difficulty was just adjusting the code from the Tic Tac Toe template to a Connect 4 program.
Eventually, the program was running successfully, and I experimented by having two computers
train with the Q-learning algorithm by playing against each other for 10,000 games and then, one
of the trained computer players played against a random player for 10,000 games. I wanted to
gauge the effectiveness of the Q-learning player by seeing how well it could defeat a random
player, and the results were the Q-learning player won 86.35% of the time, the random player
won 13.65% of the time, and there were no ties. From these results, we can see that the
Q-learning player is in fact learning as the results do not mirror the data found from two random
players playing against each other for the same number of games since the Q-learning player
won 30.9% more of the time compared to a random player when playing against another random
player. After this data is found, the program will have the two trained Q-learning players play
against each other for 1000 games, the results are the first Q-learning player won 52.4% of the
time, the second player won 47.1% of the time, and there were 5 ties. Finally, the program will
have the Q-learning player play against a human opponent, that being the user running the
program, and anyone understanding the rules of Connect 4 will be able to defeat the Q-learning
player as it will make mistakes when a victory is about to occur such as failing to stop a Connect
4 by the human player.
The way we could improve the Q-learning program would be to make the Q-learning
players train more effectively by assigning reward values to boards before a game is won. This
was very difficult for me to include into my program because of my own confusion on how to do
such a process as well as how to include that in the code.
