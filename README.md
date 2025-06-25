# MIU Formal System Theorem Generator

Infinitely generate theorems from the [MIU formal system](https://en.wikipedia.org/wiki/MU_puzzle) definied in [Gödel, Escher, Bach](https://en.wikipedia.org/wiki/Gödel,_Escher,_Bach)'s "The MU Puzzle" chapter.

A breadth-first theorem generator that builds valid theorems from axioms using transformation rules. This implementation maintains proper tree structure while preventing duplicate theorem generation.

## Features

- **Tree Structure**: Maintains actual parent-child relationships for derivation tracking
- **BFS Generation**: Uses breadth-first search for systematic theorem exploration
- **Derivation Paths**: Tracks how each theorem was derived from the axiom

## MIU System Example

Starting from axiom `"MI"` with four transformation rules:
- Rule 0: If string ends with 'I', add 'U'
- Rule 1: If string starts with 'M', duplicate everything after 'M'
- Rule 2: Replace 'III' with 'U'
- Rule 3: Remove 'UU'

## Usage

```python
from theorem_generator import generate_theorem_tree_optimized, AXIOM, RULES

# Generate theorem tree up to level 4
root = generate_theorem_tree_optimized(axiom=AXIOM, rules=RULES, max_level=4)
```

## Sample Output

```
=== Optimized Theorem Generation ===
Total unique theorems generated: 19

=== Tree Structure ===
├─ MI (level 0)
  ├─ MIU (level 1)
    ├─ MIUIU (level 2)
      ├─ MIUIUIUIU (level 3)
        ├─ MIUIUIUIUIUIUIUIU (level 4)
  ├─ MII (level 1)
    ├─ MIIU (level 2)
      ├─ MIIUIIU (level 3)
        ├─ MIIUIIUIIUIIU (level 4)
    ├─ MIIII (level 2)
      ├─ MIIIIU (level 3)
        ├─ MIIIIUIIIIU (level 4)
        ├─ MUIU (level 4)
      ├─ MIIIIIIII (level 3)
        ├─ MIIIIIIIIU (level 4)
        ├─ MIIIIIIIIIIIIIIII (level 4)
        ├─ MUIIIII (level 4)
      ├─ MUI (level 3)
        ├─ MUIUI (level 4)

=== Theorems by Level ===
Level 0: ['MI']
Level 1: ['MIU', 'MII']
Level 2: ['MIUIU', 'MIIU', 'MIIII']
Level 3: ['MIUIUIUIU', 'MIIUIIU', 'MIIIIU', 'MIIIIIIII', 'MUI']
Level 4: ['MIUIUIUIUIUIUIUIU', 'MIIUIIUIIUIIU', 'MIIIIUIIIIU', 'MUIU', 'MIIIIIIIIU', 'MIIIIIIIIIIIIIIII', 'MUIIIII', 'MUIUI']

=== Sample Derivation Paths ===
Path to 'MIUIU': MI -> MIU -> MIUIU
Path to 'MIUIUIUIU': MI -> MIU -> MIUIU -> MIUIUIUIU
Path to 'MIUIUIUIUIUIUIUIU': MI -> MIU -> MIUIU -> MIUIUIUIU -> MIUIUIUIUIUIUIUIU
```

## Performance

- **Time Complexity**: O(U × R × S) where U=unique theorems, R=rules, S=string length
- **Space Complexity**: O(U) - linear in unique theorems only
- **Memory Optimization**: Prevents duplicate storage through theorem deduplication
