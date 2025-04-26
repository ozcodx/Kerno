"""
UI module for handling the game's user interface
"""
import pygame

class UI:
    """UI class for handling the game's user interface"""
    
    def __init__(self, config, screen):
        """Initialize UI with configuration"""
        self.config = config
        self.screen = screen
        
        # Load fonts
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', self.config.font_size)
        self.title_font = pygame.font.SysFont('monospace', self.config.font_size + 4, bold=True)
        
        # UI elements and their positions
        self.map_rect = pygame.Rect(0, 0, self.config.map_width, self.config.map_height)
        self.text_rect = pygame.Rect(0, self.config.map_height, self.config.map_width, self.config.text_height)
        self.inventory_rect = pygame.Rect(self.config.map_width, 0, self.config.inventory_width, self.config.height - self.config.actions_height)
        self.actions_rect = pygame.Rect(self.config.map_width, self.config.height - self.config.actions_height, self.config.inventory_width, self.config.actions_height)
        
        # Button rects for action buttons
        self.action_buttons = []
    
    def update_actions(self, actions):
        """Update available action buttons"""
        self.action_buttons = []
        
        button_height = 30
        button_padding = 5
        button_width = self.config.inventory_width - 20
        
        # Create buttons for each action
        for i, action in enumerate(actions):
            y_pos = self.config.height - self.config.actions_height + button_padding + i * (button_height + button_padding)
            
            if y_pos + button_height < self.config.height - button_padding:
                button_rect = pygame.Rect(
                    self.config.map_width + 10,
                    y_pos,
                    button_width,
                    button_height
                )
                self.action_buttons.append((button_rect, action))
    
    def draw(self, player, map_obj, current_text):
        """Draw the UI elements"""
        # Draw map section
        pygame.draw.rect(self.screen, self.config.DARK_GRAY, self.map_rect)
        self._draw_map(map_obj, player)
        
        # Draw text section
        pygame.draw.rect(self.screen, self.config.GRAY, self.text_rect)
        self._draw_text_area(current_text)
        
        # Draw inventory section
        pygame.draw.rect(self.screen, self.config.DARK_GRAY, self.inventory_rect)
        self._draw_inventory(player)
        
        # Draw actions section
        pygame.draw.rect(self.screen, self.config.GRAY, self.actions_rect)
        self._draw_actions()
    
    def _draw_map(self, map_obj, player):
        """Draw the map"""
        # Draw grid
        grid_size = min(
            self.config.map_width // len(map_obj.current_map[0]) if map_obj.current_map[0] else self.config.tile_size,
            self.config.map_height // len(map_obj.current_map) if map_obj.current_map else self.config.tile_size
        )
        
        offset_x = (self.config.map_width - grid_size * len(map_obj.current_map[0])) // 2
        offset_y = (self.config.map_height - grid_size * len(map_obj.current_map)) // 2
        
        # Draw each cell
        for y, row in enumerate(map_obj.current_map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    offset_x + x * grid_size,
                    offset_y + y * grid_size,
                    grid_size, 
                    grid_size
                )
                
                # Draw cell
                if cell:
                    # Room exists
                    color = self.config.BLUE
                    # Highlight current location
                    if cell == player.position:
                        color = self.config.GREEN
                    
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, self.config.BLACK, rect, 1)
                    
                    # Draw connections/doors
                    location = map_obj.get_location(cell)
                    if location:
                        for direction in location.exits:
                            if direction == "norde":
                                pygame.draw.line(
                                    self.screen, 
                                    self.config.WHITE,
                                    (rect.centerx, rect.top),
                                    (rect.centerx, rect.top + grid_size//4)
                                )
                            elif direction == "sude":
                                pygame.draw.line(
                                    self.screen, 
                                    self.config.WHITE,
                                    (rect.centerx, rect.bottom),
                                    (rect.centerx, rect.bottom - grid_size//4)
                                )
                            elif direction == "este":
                                pygame.draw.line(
                                    self.screen, 
                                    self.config.WHITE,
                                    (rect.right, rect.centery),
                                    (rect.right - grid_size//4, rect.centery)
                                )
                            elif direction == "weste":
                                pygame.draw.line(
                                    self.screen, 
                                    self.config.WHITE,
                                    (rect.left, rect.centery),
                                    (rect.left + grid_size//4, rect.centery)
                                )
    
    def _draw_text_area(self, text):
        """Draw the text area with the current description"""
        # Draw title
        title = self.title_font.render("Deskriptio", True, self.config.BLACK)
        self.screen.blit(title, (10, self.config.map_height + 10))
        
        # Draw text with wrapping
        y_offset = self.config.map_height + 40
        max_width = self.config.map_width - 20
        
        for paragraph in text.split('\n'):
            # Wrap text into multiple lines if needed
            words = paragraph.split(' ')
            line = ''
            for word in words:
                test_line = line + word + ' '
                text_width, _ = self.font.size(test_line)
                
                if text_width > max_width:
                    text_surface = self.font.render(line, True, self.config.BLACK)
                    self.screen.blit(text_surface, (10, y_offset))
                    y_offset += self.config.font_size + 5
                    line = word + ' '
                else:
                    line = test_line
            
            if line:
                text_surface = self.font.render(line, True, self.config.BLACK)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += self.config.font_size + 15  # Extra space between paragraphs
    
    def _draw_inventory(self, player):
        """Draw the player's inventory"""
        # Draw title
        title = self.title_font.render("Inventaro", True, self.config.WHITE)
        self.screen.blit(title, (self.config.map_width + 10, 10))
        
        # Draw player info
        profession_text = f"Profesiono: {player.profession}"
        prof_surface = self.font.render(profession_text, True, self.config.WHITE)
        self.screen.blit(prof_surface, (self.config.map_width + 10, 40))
        
        # Draw inventory items
        y_offset = 80
        if player.inventory:
            for item in player.inventory:
                item_text = f"- {item.name}"
                item_surface = self.font.render(item_text, True, self.config.WHITE)
                self.screen.blit(item_surface, (self.config.map_width + 10, y_offset))
                y_offset += self.config.font_size + 5
        else:
            empty_text = "- (vakua)"
            empty_surface = self.font.render(empty_text, True, self.config.WHITE)
            self.screen.blit(empty_surface, (self.config.map_width + 10, y_offset))
        
        # Draw stats if enabled
        if hasattr(self.config, 'survival_mode') and self.config.survival_mode:
            self._draw_survival_stats(player, y_offset + 40)
    
    def _draw_survival_stats(self, player, y_offset):
        """Draw survival stats (hunger, thirst, fatigue)"""
        title = self.title_font.render("Fizikala Stato", True, self.config.WHITE)
        self.screen.blit(title, (self.config.map_width + 10, y_offset))
        
        # Draw hunger
        hunger_text = f"Famo: {int(player.hunger)}%"
        hunger_surface = self.font.render(hunger_text, True, self.config.WHITE)
        self.screen.blit(hunger_surface, (self.config.map_width + 10, y_offset + 30))
        
        # Draw thirst
        thirst_text = f"Soifo: {int(player.thirst)}%"
        thirst_surface = self.font.render(thirst_text, True, self.config.WHITE)
        self.screen.blit(thirst_surface, (self.config.map_width + 10, y_offset + 50))
        
        # Draw fatigue
        fatigue_text = f"Fatigeso: {int(player.fatigue)}%"
        fatigue_surface = self.font.render(fatigue_text, True, self.config.WHITE)
        self.screen.blit(fatigue_surface, (self.config.map_width + 10, y_offset + 70))
    
    def _draw_actions(self):
        """Draw action buttons"""
        # Draw title
        title = self.title_font.render("Aktioni", True, self.config.BLACK)
        self.screen.blit(title, (self.config.map_width + 10, self.config.height - self.config.actions_height + 10))
        
        # Draw buttons
        for button_rect, action in self.action_buttons:
            pygame.draw.rect(self.screen, self.config.BLUE, button_rect)
            pygame.draw.rect(self.screen, self.config.BLACK, button_rect, 1)
            
            button_text = self.font.render(action.name, True, self.config.WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
    
    def handle_click(self, pos, action_manager):
        """Handle click on UI elements"""
        # Check if an action button was clicked
        for button_rect, action in self.action_buttons:
            if button_rect.collidepoint(pos):
                # Execute the action
                action.execute()
                return True
        
        return False 