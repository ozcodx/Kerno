"""
Main game module that handles the game loop and state
"""
import pygame
from src.map import Map
from src.player import Player
from src.ui import UI
from src.action_manager import ActionManager

class Game:
    """Main game class that handles the game loop and state"""
    
    def __init__(self, config):
        """Initialize the game with configuration"""
        self.config = config
        
        # Create the game window
        self.screen = pygame.display.set_mode(
            (self.config.width, self.config.height)
        )
        pygame.display.set_caption(self.config.title)
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.map = Map(self.config)
        self.player = Player(self.config)
        self.ui = UI(self.config, self.screen)
        self.action_manager = ActionManager(self.config)
        
        # Game state variables
        self.running = True
        self.game_stage = 1  # Stage 1: Daily Routine
        self.current_text = ""
        self.current_location = None
        
        # Initialize starting point
        self.initialize_game()
    
    def initialize_game(self):
        """Set up the initial game state"""
        # Set player position to starting location
        starting_location = self.map.get_starting_location()
        self.player.position = starting_location
        self.current_location = starting_location
        
        # Set initial game text
        self.current_text = self.get_location_description(starting_location)
        
        # Add initial actions
        self.update_available_actions()
    
    def get_location_description(self, location):
        """Get the description of the current location"""
        # This will be expanded with actual location data
        return f"Vi esas en {location.name}. {location.description}"
    
    def update_available_actions(self):
        """Update the available actions based on the current context"""
        # Clear previous actions
        self.action_manager.clear_actions()
        
        # Add basic movement actions based on available exits
        exits = self.map.get_exits(self.player.position)
        for direction, location in exits.items():
            self.action_manager.add_action(f"Irar {direction}", self.move_player, direction)
        
        # Add standard actions
        self.action_manager.add_action("Regardar", self.look_around)
        
        # Add context-specific actions
        location = self.map.get_location(self.player.position)
        for item in location.items:
            self.action_manager.add_action(f"Examinar {item.name}", self.examine_item, item)
        
        # Update UI
        self.ui.update_actions(self.action_manager.get_actions())
    
    def move_player(self, direction):
        """Move the player in the specified direction"""
        new_position = self.map.get_adjacent_location(self.player.position, direction)
        if new_position:
            self.player.position = new_position
            self.current_location = new_position
            self.current_text = self.get_location_description(new_position)
            self.update_available_actions()
    
    def look_around(self):
        """Look around the current location"""
        location = self.map.get_location(self.player.position)
        items_desc = ", ".join([item.name for item in location.items]) if location.items else "nenio speciala"
        self.current_text = f"{self.get_location_description(location)}\nVi vidas: {items_desc}"
    
    def examine_item(self, item):
        """Examine an item in the current location"""
        self.current_text = f"Vi examenas {item.name}. {item.description}"
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Add other key controls here
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.ui.handle_click(event.pos, self.action_manager)
    
    def update(self):
        """Update game state"""
        # Update game components
        self.player.update()
        self.map.update()
    
    def render(self):
        """Render the game screen"""
        # Clear the screen
        self.screen.fill(self.config.BLACK)
        
        # Draw UI components
        self.ui.draw(self.player, self.map, self.current_text)
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle input
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render the game
            self.render()
            
            # Control the game speed
            self.clock.tick(self.config.fps) 