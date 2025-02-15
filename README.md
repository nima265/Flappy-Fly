# Flappy-Fly

Flappy-Fly is a fun and addictive game written in Python, inspired by the classic Flappy Bird. The objective is simple: navigate your character through a series of obstacles without crashing. As the game progresses, the difficulty increases, providing endless entertainment and challenge.

## Features

- **Simple Controls**: Easy to learn, difficult to master.
- **Increasing Difficulty**: The game gets progressively harder as you advance.
- **High Score Tracking**: Keep track of your highest scores.
- **Colorful Graphics**: Enjoy a visually appealing gaming experience.
- **NEAT AI Integration**: Watch an AI learn and master the game using the NEAT algorithm.

## Getting Started

### Prerequisites

To run Flappy-Fly, you need to have Python installed on your machine. You can download Python from the [official website](https://www.python.org/).

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/nima265/Flappy-Fly.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Flappy-Fly
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Game

Once you have installed the dependencies, you can start the game by running the following command:
```bash
python FlappyFlyGame.py
```

## How to Play

1. When you run the game, you will first see a menu with a play button.
2. Press the play button to go to the next page, where you will see two buttons:
    - **Play Game**: This button allows you to play the game yourself.
    - **NEAT AI**: This button lets the NEAT algorithm learn and play the game.

### Gameplay

- **Player Mode**: Press the space bar to make your character fly. Avoid obstacles by navigating through the gaps. Try to achieve the highest score possible.

![Player playing the game](Play-Yourself.gif "Player Playing the Game")

- **AI Mode**: Watch the NEAT algorithm learn and master the game. The AI will start from scratch and improve over time by evolving and adapting to the game mechanics.

![NEAT AI playing the game](Play-AI.gif "NEAT AI Playing the Game")

## NEAT Algorithm

Flappy-Fly leverages the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to create an AI that can learn to play the game. NEAT is a genetic algorithm that evolves neural networks. It starts with a population of simple neural networks and evolves them over generations to improve their performance.

### How NEAT Works

1. **Initialization**: Start with a population of random neural networks.
2. **Evaluation**: Each network is evaluated based on its performance in the game.
3. **Selection**: The best-performing networks are selected to reproduce.
4. **Crossover**: Selected networks are combined to create offspring.
5. **Mutation**: Offspring networks are randomly mutated to introduce variability.
6. **Iteration**: Steps 2-5 are repeated for many generations until the AI achieves a high level of performance.

The NEAT algorithm allows the AI to autonomously learn and master the game, providing an interesting and educational experience for those interested in machine learning and AI.

## Contributing

Contributions are welcome! If you have any improvements or new features to add, feel free to open a pull request. Please ensure that your code follows the project's coding standards.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the original Flappy Bird game.
- Thanks to the Python community for their valuable resources and support.
- Special thanks to the developers of the NEAT algorithm for their contributions to AI and machine learning.

Enjoy the game and have fun!
