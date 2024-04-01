# Red-Blue Nim

## Description

An agent that can play two versions (standard and misère) of the variant of a game called Nim (called red-blue nim against a human player).
The game consists of two piles of marbles (red and blue). On each players turn they pick a pile and remove one or two marbles from it (if possible). If on their turn, either pile is empty then they lose in the standard version and win in the misère version. The amount they lose (or win) is dependent on the number of marbles left (2 for every red marble and 3 for every blue marble). So if on the computers turn, it has 0 red marbles and 3 blue marbles, it loses 9 points in the standard version (or wins 9 points in the misère version)

## How to run

```bash
Play Red-Blue Nim.

positional arguments:
  num_red            Number of red marbles
  num_blue           Number of blue marbles
  {standard,misere}  Game version (default: standard)
  {computer,human}   First player (default: computer)
  depth              Depth for search, must be greater than 0 (default: 15)

options:
  -h, --help         show this help message and exit

```

To run the script with default arguments, run the following command:

```bash
python red_blue_nim.py <num_red> <num_blue>
```
