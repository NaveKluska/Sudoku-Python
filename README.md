# Sudoku-Python

**University project - graded 100 / 100**

## Overview
This program can

1. **Generate** a valid Sudoku puzzle  
2. **Play** interactively in the terminal  
3. **Solve** any board automatically (backtracking)  

All code is plain Python 3—no external libraries.

## How to run
```bash
python Main2.py
```                 

## Key files
| File       | Purpose                             |
|------------|-------------------------------------|
| `Main2.py` | Game loop, puzzle generator, solver |

## Algorithm notes
- Solver uses depth-first search with backtracking.  
- `possible_digits()` checks row, column, and 3×3 box sets in O(1).

© 2025 Nave Kluska
