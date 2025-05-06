#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kerno: La Lasta Devo

Exekutez ica skripto por komencar la ludo.
"""

import sys
import argparse
from kerno.main import GameEngine

def main():
    """Main entry point for the game"""
    parser = argparse.ArgumentParser(description="Kerno: La Lasta Devo")
    parser.add_argument(
        "--world", 
        default="kerno/data/tutorial_world.json",
        help="La dosiero por la mondo charjar (original: tutorial_world.json)"
    )
    args = parser.parse_args()
    
    try:
        game = GameEngine(args.world)
        game.game_loop()
    except KeyboardInterrupt:
        print("\nLudo interrompita per uzanto.")
        return 1
    except Exception as e:
        print(f"Eroro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 