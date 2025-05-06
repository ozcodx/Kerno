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
        self.drag_active = False
        
        # Initialize starting point
        self.initialize_game()
    
    def initialize_game(self):
        """Set up the initial game state"""
        # Set player position to starting location
        starting_location_id = self.map.get_starting_location()
        self.player.position = starting_location_id
        self.current_location = starting_location_id
        
        # Get the actual location object and set the initial text
        starting_location = self.map.get_location(starting_location_id)
        if starting_location:
            self.current_text = self.get_location_description(starting_location)
            # Add initial text to log only once
            self.ui.add_to_text_log(self.current_text)
        else:
            self.current_text = "Error: Location not found."
        
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
        self.action_manager.add_action("Mapo", self.show_map)
        
        # Add context-specific actions
        location = self.map.get_location(self.player.position)
        if location and location.items:
            for item in location.items:
                self.action_manager.add_action(f"Examinar {item.name}", self.examine_item, item)
                
                # Add pickup action if item can be picked up
                if hasattr(item, 'can_pick_up') and item.can_pick_up:
                    self.action_manager.add_action(f"Prendar {item.name}", self.pickup_item, item)
                
                # Add use action if item can be used
                if hasattr(item, 'can_use') and item.can_use:
                    self.action_manager.add_action(f"Uzar {item.name}", self.use_item, item)
        
        # Update UI
        self.ui.update_actions(self.action_manager.get_actions())
    
    def move_player(self, direction):
        """Move the player in the specified direction"""
        new_position_id = self.map.get_adjacent_location(self.player.position, direction)
        if new_position_id:
            self.player.position = new_position_id
            self.current_location = new_position_id
            
            # Get location description
            location = self.map.get_location(new_position_id)
            if location:
                self.current_text = self.get_location_description(location)
                self.ui.add_to_text_log(self.current_text)
            else:
                self.current_text = "Error: Location not found."
                self.ui.add_to_text_log(self.current_text)
                
            self.update_available_actions()
    
    def look_around(self):
        """Look around the current location"""
        location = self.map.get_location(self.player.position)
        if location:
            items_desc = ", ".join([item.name for item in location.items]) if location.items else "nenio speciala"
            self.current_text = f"{self.get_location_description(location)}\nVi vidas: {items_desc}"
            # Only add to log if the text is different from the last entry
            if not self.ui.text_log or self.current_text != self.ui.text_log[-1]:
                self.ui.add_to_text_log(self.current_text)
        else:
            self.current_text = "Error: Location not found."
            if not self.ui.text_log or self.current_text != self.ui.text_log[-1]:
                self.ui.add_to_text_log(self.current_text)
    
    def examine_item(self, item):
        """Examine an item in the current location"""
        self.current_text = f"Vi examenas {item.name}. {item.description}"
        self.ui.add_to_text_log(self.current_text)
    
    def pickup_item(self, item):
        """Pick up an item and add it to inventory"""
        location = self.map.get_location(self.player.position)
        if location and item in location.items:
            # Convert to a simple dict format for inventory
            inventory_item = {
                'name': item.name,
                'description': item.description,
                'icon': None,  # Will be set to placeholder in UI
                'amount': 1
            }
            
            # Add to player inventoryl
            self.player.add_to_inventory(inventory_item)
            
            # Remove from location
            location.items.remove(item)
            
            # Update text
            self.current_text = f"Vi prendas {item.name}."
            self.ui.add_to_text_log(self.current_text)
            
            # Update actions
            self.update_available_actions()
    
    def show_map(self):
        """Show the map"""
        self.ui.show_map = True
        self.current_text = "Vi uzas la mapo."
        self.ui.add_to_text_log(self.current_text)
    
    def use_item(self, item):
        """Use an item from inventory"""
        # Check if item is in inventory
        if any(inv_item.get('name', '').lower() == item.name.lower() for inv_item in self.player.inventory):
            if item.name.lower() == 'mapo':
                self.ui.show_map = True
                self.current_text = "Vi uzas la mapo."
                self.ui.add_to_text_log(self.current_text)
            else:
                self.current_text = f"Vi uzas {item.name}. {item.use_description}"
                self.ui.add_to_text_log(self.current_text)
        else:
            self.current_text = f"Vi ne havas {item.name} en vua inventaro."
            self.ui.add_to_text_log(self.current_text)
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.ui.show_map:
                        # Close map if open
                        self.ui.show_map = False
                    else:
                        self.running = False
                elif event.key == pygame.K_RETURN:
                    # Execute command on Enter
                    if self.ui.command_text:
                        self.ui.execute_command(self.action_manager)
                else:
                    # Pass keypresses to UI for command input
                    self.ui.handle_key(event.key, self.action_manager)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Handle UI clicks
                    if self.ui.handle_click(event.pos, self.action_manager):
                        # Start tracking drags for scrollbars
                        self.drag_active = True
                        self.drag_start_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    # Stop tracking drags
                    self.drag_active = False
                    
                    # Notify scrollbars of release
                    self.ui.textlog_scrollbar.handle_release()
                    self.ui.inventory_scrollbar.handle_release()
            
            elif event.type == pygame.MOUSEMOTION:
                # Update UI hover states
                self.ui.handle_mouse_move(event.pos)
                
                # Handle drag for scrollbars if active
                if self.drag_active:
                    self.ui.textlog_scrollbar.handle_drag(event.pos)
                    self.ui.inventory_scrollbar.handle_drag(event.pos)
    
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
    
    def handle_invalid_command(self, command):
        """Handle invalid commands"""
        self.current_text = f"Nevalida komando: {command}"
        self.ui.add_to_text_log(self.current_text) 