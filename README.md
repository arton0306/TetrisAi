# TetrisAi

This is designed for fun and to test genetic algorithm.

There are 2 versions of AI.

1. Simple AI
  - Setting AI parameters manually, and just considering current tetris piece.
  - Only 2 files: TetrisAi.py and TetrisObject.py, < 400 lines totally.
  - Run: _python3 TetrisAi.py_
2. Smart AI
  - Trainning AI parameters with genetic algorithm, and considering current and next tetris pieces.
  - Only 2 files: TetrisAiMultiBlock.py and TetrisObject.py, < 600 lines totally.
  - Run: _python3 TetrisAiMultiBlock.py_
  - You can switch to train mode by modified the do_train flag in TetrisAiMultiBlock.py

### Output Example For Smart AI
The result of Ai output in console by the format as below, or see [replay.txt](replay.txt) for a full example ).
``` txt
...
 Got Block: S	 Next Block: T
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o o o 
o o o o o o o o x x 
o o o o o o o x x x 
o o o o o o o x x x 
o o o o o x x x o x 
o x x o o x x x x x 
o x x x x x x x x x 
o x x x x x x x x x 
o x x x x x x x x o 
o x x x x x x x x x 
x x x x x o x x x x 
x x x x x x x x o x 
topfilledgrid = [18, 13, 13, 14, 14, 12, 12, 10, 9, 9]
revtopfilledgrid = [2, 7, 7, 6, 6, 8, 8, 10, 11, 11]
filledGridCount = 72
holeCount = 4
blockadeCount = 22
lastLineClearCount = 1
totalBlockCount = 893
combo = 1
...
```

### Other Files
The other files are for enabling simple AI to play TetrisBattle in Facebook. It gets next block by looking at the RBG of a hard-coded position of the window of facebook tetrix battle, and move or rotate the block by sending keyboard signal with heuristic delay. It has some hard-coded part, so it needs to be tuned if you want to try it. I would like to recommend just to take it as a reference.
