# The Tic Tac Toe with AI

## Table of Contents

- [Project Goals](#project-goals)
- [User Experience](#user-experience)
- [Design](#design)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Clone a Repository Code Locally](#clone-a-repository-code-locally)
- [Forking in GitHub](#forking-in-github)
- [Credits](#credits)

---

## Project Goals

### User Goals

- Provide an engaging, old-school game of Tic Tac Toe that users can play against a self-learning AI.
- Offer a leaderboard system where users can see their rankings based on game outcomes.

### Site Owner Goals

- Create an interactive and funny game that keeps users returning and competing for the top leaderboard positions.
- Collect and use gameplay data to improve AI algorithms.
- Improve the owner's machine learning skills.

[Back to Table of Contents](#table-of-contents)

---

## User Experience

### Target Audience

- Individuals looking for a quick and entertaining game that challenges their strategic thinking.
- Players interested in competing against AI with learning capabilities.

### User Stories

- As a user, I want to easily understand how to play the game and what the rules are.
- As a player, I wish to see my game history and how I rank compared to other players.
- As a competitive user, I want the AI to be challenging enough that it provides a sense of accomplishment when I win.

[Back to Table of Contents](#table-of-contents)

---

## Design

### Flowchart 

- The flowchart details the logic of the game, the decision-making process of the AI, and the interactions between different modules of the application.

[Back to Table of Contents](#table-of-contents)

---

## Features

#### Welcome Screen

- A friendly interface greets the user and presents them with options to start a new game, view the leaderboard, or exit.

#### Game Rules

- The rules are succinctly outlined for quick reference for new and returning players.

#### Game Play

- The game play is turn-based, with the user making moves against the AI. The state of the game is displayed after each move, and the game announces the winner or a draw when the game concludes.

[Back to Table of Contents](#table-of-contents)

---

## Technologies Used

- Python for the main game logic.
- TensorFlow for implementing and training the AI model.
- Google Sheets API for storing game outcomes and leaderboard.
- Google Drive API for managing the AI model's storage.

[Back to Table of Contents](#table-of-contents)

---

## Testing

### Python Validation

- The code was validated using pylint and adheres to PEP8 standards, ensuring readability and maintainability.

### Manual Testing

- The game was manually tested to ensure all features function as intended and that the user interface is intuitive and responsive.

[Back to Table of Contents](#table-of-contents)

---

## Bugs

- [Under Constraction].

[Back to Table of Contents](#table-of-contents)

---

## Deployment

### Version Control

- The development process utilized Git for version control, with regular commits and descriptive messages to track changes and facilitate collaboration.

### Heroku Deployment

- Detailed steps are provided on how the game was deployed on Heroku, allowing users to access it through a web interface.

---

### Clone a Repository Code Locally

To clone the repository and run this Tic Tac Toe game locally on your machine, you will need to follow these steps:

#### Prerequisites

Before you begin, make sure you have the following installed:
- [Git](https://git-scm.com/downloads)
- Python (at least version 3.6)
- A text editor or an IDE (like Visual Studio Code, PyCharm, etc.)

#### Cloning the Repository

1. **Open Terminal**: Open your terminal, command prompt, or Git bash in the directory where you wish to clone the repository.

2. **Clone the Repository**: Use the following Git command to clone the repository:

    ```bash
    git clone https://github.com/your-username/tic-tac-toe-with-ai.git
    ```

    Replace `your-username` with the actual username where the repository exists.

3. **Navigate to the Repository Directory**: Once the repository has been cloned, navigate to the cloned repository directory:

    ```bash
    cd tic-tac-toe-with-ai
    ```

4. **Create a Virtual Environment** (optional but recommended): Run the following commands to create and activate a virtual environment:

    For Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    For macOS and Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

5. **Install Dependencies**: Install all the required dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

    This command reads the `requirements.txt` file and installs all the Python packages needed for the game to run.

6. **Run the Game**: You can now run the game using the following command:

    ```bash
    python run.py
    ```

    Replace `main.py` with the actual entry script if it’s named differently.

#### Contribute to the Development

If you want to contribute to the game's development, it's generally a good practice to:

1. Fork the repository.
2. Clone your forked version of the repository.
3. Create a new branch for your feature or fix.
4. Make your changes and commit them with descriptive commit messages.
5. Push the changes to your fork.
6. Open a pull request to the original repository.

Please ensure you adhere to the contribution guidelines provided by the repository owner.

[Back to Table of Contents](#table-of-contents)

---

## Credits

### Code

- Attribution to open-source libraries and code snippets that were utilized in the creation of the game.

### Design

- Recognition of any design inspiration or assets that were used to create the user interface.

### Acknowledgements

- Special thanks to individuals who have contributed to the ideation, development, and testing phases of the game.

[Back to Table of Contents](#table-of-contents)
