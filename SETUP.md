# Kerno - Setup Guide

## Requirements
- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd Kerno
```

2. Create a virtual environment (recommended):
```
python -m venv venv
```

3. Activate the virtual environment:

On Windows:
```
venv\Scripts\activate
```

On macOS/Linux:
```
source venv/bin/activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

## Running the Game

After installation, you can run the game with:
```
python main.py
```

## Controls

- **Mouse**: Click on action buttons to perform actions
- **ESC**: Exit the game

## Development Notes

- The game language is exclusively Ido, an auxiliary language created in 1907.
- The game currently supports the Technician profession, with more professions to be added later.
- The game is in early development (MVP) focusing on the basic map and movement systems.

## Features in Development

- Expanded map and locations
- Additional player professions (Botanist, Archivist, etc.)
- Free text input with parser in Ido
- Survival mode features (hunger, thirst, fatigue)
- Character interactions and dialogues with Kaliel 