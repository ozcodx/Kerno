#!/usr/bin/env python3
"""
Kerno
Main entry point for the game
"""
import pygame
import sys
from src.game import Game
from src.config import Config

def main():
    """Main function to initialize and run the game"""
    # Initialize pygame
    pygame.init()
    
    # Load configuration
    config = Config()
    
    # Create game instance
    game = Game(config)
    
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