# Shuffled

A 5×5 sliding tile puzzle game built with Pygame.

## About

Shuffled is a classic slide puzzle where you rearrange 24 tiles on a 5×5 grid to restore them to the correct order. The 25th tile is the blank space you slide pieces into.

## Requirements

- Python 3.x
- Pygame

```bash
pip install pygame
```

## Setup

1. Clone the repo
2. Place tile images (`0.png` – `24.png`) and `border1.png` inside an `assets/` folder in the project root
3. Run the game:

```bash
python main.py
```

## How to Play

- **Click a tile** to select it
- **Click the blank neighbour** to slide the tile into that space
- Arrange all tiles in order to win
- Press **R** to restart at any time

## Project Structure

```
shuffled/
├── main.py
└── assets/
    ├── 0.png – 24.png   # Tile images
    └── border1.png       # Board border
```
