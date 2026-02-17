# Connections Game 

A Python clone of the [New York Times Connections](https://www.nytimes.com/games/connections) word puzzle game.

## About

Group 16 words into 4 categories of 4. Each category shares a hidden connection—find all four groups before you run out of mistakes!

## Screenshot

![Connections Game](connections.png)

## Requirements

- Python 3.x
- tkinter
- tkmacosx
- pandas
- openpyxl

## Installation

```bash
pip install tkmacosx pandas openpyxl
```

## Setup

1. Create an Excel file named `connections_groups.xlsx`
2. Add 4 sheets, one for each color/difficulty:
   - Sheet names should be color codes (e.g., `#f9df6d`, `#a0c35a`, `#b0c4ef`, `#ba81c5`)
3. Each sheet should have one column with the category name as the header and 4 words below

**Example sheet structure:**

| FRUITS |
|--------|
| Apple  |
| Banana |
| Orange |
| Grape  |

4. Add a `connections.png` image for the start screen (optional)

## How to Play

```bash
python connections.py
```

1. Click **Play** to start
2. Select 4 words you think belong to the same category
3. Click **Submit** to check your guess
4. Find all 4 groups before making 4 mistakes

### Controls

- **Shuffle** — Randomize word positions
- **Deselect All** — Clear current selection
- **Submit** — Check if selected words form a group

## License
MIT
