"""
Configuration module for the game
"""

class Config:
    """Configuration class that holds game settings"""
    
    def __init__(self):
        # Window settings
        self.title = "Kerno"
        self.width = 1024
        self.height = 768
        self.fps = 60
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.DARK_GRAY = (50, 50, 50)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        
        # Game settings
        self.tile_size = 32
        self.font_size = 18
        self.lang = "ido"
        self.survival_mode = False  # Set to True to enable survival features
        
        # UI layout settings
        self.map_width = int(self.width * 0.6)
        self.map_height = int(self.height * 0.6)
        self.text_height = int(self.height * 0.3)
        self.inventory_width = int(self.width * 0.4)
        self.actions_height = int(self.height * 0.1)
        
        # Player settings
        self.player_profession = "technician"  # Default profession
        
        # Debug settings
        self.debug = True 