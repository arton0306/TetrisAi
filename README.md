# TetrixAi

This is designed for fun and to test genetic algorithm.

There are 2 versions of AI.

1. Simple AI
  - Setting AI parameters manually, and just considering current tetrix piece.
  - Only 2 files: TetrixAi.py and TetrixObject.py, < 400 lines totally.
  - Run: _python3 TetrixAi.py_
2. Smart AI
  - Trainning AI parameters with genetic algorithm, and considering current and next tetrix pieces.
  - Only 2 files: TetrixAiMultiBlock.py and TetrixObject.py, < 600 lines totally.
  - Run: _python3 TetrixAiMultiBlock.py_
  - You can switch to train mode by modified the do_train flag in TetrixAiMultiBlock.py

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
The other files are for enabling simple AI to play TetrixBattle in Facebook. Get tetrix piece by screenshot and control the game by send keyboard signal. Will not update these files in the future.
