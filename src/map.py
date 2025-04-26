"""
Map module for handling game locations and navigation
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

@dataclass
class Item:
    """Class representing an item in the game world"""
    name: str
    description: str
    can_pick_up: bool = False
    required_skill: Optional[str] = None
    required_skill_level: int = 0
    interactions: Dict[str, str] = field(default_factory=dict)

@dataclass
class Location:
    """Class representing a location in the game world"""
    id: str
    name: str
    description: str
    x: int
    y: int
    items: List[Item] = field(default_factory=list)
    exits: Dict[str, str] = field(default_factory=dict)
    accessible_by: List[str] = field(default_factory=lambda: ["all"])

class Map:
    """Map class for managing game locations and player movement"""
    
    def __init__(self, config):
        """Initialize the map with configuration"""
        self.config = config
        self.locations = {}
        self.current_map = []
        
        # Initialize map with starting locations
        self._initialize_map()
    
    def _initialize_map(self):
        """Initialize the map with starting locations"""
        # Create initial locations for the technician's work area
        
        # Control Room - Starting location
        control_room = Location(
            id="control_room",
            name="Kontrolo-Chambro",
            description="La centrala kontrolo-chambro. Luminizita ekrani kovras la muroj. Diversa butoni e indikili blinkigas.",
            x=5,
            y=5,
            items=[
                Item(
                    name="kontrolo-panelo",
                    description="Un granda kontrolo-panelo kun multa butoni e indikili.",
                    can_pick_up=False,
                    interactions={"uzi": "Vi presas kelka butoni, ma nulleso chanjas."}
                ),
                Item(
                    name="kafeo-taso",
                    description="Un varma taso di kafeo.",
                    can_pick_up=True
                )
            ],
            exits={
                "norde": "hall",
                "este": "server_room",
                "weste": "maintenance"
            }
        )
        
        # Maintenance Room
        maintenance = Location(
            id="maintenance",
            name="Mantenado-Chambro",
            description="Un chambro plena di utensili e peci di ekipajo.",
            x=4,
            y=5,
            items=[
                Item(
                    name="utensilo-kesto",
                    description="Un kesto di utensili por reparar la ekipajo.",
                    can_pick_up=False,
                    required_skill="technical",
                    required_skill_level=1,
                    interactions={"uzi": "Vi trovas un utila utensilo."}
                )
            ],
            exits={
                "este": "control_room"
            }
        )
        
        # Server Room
        server_room = Location(
            id="server_room",
            name="Servilo-Chambro",
            description="Un chambro plena di altaj servilo-kabineti. La sono di ventili esas konstanta.",
            x=6,
            y=5,
            items=[
                Item(
                    name="servilo-kabineto",
                    description="Un alta servilo-kabineto kun blinkanta luci.",
                    can_pick_up=False,
                    required_skill="technical",
                    required_skill_level=2,
                    interactions={"uzi": "Vi akesas la sistemo e ekamenas la datumi."}
                )
            ],
            exits={
                "weste": "control_room"
            }
        )
        
        # Hall
        hall = Location(
            id="hall",
            name="Halo",
            description="Un longa koridoro kun pordi ad altra chambri.",
            x=5,
            y=4,
            items=[],
            exits={
                "sude": "control_room",
                "norde": "break_room",
                "este": "lab"
            }
        )
        
        # Break Room
        break_room = Location(
            id="break_room",
            name="Pauso-Chambro",
            description="Un chambro kun stuli, tabli, e kafeo-mashino. Hike la laboristi relaxas.",
            x=5,
            y=3,
            items=[
                Item(
                    name="kafeo-mashino",
                    description="Un auto-kafeo-mashino.",
                    can_pick_up=False,
                    interactions={"uzi": "Vi facas un taso di varma kafeo."}
                )
            ],
            exits={
                "sude": "hall"
            }
        )
        
        # Lab
        lab = Location(
            id="lab",
            name="Laboratorio",
            description="Un ciencal laboratorio kun diversa aparati e instrumenti.",
            x=6,
            y=4,
            items=[
                Item(
                    name="mikroskopio",
                    description="Un preciza mikroskopio por analizor miliardizima specimeni.",
                    can_pick_up=False,
                    required_skill="observation",
                    required_skill_level=1,
                    interactions={"uzi": "Vi regardas tra la mikroskopio e vidas stranja celuli."}
                )
            ],
            exits={
                "weste": "hall"
            }
        )
        
        # Add locations to the map
        self.locations = {
            "control_room": control_room,
            "maintenance": maintenance,
            "server_room": server_room,
            "hall": hall,
            "break_room": break_room,
            "lab": lab
        }
        
        # Create a 2D grid representation of the map
        self._create_grid()
    
    def _create_grid(self):
        """Create a 2D grid representation of the map"""
        # Find map dimensions
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        for location in self.locations.values():
            min_x = min(min_x, location.x)
            min_y = min(min_y, location.y)
            max_x = max(max_x, location.x)
            max_y = max(max_y, location.y)
        
        # Create empty grid
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        self.current_map = [[None for _ in range(width)] for _ in range(height)]
        
        # Place locations on the grid
        for location in self.locations.values():
            x = location.x - min_x
            y = location.y - min_y
            self.current_map[y][x] = location.id
    
    def get_location(self, location_id):
        """Get a location by its ID"""
        return self.locations.get(location_id)
    
    def get_starting_location(self):
        """Get the starting location for the player"""
        # Control room is the default starting location for the technician
        return "control_room"
    
    def get_exits(self, location_id):
        """Get available exits from the current location"""
        location = self.get_location(location_id)
        if not location:
            return {}
        
        exits = {}
        for direction, exit_id in location.exits.items():
            exit_location = self.get_location(exit_id)
            if exit_location:
                exits[direction] = exit_id
        
        return exits
    
    def get_adjacent_location(self, location_id, direction):
        """Get the adjacent location in the specified direction"""
        exits = self.get_exits(location_id)
        return exits.get(direction)
    
    def update(self):
        """Update map state (for dynamic map elements)"""
        # This will be expanded in future versions with dynamic elements
        pass 