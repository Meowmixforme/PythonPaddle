# PythonPaddle

A classic Ping-Pong arcade game implementation in Python using Pygame. This project features both single-player (against AI) and two-player modes with physics-based ball movement, visual effects, and sound.

![Screenshot 2025-06-14 194002](https://github.com/user-attachments/assets/453b6430-7b73-4839-82d7-acce3ff5490d)

![Screenshot 2025-06-14 194018](https://github.com/user-attachments/assets/295ca365-47a3-4447-8abb-39775715d447)

![Screenshot 2025-06-14 194101](https://github.com/user-attachments/assets/14ee04a6-6c63-4221-aca1-15678682635b)



## Features

- Classic Ping-Pong gameplay mechanics
- Single-player mode with AI opponent
- Two-player local multiplayer
- Physics-based ball movement with realistic paddle collisions
- Visual effects including ball trails
- Sound effects for enhanced gameplay experience
- Score tracking and win conditions
- Menu system for game navigation

## Installation

### Prerequisites

- Python 3.x
- Pygame library

### Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/Meowmixforme/pythonpaddle.git
    cd pythonpaddle
    ```

2. Install dependencies:

    ```bash
    pip install pygame
    ```

3. Run the game:

    ```bash
    python pythonpaddle_main.py
    ```

## How to Play

### Menu Navigation
- Use arrow keys to navigate and Enter to select

### Player 1 (Left Paddle)
- **W**: Move Up
- **S**: Move Down

### Player 2 (Right Paddle)
- **Up Arrow**: Move Up
- **Down Arrow**: Move Down

### General
- **ESC**: Return to menu/Exit game

## Game Rules

- First player to reach 10 points wins
- If the ball passes your paddle, the opponent scores a point
- The ball speeds up slightly with each paddle hit
- Ball direction changes based on where it hits the paddle

## Project Structure

```
pythonpaddle/
├── pythonpaddle/
│   ├── __init__.py
│   ├── assets/
│   │   └── sounds/
│   │       ├── paddle_hit.wav
│   │       ├── wall_hit.wav
│   │       └── score.wav
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ball.py
│   │   ├── paddle.py
│   │   └── scoreboard.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game_engine.py
│   │   └── physics.py
│   ├── states/
│   │   ├── __init__.py
│   │   ├── game_state.py
│   │   ├── menu_state.py
│   │   └── state_machine.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── sound_manager.py
│   └── main.py
├── pythonpaddle_main.py
└── setup.py
```

## Customization

You can customize various aspects of the game by modifying the `pythonpaddle/utils/config.py` file:

- Window dimensions
- Colors
- Game speed
- Paddle and ball sizes
- Winning score
- Sound settings

## Sound Credits

- **Score Sound:** CorrectCh_New.mp3 by Gronkjaer | [Source](https://freesound.org/people/Gronkjaer/sounds/654321/) | License: Creative Commons 0
- **Paddle Hit Sound:** Table Tennis by michorvath | [Source](https://freesound.org/people/michorvath/sounds/269718/) | License: Creative Commons 0
- **Wall Hit Sound:** Sports Whistle by SomeGuy22 | [Source](https://freesound.org/people/SomeGuy22/sounds/431327/) | License: Creative Commons 0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original Pong game by Atari (1972)
- Pygame library and community
- Sound effects from Freesound.org contributors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add some amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request  
