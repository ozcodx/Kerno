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
        self.textlog_height = int(self.config.height * 0.5)
        self.command_height = self.config.height - self.biome_height - self.textlog_height
        
        # UI elements and their positions
        self.biome_rect = pygame.Rect(0, 0, self.left_column_width, self.biome_height)
        self.textlog_rect = pygame.Rect(0, self.biome_height, self.left_column_width, self.textlog_height)
        self.command_rect = pygame.Rect(0, self.biome_height + self.textlog_height, self.left_column_width, self.command_height)
        self.inventory_rect = pygame.Rect(self.left_column_width, 0, self.right_column_width, self.config.height)
        
        # UI state variables
        self.show_map = False
        self.text_log = []
        self.text_log_offset = 0  # For scrolling
        self.command_text = ""
        self.dropdown_open = False
        self.dropdown_options = []
        
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
    
    def add_to_text_log(self, text):
        """Add text to the text log"""
        # Split text into lines that fit in the text log width
        available_width = self.textlog_rect.width - 40  # Adjust for padding and scrollbar
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width, _ = self.font.size(test_line)
            
            if text_width < available_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Add to the log
        self.text_log.extend(lines)
        
        # Scroll to bottom
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll text log to the bottom"""
        max_visible_lines = self.textlog_rect.height // (self.config.font_size + 5)
        if len(self.text_log) > max_visible_lines:
            self.text_log_offset = len(self.text_log) - max_visible_lines
        else:
            self.text_log_offset = 0
    
    def update_actions(self, actions):
        """Update available action buttons"""
        self.dropdown_options = actions
    
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
        
        # Check if an inventory item was clicked
        if self.inventory_rect.collidepoint(pos):
            item_height = 60
            item_y = self.inventory_rect.top
            
            for i, item in enumerate(self.inventory_items):
                item_rect = pygame.Rect(
                    self.inventory_rect.left + 10,
                    item_y + i * item_height - self.inventory_scrollbar.scroll_pos,
                    self.inventory_rect.width - 30,
                    item_height
                )
                
                if item_rect.collidepoint(pos):
                    # Special case for map
                    if item.get('name', '').lower() == 'map':
                        self.show_map = True
                    return True
            
            # Check if inventory scrollbar was clicked
            if self.inventory_scrollbar.handle_click(pos):
                return True
        
        # Check if text log scrollbar was clicked
        if self.textlog_scrollbar.handle_click(pos):
            self.text_log_offset = int(self.textlog_scrollbar.get_scroll_percentage() * 
                                      max(0, len(self.text_log) - self.textlog_rect.height // (self.config.font_size + 5)))
            return True
        
        # Check if dropdown is open and an option was clicked
        if self.dropdown_open:
            dropdown_height = len(self.dropdown_options) * 30
            dropdown_rect = pygame.Rect(
                10, 
                self.command_rect.top - dropdown_height,
                self.left_column_width - 20,
                dropdown_height
            )
            
            if dropdown_rect.collidepoint(pos):
                # Calculate which option was clicked
                option_idx = (pos[1] - dropdown_rect.top) // 30
                if 0 <= option_idx < len(self.dropdown_options):
                    action = self.dropdown_options[option_idx]
                    action.execute()
                    self.dropdown_open = False
                    return True
            else:
                # Close dropdown if clicked outside
                self.dropdown_open = False
                return True
        
        # Check if command input was clicked
        if self.command_rect.collidepoint(pos):
            # Toggle dropdown
            self.dropdown_open = not self.dropdown_open
            return True
        
        return False
    
    def handle_key(self, key):
        """Handle key presses for command input"""
        if key == pygame.K_BACKSPACE:
            self.command_text = self.command_text[:-1]
        elif key == pygame.K_RETURN:
            if self.command_text:
                # Process command
                command = self.command_text
                self.command_text = ""
                return command
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
        # Update text log if there's new text
        if current_text and (not self.text_log or current_text != self.text_log[-1]):
            self.add_to_text_log(current_text)
        
        # Draw biome section
        self._draw_biome_area(player)
        
        # Draw text log section
        self._draw_text_log()
        
        # Draw command section
        self._draw_command_area()
        
        # Draw inventory section
        self._draw_inventory(player)
        
        # Draw dropdown if open
        if self.dropdown_open:
            self._draw_dropdown()
    
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
        
        # Draw visible text lines
        y_offset = self.textlog_rect.top + 40
        for i in range(self.text_log_offset, min(self.text_log_offset + max_visible_lines, total_lines)):
            line = self.text_log[i]
            text_surface = self.font.render(line, True, self.config.WHITE)
            self.screen.blit(text_surface, (self.textlog_rect.left + 10, y_offset))
            y_offset += line_height
        
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
        
        # Draw dropdown indicator
        indicator = "▼" if not self.dropdown_open else "▲"
        indicator_surface = self.font.render(indicator, True, self.config.WHITE)
        self.screen.blit(indicator_surface, (self.command_rect.right - 30, self.command_rect.top + 10))
    
    def _draw_dropdown(self):
        """Draw the command dropdown menu"""
        dropdown_height = len(self.dropdown_options) * 30
        dropdown_rect = pygame.Rect(
            10, 
            self.command_rect.top - dropdown_height,
            self.left_column_width - 20,
            dropdown_height
        )
        
        # Draw dropdown background
        pygame.draw.rect(self.screen, self.config.DARK_GRAY, dropdown_rect)
        pygame.draw.rect(self.screen, self.config.WHITE, dropdown_rect, 1)
        
        # Draw options
        for i, action in enumerate(self.dropdown_options):
            option_rect = pygame.Rect(
                dropdown_rect.left,
                dropdown_rect.top + i * 30,
                dropdown_rect.width,
                30
            )
            
            # Highlight on hover (if we were tracking mouse position)
            pygame.draw.rect(self.screen, self.config.GRAY, option_rect)
            
            # Draw option text
            option_text = self.font.render(action.name, True, self.config.WHITE)
            self.screen.blit(option_text, (option_rect.left + 10, option_rect.top + 5))
    
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
            self.inventory_items = player.inventory.copy()
            # Always ensure map is in inventory for demo
            map_in_inventory = any(item.get('name', '').lower() == 'map' for item in self.inventory_items)
            if not map_in_inventory:
                self.inventory_items.append({'name': 'Map', 'icon': self.placeholder, 'amount': 1})
        
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