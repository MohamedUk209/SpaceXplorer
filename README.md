# SpaceXplorer

**Version:** 1.0 
**Author:** Mohamed  
**Language:** C ( Python for testing)

## Overview

**SpaceXplorer** is a terminal-based C game where you play as a lone astronaut navigating a hazardous galaxy. Your mission is to **collect space junk**, **avoid asteroids**, **evade alien threats**, and survive until rescue. Every move costs fuel, and your decisions affect your fate. Can you survive long enough?

## Gameplay Features

- 18x18 space map rendered in ASCII
- Movement via `W`, `A`, `S`, `D`
- Live ship status panel (`H` key)
- Space junk collection system with reward choice:
  - `F` → +5 Fuel
  - `R` → +2 Repair (Health)
- Randomly moving alien that causes damage
- Moving asteroid that ends the game on collision
- Difficulty selection (Easy, Medium, Hard)
- Score saving and test mode support

---

## Controls

| Key | Action                     |
|-----|----------------------------|
| W   | Move Up                   |
| A   | Move Left                 |
| S   | Move Down                |
| D   | Move Right               |
| H   | Check System Status      |
| F/R | Reward after collecting junk |

---

## How to Compile

gcc -o game main.c map.c game.c fileio.c


---

## How to Run

```bash
./game


