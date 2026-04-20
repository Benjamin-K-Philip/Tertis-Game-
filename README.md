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

   - **Line Clears:** When a row is full, it is removed, and the board above is shifted down.

   - **Dynamic Difficulty:** The level increases for every 10 lines cleared, which in turn reduces the drop_timer to make the game faster.

   - **Scoring Formula:** Points are awarded based on the number of lines cleared simultaneously (1, 2, 3, or 4), multiplied by the current level. Bonus points are awarded for Soft Drops and Hard Drops.


➤ **Data Persistence**
The application includes a persistent high score system. Upon game over or a score increase, the system checks the current score against the value stored in a local JSON file. This ensures that the "Best Score" is remembered even after the application is closed.

---

## Features <br>
  - **Classic Gameplay:** Includes all 7 Tetromino shapes with accurate rotation and movement.

  - **Ghost Piece:** Provides a visual guide showing the landing position of the current piece.

  - **Persistent High Score:** Saves and loads the highest score using a JSON data file.

  - **Leveling System:** Increases game speed and scoring potential as the player clears lines.

  - **Preview Window:** Shows the "Next" piece to help players plan their moves.

  - **Responsive Controls:** Supports both Arrow keys and WASD for movement, rotation, and drops.

---

## Project Structure <br>
  - **pyxel (External Package):** The core game engine used for rendering pixel art, handling window events, and managing the 60 FPS game loop.

  - **json (Standard Library):** Used to parse and write the pyxel_tetris_highscore.json file, ensuring the high score is stored in a structured, readable format.

  - **TetrisApp (Main Class):** Contains the primary game logic, including update() for mechanics and draw() for graphics.

  - **Piece (Helper Class):** Defines the shapes, colors, and rotation behavior of individual Tetrominoes.

  - **highscore.json:** A local data file created automatically to store the highest score achieved on that machine.

---


## Output
<img width="1366" height="720" alt="Screenshot (7680)" src="https://github.com/user-attachments/assets/e3f92185-d145-4b8b-97e0-1a4a6df38ec1" />
<br>
<img width="1366" height="720" alt="Screenshot (7682)" src="https://github.com/user-attachments/assets/57048a3d-5b8f-478a-a257-39e5b49c2694" />
<br>
<img width="1366" height="718" alt="Screenshot (7853)" src="https://github.com/user-attachments/assets/2a7993cc-7610-4fd1-9493-f95b59e82aac" />
<br>
<img width="1366" height="718" alt="Screenshot (7854)" src="https://github.com/user-attachments/assets/d82799d2-dced-436c-9aea-7d1cb157eb7d" />
<br>
<img width="1366" height="720" alt="Screenshot (7855)" src="https://github.com/user-attachments/assets/c87e7e42-c491-4527-933a-16408ecefeff" />
<br>
<img width="1366" height="720" alt="Screenshot (7859)" src="https://github.com/user-attachments/assets/c2e29e6c-315d-4a30-972c-e40d8f08a862" />
<br>
<img width="1366" height="718" alt="Screenshot (7857)" src="https://github.com/user-attachments/assets/cba0a12a-5158-479f-ae9a-d53e36406a15" />
<br>
<img width="1366" height="720" alt="Screenshot (7856)" src="https://github.com/user-attachments/assets/d0c608ea-6547-42af-9d9c-6572abad4566" />
<br>
