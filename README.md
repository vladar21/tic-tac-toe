# Tic-Tac-Toe Game

This Python command-line game, "Tic-tac-toe", allows you to compete against artificial intelligence. The AI can be trained using gameplay data and played against it, which makes the game interesting not only because of the gameplay, but also because it is fun to watch the AI evolve in real time.

[View the live project here.](https://vladar21.github.io/english-teacher/)

## Description
This console-based Tic-Tac-Toe game provides an opportunity to play the classic game against an AI opponent. The AI can be trained through gameplay data and then used to make predictions based on its training. The game is designed to provide an enjoyable and challenging experience for players of all skill levels.

## User Goals
- **Play Tic-Tac-Toe:** Users can play the game against the AI.
- **Train the AI:** Users can train the AI model by playing games against it.
- **Load an AI Model:** Users can load an existing AI model for gameplay.
- **Enjoyable Experience:** Users should have a fun and engaging gaming experience.

## User Stories
As a user, I want to:
1. **Play Tic-Tac-Toe against the computer.**
   - I can enjoy a game of Tic-Tac-Toe without needing a human opponent.
2. **Train the AI model by playing games against it.**
   - I can improve the AI's skill by playing games and letting it learn from our interactions.
3. **Load an existing AI model to play against.**
   - I can use a pre-trained AI model to challenge my Tic-Tac-Toe skills.
4. **Have an easy and intuitive way to make moves during the game.**
   - I should be able to make my moves simply and quickly.
5. **Receive feedback on the game's outcome.**
   - I want to know who won, lost, or if the game ended in a draw.

## Features
- **Tic-Tac-Toe Game:** The core feature is a console-based Tic-Tac-Toe game.
- **AI Model Training:** Users can train the AI model through gameplay data.
- **AI Model Usage:** Trained AI models can be loaded and used to play against.
- **User-Friendly Moves:** The game provides an intuitive way for users to make moves.
- **Outcome Feedback:** At the end of the game, the outcome is displayed.

## Technologies Used
- **Python:** The core programming language used for the game.
- **TensorFlow:** For building and training the AI model.
- **gspread:** To interact with Google Sheets for data storage.
- **Google Sheets API:** To manage game data.

## Installation and Usage
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe.git
   cd tic-tac-toe
2. **Install Dependencies:**
    
    Install the required Python libraries using pip:

    ```bash    
    pip install -r requirements.txt
4. **Run the Game:**
    
    Start the game by running the main.py script.
    ```bash
    python main.py
5. **Gameplay:**
    - Follow the on-screen instructions to play the game.
    - Make your moves by entering a number from 0 to 8, indicating the position on the board.
    - The game will provide feedback on the outcome.

## Future Enhancements
Here are several ideas for improving this project in the future:

- Implement a graphical user interface (GUI) to make the game more visually appealing.
- Enhance the AI training capabilities to improve its skill and decision-making.
- Add functionality to save and load gameplay data and AI models.

## Testing
We have performed thorough testing, including unit tests for the game logic and AI training process. We are continuously working to ensure the game's reliability and performance.

## Bugs
Under construction

## Deployment
This is a console-based game, and there is no specific deployment process. You can run it on your local machine without the need for hosting or server deployment.

## Credits
Code: 

Content: 

Media: 

Acknowledgements: 



## License
This project is open-source and licensed under the MIT License. You are free to use, modify, and distribute the code in accordance with the license terms.