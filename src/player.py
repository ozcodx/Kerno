"""
Player module representing the player character
"""

class Player:
    """Player class representing the player character in the game"""
    
    def __init__(self, config):
        """Initialize player with default values"""
        self.config = config
        self.position = None  # Will be set when the map is created
        self.profession = config.player_profession
        self.inventory = []
        
        # Player stats
        self.energy = 100
        self.stress = 0
        
        # Optional survival stats (for advanced mode)
        self.hunger = 0
        self.thirst = 0
        self.fatigue = 0
        
        # Skills based on profession
        self.skills = self._initialize_skills()
    
    def _initialize_skills(self):
        """Initialize skills based on player profession"""
        skills = {
            "technical": 0,
            "observation": 0,
            "communication": 0,
            "physical": 0
        }
        
        # Set skills based on profession
        if self.profession == "technician":
            skills["technical"] = 2
            skills["observation"] = 1
        elif self.profession == "botanist":
            skills["observation"] = 2
            skills["technical"] = 1
        elif self.profession == "archivist":
            skills["observation"] = 2
            skills["communication"] = 1
        
        return skills
    
    def add_to_inventory(self, item):
        """
        Add an item to the player's inventory
        
        Item format expected to be a dict with:
        - name: Name of the item
        - description: Item description
        - icon: Optional image for the item
        - amount: Number of items (stacks)
        """
        # Check if item already exists in inventory (for stacking)
        for inv_item in self.inventory:
            if inv_item.get('name') == item.get('name'):
                # Increase amount
                inv_item['amount'] = inv_item.get('amount', 1) + item.get('amount', 1)
                return
        
        # If item not found, add it
        self.inventory.append(item)
    
    def remove_from_inventory(self, item_name, amount=1):
        """Remove an item from the player's inventory"""
        for i, item in enumerate(self.inventory):
            if item.get('name') == item_name:
                # Decrease amount
                item['amount'] = item.get('amount', 1) - amount
                
                # Remove if amount is 0 or less
                if item['amount'] <= 0:
                    self.inventory.pop(i)
                
                return True
        return False
    
    def has_item(self, item_name):
        """Check if player has an item"""
        return any(item.get('name') == item_name for item in self.inventory)
    
    def get_item(self, item_name):
        """Get an item from inventory by name"""
        for item in self.inventory:
            if item.get('name') == item_name:
                return item
        return None
    
    def has_skill(self, skill_name, required_level=1):
        """Check if player has the required skill level"""
        return self.skills.get(skill_name, 0) >= required_level
    
    def can_interact_with(self, item):
        """Check if player can interact with the item"""
        # In the future, this will check profession-specific abilities
        return True
    
    def update(self):
        """Update player state"""
        # Update survival stats if enabled
        if hasattr(self.config, 'survival_mode') and self.config.survival_mode:
            self._update_survival_stats()
    
    def _update_survival_stats(self):
        """Update survival stats (hunger, thirst, fatigue)"""
        # Increase hunger and thirst over time
        self.hunger = min(self.hunger + 0.01, 100)
        self.thirst = min(self.thirst + 0.02, 100)
        self.fatigue = min(self.fatigue + 0.005, 100)
        
        # Apply effects of high survival stats
        if self.hunger > 80 or self.thirst > 80 or self.fatigue > 80:
            self.energy = max(self.energy - 0.1, 0)
            self.stress = min(self.stress + 0.1, 100) 