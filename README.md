# Tertis Game

## Description
A Python-based retro arcade application that simulates a classic Tetris game using the Pyxel game engine. The project demonstrates core game development principles such as game loops, collision detection, state management, and persistent data storage using JSON.


---

## How the Code Works
The Pyxel Tetris application is designed as a single-class engine that manages the game lifecycle—from initialization and input handling to physics and rendering. It utilizes a grid-based coordinate system to manage piece movement and board state.

➤ **Core Architecture and Logic** <br>
The application is built around the TetrisApp class, which orchestrates the interaction between game pieces and the static board:

   - **Piece Management:** The Piece class handles the geometry of the seven classic Tetrominoes (I, O, T, S, Z, J, L). It includes logic for matrix rotation using Python’s zip function and list slicing.

   - **Collision & Physics:** The collision method checks the piece's coordinates against the board boundaries and existing locked blocks. It supports Wall Kicks, allowing pieces to shift slightly during rotation if they hit a wall.

   - **Game Loop:** Pyxel’s update function handles the gravity logic (auto-drop), while the draw function renders the UI, including a "Ghost Piece" that previews where the block will land.


➤ **Scoring and Progression** <br>
The system mimics authentic Tetris mechanics to calculate difficulty and rewards:

**Line Clears:** When a row is full, it is removed, and the board above is shifted down.

**Dynamic Difficulty:** The level increases for every 10 lines cleared, which in turn reduces the drop_timer to make the game faster.

**Scoring Formula:** Points are awarded based on the number of lines cleared simultaneously (1, 2, 3, or 4), multiplied by the current level. Bonus points are awarded for Soft Drops and Hard Drops.


➤ **Data Persistence**
The application includes a persistent high score system. Upon game over or a score increase, the system checks the current score against the value stored in a local JSON file. This ensures that the "Best Score" is remembered even after the application is closed.

---

