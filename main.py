#!/usr/bin/env python3
"""
Kerno
Main entry point for the game
"""
import pygame
import sys
import os
from src.game import Game
from src.config import Config

def main():
    """Main function to initialize and run the game"""
    print("Starting Kerno...")
    
    # Check required directories
    for directory in ['src/assets/images', 'src/assets/fonts', 'src/assets/sounds']:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory {directory}")
    
    # Initialize pygame
    pygame.init()
    print("Pygame initialized correctly")
    
    # Load configuration
    config = Config()
    print("Configuration loaded")
    
    # Create game instance
    print("Creating game world...")
    game = Game(config)
    print("Game world created")
    
    print("Ready to play!")
    print("Use ESC to exit")
    
    try:
        # Run the game loop
        game.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main() 