# AI-Agent-For-Checkers-Game
The methodology that I implemented in student.py is the combination of Minimax and MCTS. I found out that in the game of Checkers, Minimax can take rational moves at the first several moves to take advantages. Then in the further games, we need deeper thoughts so I use MCTS to take the moves. 
If you modify the usage between Minimax and MCTS, you can do it in studentAI.py. 

To run under manual mode, please use this command "python3 main.py {row} {col} {k} m {order}"

e.g. "python3 main.py 7 7 2 m 0"
e.g. "python3 main.py 7 7 2 l {AI_path 1} {AI_path 2}"
e.g. "python3 main.py 7 7 2 n {AI_path}"

Because the initialization of network mode is different from the normal modes,
the initialization of network mode is separated from other modes.
