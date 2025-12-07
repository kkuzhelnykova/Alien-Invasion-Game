# Alien-Invasion-Game

**Author:** Karyna Kuzhelnykova
**Course:** SFWE 101 (Alien Invasion Game Project)
**IDE:** Visual Studio Code
**Language:** Python
**Libraries:** Pygame

---

##  Overview

This project is a customized version of the “Alien Invasion” game built with Python and Pygame.
The player controls a spaceship at the bottom of the screen, moves left/right, and fires bullets to destroy a descending alien fleet. The player has a limited number of ships (lives), and the game ends when all ships are lost.

This version includes **required features** from the course and **additional student-developed features**.

---

## 🎮 Game Controls

| Key       | Action                   |
| --------- | ------------------------ |
| **← / →** | Move ship left / right   |
| **SPACE** | Fire bullet              |
| **P**     | Pause / Unpause the game |
| **Q**     | Quit game                |
| **Mouse** | Click pause menu buttons |

---

## Required Features Implemented

### **1. Multiple Ships (Lives)**

* The player begins with a set number of ships (default = 4).
* Each time the ship is hit by an alien, `ships_left` is decremented.
* When `ships_left` reaches **0**, the game ends with a **YOU LOST** screen.

### **2. Alien Destruction Counter**

* The game counts the total number of aliens destroyed.
* This value increases each time a bullet hits an alien.

### **3. On-Screen Display**

Both required values are displayed on screen during gameplay:

* **Ships left**
* **Aliens hit**

---

## Additional Features Implemented

### **Pause Menu with Buttons**

Press **P** to pause the game.
The pause screen shows three clickable buttons:

#### ✔ Continue

Resume the game from the exact paused state.

#### ✔ New Game

* Resets ships
* Resets alien fleet
* Resets kill counter
* Restarts gameplay

#### ✔ Quit

Exits the game entirely.

The menu uses a custom `Button` class with mouse collision detection and scaled PNG images.

---

##  Project Structure

```
Alien-Invasion-Game/
│
├── main.py                # Main game loop and logic
├── settings.py            # Game settings (speed, sizes, limits)
├── ship.py                # Player ship class
├── bullet.py              # Bullet behavior
├── alien.py               # Alien logic
├── game_stats.py          # Track ships left, game state, statistics
├── button.py              # Button class for pause menu
│
└── Images/                # Button images
    ├── continue.png
    ├── newGame.png
    └── quit.png
```

---

##  How to Run the Game

### **Prerequisites**

Install Python 3.12 and Pygame:

```bash
python3.12 -m pip install pygame
```

### **Run the game**

```bash
python3.12 main.py
```

---

## Testing the Features

### ✔ Ship counter testing

* Allow aliens to collide with the ship or reach the bottom.
* Ensure `ships_left` decreases correctly.
* When ships reach 0, verify the game ends.

### ✔ Alien destruction counter testing

* Destroy aliens and confirm `kill_count` increases by 1 per alien.
* Confirm counter resets when clicking New Game.

### ✔ Pause menu testing

* Press **P** to pause the game.
* Test each button:

  * **Continue** resumes gameplay.
  * **New Game** resets the game state.
  * **Quit** exits successfully.
