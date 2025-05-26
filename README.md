# 🐍 Terminal Snake Game

A classic Snake game implementation that runs in your terminal, featuring colorful graphics, smooth controls, and progressive difficulty.

```
+-------------------+
|    SNAKE GAME     |
| Score: 50     ◆   |
|         █▒▒▒▒     |
|                   |
|    ◆              |
|                   |
+-------------------+
```

## ✨ Features

- 🎮 Smooth terminal-based gameplay
- 🎨 Full color support (when available)
- 📈 Progressive difficulty - snake speeds up as your score increases
- 💫 Unicode graphics with ASCII fallbacks
- ⌨️ Intuitive arrow key controls
- 🏆 Score tracking
- 🖥️ Dynamic terminal size handling
- 🎯 Random food placement
- 🔄 Restart game functionality

## 🚀 Requirements

- Python 3.x (Developed and tested with Python 3.12.6)
- Terminal with curses support (most modern terminals)
- Terminal with color support (optional, falls back to monochrome)

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:EricLamphere/snake_game.git
   cd snake_game
   ```

2. Make the game executable:
   ```bash
   chmod +x snake.py
   ```

## 🎮 How to Play

1. Start the game:
   ```bash
   python3 snake.py
   ```

2. Controls:
   - ⬆️ Up Arrow: Move up
   - ⬇️ Down Arrow: Move down
   - ⬅️ Left Arrow: Move left
   - ➡️ Right Arrow: Move right
   - Q: Quit game
   - R: Restart after game over

3. Gameplay:
   - Eat food (◆) to grow and increase your score
   - Avoid hitting the walls or yourself
   - The snake speeds up as your score increases
   - Try to achieve the highest score possible!

## 🛠️ Technical Details

- Written in Python using the curses library
- Implements smooth terminal graphics handling
- Features dynamic terminal size adaptation
- Includes graceful error handling
- Uses Unicode characters with ASCII fallbacks
- Supports color terminals with graceful degradation

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements you'd like to add!

## 📜 License

This project is open source and available under the MIT License.

---
Created with 💚 by Eric Lamphere
