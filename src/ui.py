"""
UI module for handling the game's user interface
"""
import pygame
import os

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
        
        # Load images
        self.load_images()
        
        # UI element dimensions
        self.left_column_width = int(self.config.width * 0.7)
        self.right_column_width = self.config.width - self.left_column_width
        
        # Left column elements
        self.biome_height = int(self.config.height * 0.3)
        self.textlog_height = int(self.config.height * 0.6)  # Increased text log area
        self.command_height = int(self.config.height * 0.1)  # Reduced command area to fit 2 lines
        
        # Command input area dimensions
        self.input_width = int(self.left_column_width * 0.6)  # 60% of left column for input
        self.help_button_width = int(self.left_column_width * 0.2)  # 20% for help button
        self.execute_button_width = self.left_column_width - self.input_width - self.help_button_width  # Remaining space for execute button
        
        # UI elements and their positions
        self.biome_rect = pygame.Rect(0, 0, self.left_column_width, self.biome_height)
        self.textlog_rect = pygame.Rect(0, self.biome_height, self.left_column_width, self.textlog_height)
        self.command_rect = pygame.Rect(0, self.biome_height + self.textlog_height, self.input_width, self.command_height)
        self.help_button_rect = pygame.Rect(self.input_width, self.biome_height + self.textlog_height, self.help_button_width, self.command_height)
        self.execute_button_rect = pygame.Rect(self.input_width + self.help_button_width, self.biome_height + self.textlog_height, self.execute_button_width, self.command_height)
        self.inventory_rect = pygame.Rect(self.left_column_width, 0, self.right_column_width, self.config.height)
        
        # UI state variables
        self.show_map = False
        self.text_log = []
        self.text_log_offset = 0  # For scrolling
        self.command_text = ""
        self.show_help = False
        self.execute_hover = False  # For button highlighting
        self.help_hover = False  # For help button highlighting
        
        # Help text
        self.help_text = [
            "Verbi:",
            "  Irar [direktione] - Movar a lokaciono",
            "  Regardar - Regardar cirkumajo",
            "  Examinar [objekto] - Examinar objekto",
            "  Prendar [objekto] - Prendar objekto",
            "  Uzar [objekto] - Uzar objekto",
            "",
            "Direktioni:",
            "  norde, sude, este, weste",
            "",
            "Exempli:",
            "  Irar norde",
            "  Examinar mapo",
            "  Prendar klavo",
            "  Uzar klavo"
        ]
        
        # Action buttons for dropdown
        self.action_buttons = []
        
        # Inventory items (example)
        self.inventory_items = []
        
        # Initialize scrollbars
        self.textlog_scrollbar = ScrollBar(
            self.textlog_rect.right - 20, 
            self.textlog_rect.top, 
            20, 
            self.textlog_rect.height
        )
        self.inventory_scrollbar = ScrollBar(
            self.inventory_rect.right - 20, 
            self.inventory_rect.top, 
            20, 
            self.inventory_rect.height
        )
        
        # Initialize log file
        self.log_file = "game_log.txt"
        self.initialize_log_file()
        
        # Initialize with map in inventory
        self.add_map_to_inventory()
    
    def initialize_log_file(self):
        """Initialize or clear the log file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("KERNO\n\n")
    
    def add_to_text_log(self, text):
        """Add text to the text log file"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(text + "\n")
        
        # Update the in-memory log for display
        self._update_text_log_from_file()
    
    def _update_text_log_from_file(self):
        """Update the in-memory log from the file"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.text_log = f.readlines()
                # Remove empty lines and strip newlines
                self.text_log = [line.strip() for line in self.text_log if line.strip()]
        except FileNotFoundError:
            self.text_log = []
    
    def add_map_to_inventory(self):
        """Add map to inventory as an initial item"""
        map_item = {
            'name': 'Mapo',
            'description': 'Mapo de la instalação',
            'icon': self.placeholder,
            'amount': 1
        }
        self.inventory_items.append(map_item)
    
    def load_images(self):
        """Load UI images"""
        img_dir = os.path.join('src', 'assets', 'images')
        
        self.biome_bg = self.load_image(os.path.join(img_dir, 'biome_bg.png'))
        self.textlog_bg = self.load_image(os.path.join(img_dir, 'textlog_bg.png'))
        self.command_bg = self.load_image(os.path.join(img_dir, 'command_bg.png'))
        self.inventory_item_bg = self.load_image(os.path.join(img_dir, 'inventory_item_bg.png'))
        self.map_bg = self.load_image(os.path.join(img_dir, 'map_bg.png'))
        self.red_x = self.load_image(os.path.join(img_dir, 'red_x.png'))
        self.placeholder = self.load_image(os.path.join(img_dir, 'placeholder.png'))
    
    def load_image(self, path):
        """Load an image and scale it if needed"""
        try:
            image = pygame.image.load(path)
            return image
        except pygame.error:
            print(f"Could not load image {path}")
            # Create a colored surface as a placeholder
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((150, 150, 150))
            return placeholder
    
    def update_actions(self, actions):
        """Update available action buttons"""
        self.dropdown_options = actions
    
    def execute_command(self, action_manager):
        """Execute the current command"""
        if self.command_text:
            # Check if command matches any action name
            for action in action_manager.get_actions():
                if self.command_text.lower() == action.name.lower():  # Compare in lowercase
                    # Execute the action and clear the command
                    action.execute()
                    self.command_text = ""
                    return True
            
            # If no action matches, check if it's a speak command
            if self.command_text.lower().startswith("paroli "):
                text = self.command_text[7:]  # Remove "paroli " prefix
                self.add_to_text_log(f"Vi parolas: {text}")
                self.command_text = ""  # Clear command
                return True
            
            # If no action matches and not a speak command, show error
            self.add_to_text_log(f"Nevalida komando: {self.command_text}")
            self.command_text = ""  # Clear command
            return True
        return False
    
    def handle_click(self, pos, action_manager):
        """Handle click on UI elements"""
        # Check if map view is active
        if self.show_map:
            # Check if close button was clicked
            close_btn_rect = pygame.Rect(
                self.config.width - 50, 10, 40, 40
            )
            if close_btn_rect.collidepoint(pos):
                self.show_map = False
                return True
            return False
        
        # Check if help is shown and close button was clicked
        if self.show_help:
            close_btn_rect = pygame.Rect(self.config.width - 50, 10, 40, 40)
            if close_btn_rect.collidepoint(pos):
                self.show_help = False
                return True
        
        # Check if help button was clicked
        if self.help_button_rect.collidepoint(pos):
            self.show_help = not self.show_help
            return True
        
        # Check if execute button was clicked
        if self.execute_button_rect.collidepoint(pos):
            return self.execute_command(action_manager)
        
        # Check if an inventory item was clicked
        if self.inventory_rect.collidepoint(pos):
            # Check if inventory scrollbar was clicked
            if self.inventory_scrollbar.handle_click(pos):
                return True
            
            # Inventory items are now just informational
            return True
        
        # Check if text log scrollbar was clicked
        if self.textlog_scrollbar.handle_click(pos):
            self.text_log_offset = int(self.textlog_scrollbar.get_scroll_percentage() * 
                                      max(0, len(self.text_log) - self.textlog_rect.height // (self.config.font_size + 5)))
            return True
        
        # Check if command input was clicked
        if self.command_rect.collidepoint(pos):
            return True
        
        return False
    
    def handle_mouse_move(self, pos):
        """Handle mouse movement for button highlighting"""
        self.execute_hover = self.execute_button_rect.collidepoint(pos)
        self.help_hover = self.help_button_rect.collidepoint(pos)
    
    def handle_key(self, key, action_manager):
        """Handle key presses for command input"""
        if key == pygame.K_BACKSPACE:
            self.command_text = self.command_text[:-1]
        elif key <= 127:  # ASCII characters only
            self.command_text += chr(key)
        return None
    
    def draw(self, player, map_obj, current_text):
        """Draw the UI elements"""
        if self.show_map:
            self._draw_map_screen(map_obj, player)
        else:
            self._draw_main_interface(player, map_obj, current_text)
    
    def _draw_main_interface(self, player, map_obj, current_text):
        """Draw the main game interface"""
        # Draw biome section
        self._draw_biome_area(player)
        
        # Draw text log section
        self._draw_text_log()
        
        # Draw command section
        self._draw_command_area()
        
        # Draw help button
        self._draw_help_button()
        
        # Draw execute button
        self._draw_execute_button()
        
        # Draw inventory section
        self._draw_inventory(player)
        
        # Draw help text if help is shown
        if self.show_help:
            self._draw_help_text()
    
    def _draw_biome_area(self, player):
        """Draw the biome area with an image representing the current location"""
        # Scale image to fit
        scaled_bg = pygame.transform.scale(self.biome_bg, (self.biome_rect.width, self.biome_rect.height))
        self.screen.blit(scaled_bg, self.biome_rect)
        
        # Draw biome title
        location_name = "Unknown"
        if hasattr(player, 'position') and player.position:
            location_name = player.position.capitalize()
        
        title = self.title_font.render(location_name, True, self.config.WHITE)
        self.screen.blit(title, (self.biome_rect.left + 10, self.biome_rect.top + 10))
    
    def _draw_text_log(self):
        """Draw the text log with scrollbar"""
        # Scale background
        scaled_bg = pygame.transform.scale(self.textlog_bg, (self.textlog_rect.width, self.textlog_rect.height))
        self.screen.blit(scaled_bg, self.textlog_rect)
        
        # Draw title
        title = self.title_font.render("Log", True, self.config.WHITE)
        self.screen.blit(title, (self.textlog_rect.left + 10, self.textlog_rect.top + 10))
        
        # Draw text with scrolling
        line_height = self.config.font_size + 5
        max_visible_lines = (self.textlog_rect.height - 40) // line_height
        total_lines = len(self.text_log)
        
        # Update scrollbar
        self.textlog_scrollbar.update(total_lines, max_visible_lines)
        
        # Calculate max width for text (accounting for padding and scrollbar)
        max_width = self.textlog_rect.width - 40  # 20px padding on each side
        
        # Draw visible text lines with wrapping
        y_offset = self.textlog_rect.top + 40
        visible_lines = 0
        
        for i in range(self.text_log_offset, total_lines):
            if visible_lines >= max_visible_lines:
                break
                
            line = self.text_log[i]
            words = line.split()
            current_line = ""
            
            for word in words:
                # Test if adding the word would exceed the width
                test_line = current_line + " " + word if current_line else word
                test_surface = self.font.render(test_line, True, self.config.WHITE)
                
                if test_surface.get_width() <= max_width:
                    current_line = test_line
                else:
                    # Draw current line and start new one
                    if current_line:
                        text_surface = self.font.render(current_line, True, self.config.WHITE)
                        self.screen.blit(text_surface, (self.textlog_rect.left + 10, y_offset))
                        y_offset += line_height
                        visible_lines += 1
                        if visible_lines >= max_visible_lines:
                            break
                    current_line = word
            
            # Draw the last line
            if current_line and visible_lines < max_visible_lines:
                text_surface = self.font.render(current_line, True, self.config.WHITE)
                self.screen.blit(text_surface, (self.textlog_rect.left + 10, y_offset))
                y_offset += line_height
                visible_lines += 1
        
        # Draw scrollbar
        self.textlog_scrollbar.draw(self.screen, self.config)
    
    def _draw_command_area(self):
        """Draw the command input area"""
        # Scale background
        scaled_bg = pygame.transform.scale(self.command_bg, (self.command_rect.width, self.command_rect.height))
        self.screen.blit(scaled_bg, self.command_rect)
        
        # Draw command prompt
        prompt_text = ">> " + self.command_text
        prompt_surface = self.font.render(prompt_text, True, self.config.WHITE)
        self.screen.blit(prompt_surface, (self.command_rect.left + 10, self.command_rect.top + 10))
    
    def _draw_help_button(self):
        """Draw the help button"""
        # Button background
        button_color = self.config.DARK_BLUE if not self.help_hover else self.config.GREEN
        pygame.draw.rect(self.screen, button_color, self.help_button_rect)
        pygame.draw.rect(self.screen, self.config.WHITE, self.help_button_rect, 1)
        
        # Button text
        button_text = self.font.render("Helpo", True, self.config.WHITE)
        text_rect = button_text.get_rect(center=self.help_button_rect.center)
        self.screen.blit(button_text, text_rect)
    
    def _draw_execute_button(self):
        """Draw the execute button"""
        # Button background
        button_color = self.config.BLUE if not self.execute_hover else self.config.GREEN
        pygame.draw.rect(self.screen, button_color, self.execute_button_rect)
        pygame.draw.rect(self.screen, self.config.WHITE, self.execute_button_rect, 1)
        
        # Button text
        button_text = self.font.render("Exekutar", True, self.config.WHITE)
        text_rect = button_text.get_rect(center=self.execute_button_rect.center)
        self.screen.blit(button_text, text_rect)
    
    def _draw_help_text(self):
        """Draw the help text overlay"""
        # Create a semi-transparent background
        overlay = pygame.Surface((self.config.width, self.config.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw help text
        line_height = self.config.font_size + 5
        y_offset = 50
        
        for line in self.help_text:
            text_surface = self.font.render(line, True, self.config.WHITE)
            self.screen.blit(text_surface, (50, y_offset))
            y_offset += line_height
        
        # Draw close button
        close_btn_rect = pygame.Rect(self.config.width - 50, 10, 40, 40)
        scaled_x = pygame.transform.scale(self.red_x, (40, 40))
        self.screen.blit(scaled_x, close_btn_rect)
    
    def _draw_inventory(self, player):
        """Draw the inventory with scrollbar"""
        # Scale background to fit
        scaled_bg = pygame.transform.scale(self.inventory_item_bg, (self.inventory_rect.width, self.inventory_rect.height))
        self.screen.blit(scaled_bg, self.inventory_rect)
        
        # Draw title
        title = self.title_font.render("Inventaro", True, self.config.WHITE)
        self.screen.blit(title, (self.inventory_rect.left + 10, self.inventory_rect.top + 10))
        
        # Update inventory items from player if changed
        if player.inventory != self.inventory_items:
            # Make a copy to avoid reference issues
            self.inventory_items = []
            for item in player.inventory:
                self.inventory_items.append(item.copy() if isinstance(item, dict) else item)
            
            # Always ensure map is in inventory
            map_in_inventory = any(item.get('name', '').lower() == 'map' for item in self.inventory_items)
            if not map_in_inventory:
                self.add_map_to_inventory()
        
        # Draw items with scrolling
        item_height = 60
        visible_height = self.inventory_rect.height - 50  # Adjust for title
        max_visible_items = visible_height // item_height
        total_items = len(self.inventory_items)
        
        # Update scrollbar
        self.inventory_scrollbar.update(total_items, max_visible_items)
        
        # Draw visible items
        y_offset = self.inventory_rect.top + 50
        for i in range(min(total_items, max_visible_items)):
            adjusted_idx = i + int(self.inventory_scrollbar.scroll_pos / item_height)
            if adjusted_idx >= total_items:
                break
                
            item = self.inventory_items[adjusted_idx]
            item_rect = pygame.Rect(
                self.inventory_rect.left + 10,
                y_offset,
                self.inventory_rect.width - 30,
                item_height - 5
            )
            
            # Draw item background
            scaled_item_bg = pygame.transform.scale(
                self.inventory_item_bg, 
                (item_rect.width, item_rect.height)
            )
            self.screen.blit(scaled_item_bg, item_rect)
            
            # Draw item icon
            icon = item.get('icon', self.placeholder)
            scaled_icon = pygame.transform.scale(icon, (50, 50))
            self.screen.blit(scaled_icon, (item_rect.left + 5, item_rect.top + 5))
            
            # Draw item name
            name_text = self.font.render(item.get('name', 'Unknown'), True, self.config.WHITE)
            self.screen.blit(name_text, (item_rect.left + 60, item_rect.top + 5))
            
            # Draw item amount
            amount_text = self.font.render(f"x{item.get('amount', 1)}", True, self.config.WHITE)
            self.screen.blit(amount_text, (item_rect.left + 60, item_rect.top + 25))
            
            y_offset += item_height
        
        # Draw scrollbar
        self.inventory_scrollbar.draw(self.screen, self.config)
    
    def _draw_map_screen(self, map_obj, player):
        """Draw the fullscreen map"""
        # Scale map background to fill screen
        scaled_map_bg = pygame.transform.scale(self.map_bg, (self.config.width, self.config.height))
        self.screen.blit(scaled_map_bg, (0, 0))
        
        # Draw actual map
        self._draw_map_content(map_obj, player)
        
        # Draw close button (X)
        close_btn_rect = pygame.Rect(self.config.width - 50, 10, 40, 40)
        scaled_x = pygame.transform.scale(self.red_x, (40, 40))
        self.screen.blit(scaled_x, close_btn_rect)
    
    def _draw_map_content(self, map_obj, player):
        """Draw the actual map content"""
        # This is similar to the original _draw_map but centered on screen
        grid_size = 40  # Larger for the full screen view
        
        # Find map dimensions
        map_width = len(map_obj.current_map[0]) if map_obj.current_map and map_obj.current_map[0] else 0
        map_height = len(map_obj.current_map) if map_obj.current_map else 0
        
        total_width = map_width * grid_size
        total_height = map_height * grid_size
        
        offset_x = (self.config.width - total_width) // 2
        offset_y = (self.config.height - total_height) // 2
        
        # Draw grid title
        title = self.title_font.render("Mapo", True, self.config.WHITE)
        self.screen.blit(title, (offset_x, offset_y - 30))
        
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
                        # Draw room name
                        room_name = location.name[:8]  # Truncate if too long
                        name_surface = self.font.render(room_name, True, self.config.WHITE)
                        name_rect = name_surface.get_rect(center=rect.center)
                        self.screen.blit(name_surface, name_rect)
                        
                        # Draw doors/exits
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


class ScrollBar:
    """A simple scrollbar class"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_pos = 0
        self.total_items = 0
        self.visible_items = 0
        self.dragging = False
        self.drag_start_y = 0
    
    def update(self, total_items, visible_items):
        """Update scrollbar with new data"""
        self.total_items = max(1, total_items)
        self.visible_items = min(visible_items, total_items)
    
    def handle_click(self, pos):
        """Handle click on scrollbar"""
        scrollbar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if scrollbar_rect.collidepoint(pos):
            # Calculate handle position
            handle_height = self.get_handle_height()
            handle_y = self.y + self.get_handle_y_offset()
            handle_rect = pygame.Rect(self.x, handle_y, self.width, handle_height)
            
            if handle_rect.collidepoint(pos):
                # Start dragging
                self.dragging = True
                self.drag_start_y = pos[1] - handle_y
            else:
                # Jump to position
                click_percentage = (pos[1] - self.y) / self.height
                self.scroll_pos = click_percentage * (self.total_items - self.visible_items) * 20
                self.scroll_pos = max(0, min(self.scroll_pos, (self.total_items - self.visible_items) * 20))
            
            return True
        return False
    
    def handle_drag(self, pos):
        """Handle dragging the scrollbar"""
        if self.dragging:
            # Calculate new position
            new_handle_y = pos[1] - self.drag_start_y
            percentage = (new_handle_y - self.y) / (self.height - self.get_handle_height())
            self.scroll_pos = percentage * (self.total_items - self.visible_items) * 20
            self.scroll_pos = max(0, min(self.scroll_pos, (self.total_items - self.visible_items) * 20))
    
    def handle_release(self):
        """Handle release of mouse button"""
        self.dragging = False
    
    def get_handle_height(self):
        """Calculate handle height based on visible/total ratio"""
        ratio = self.visible_items / self.total_items
        return max(20, self.height * ratio)
    
    def get_handle_y_offset(self):
        """Calculate handle y offset based on scroll position"""
        max_offset = self.height - self.get_handle_height()
        return max_offset * self.get_scroll_percentage()
    
    def get_scroll_percentage(self):
        """Get current scroll percentage"""
        if self.total_items <= self.visible_items:
            return 0
        return self.scroll_pos / ((self.total_items - self.visible_items) * 20)
    
    def draw(self, screen, config):
        """Draw the scrollbar"""
        # Draw scrollbar background
        scrollbar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, config.DARK_GRAY, scrollbar_rect)
        
        # Draw handle
        handle_height = self.get_handle_height()
        handle_y = self.y + self.get_handle_y_offset()
        handle_rect = pygame.Rect(self.x, handle_y, self.width, handle_height)
        pygame.draw.rect(screen, config.GRAY, handle_rect)
        pygame.draw.rect(screen, config.WHITE, handle_rect, 1) 