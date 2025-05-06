#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kerno.models.world import World
from kerno.models.player import Player
from kerno.models.actions import ActionHandler
from kerno.utils.game_io import GameIO
from kerno.utils.text_utils import TextFormatter
import sys

class GameEngine:
    def __init__(self, world_file):
        self.world = World(world_file)
        self.player = Player()
        self.action_handler = ActionHandler(self.world, self.player)
        self.io = GameIO()
        self.text_formatter = TextFormatter()
        self.running = True
        
    def initialize(self):
        """Initialize the game state, load starting room"""
        self.world.load()
        starting_room = self.world.get_starting_room()
        self.player.current_location = starting_room.id
        self.io.clear_screen()
        self.io.display_intro()
    
    def game_loop(self):
        """Main game loop"""
        self.initialize()
        
        while self.running:
            # Process world events for this turn
            events = self.world.process_events(self.player)
            for event in events:
                self.io.display_message(event)
            
            # Display current room description
            current_room = self.world.get_room(self.player.current_location)
            room_desc = self.text_formatter.format_room_description(current_room, self.player)
            self.io.display_message(room_desc)
            
            # Get available actions and display prompt
            available_actions = self.action_handler.get_available_actions()
            self.io.display_prompt(available_actions)
            
            # Get player input
            user_input = self.io.get_input()
            
            # Process player action
            result = self.action_handler.process_action(user_input)
            self.io.display_message(result.message)
            
            # Check if action was to quit
            if result.action_type == "quit":
                self.running = False
    
    def cleanup(self):
        """Clean up resources before exiting"""
        self.io.display_message("Dankon pro ludado! Ĝis revido!")  # Thank you for playing! Goodbye!

if __name__ == "__main__":
    world_file = "data/tutorial_world.json"
    
    # Allow command line argument to specify world file
    if len(sys.argv) > 1:
        world_file = sys.argv[1]
    
    game = GameEngine(world_file)
    
    try:
        game.game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    finally:
        game.cleanup() 