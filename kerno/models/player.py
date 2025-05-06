class Player:
    def __init__(self):
        self.name = "Technician"
        self.profession = "technician"  # Default profession for the MVP
        self.current_location = None  # ID of current room or passage
        self.inventory = []  # List of item dictionaries
        self.health = 100
        self.hunger = 0  # 0-100 scale, 100 is starving
        self.thirst = 0  # 0-100 scale, 100 is dehydrated
        self.energy = 100  # 0-100 scale, 0 is exhausted
        self.knowledge = {}  # Dict of learned information
        self.scars = []  # List of injury descriptions
        self.status_effects = []  # List of temporary effects
        self.stats = {
            "moves": 0,
            "items_taken": 0,
            "items_used": 0,
            "interactions": 0
        }
        
    def add_item(self, item):
        """Add an item to the player's inventory"""
        self.inventory.append(item)
        self.stats["items_taken"] += 1
        return True
        
    def remove_item(self, item_id):
        """Remove an item from inventory by ID"""
        for i, item in enumerate(self.inventory):
            if item["id"] == item_id:
                self.inventory.pop(i)
                return True
        return False
        
    def has_item(self, item_id):
        """Check if player has a specific item"""
        return any(item["id"] == item_id for item in self.inventory)
        
    def use_item(self, item_id):
        """Use an item from inventory"""
        for item in self.inventory:
            if item["id"] == item_id:
                self.stats["items_used"] += 1
                # Check if item is consumable and should be removed
                if item.get("consumable", False):
                    self.remove_item(item_id)
                return True
        return False
        
    def move(self, direction):
        """Record that player has moved"""
        self.stats["moves"] += 1
        # Energy consumption
        self.energy = max(0, self.energy - 1)
        # Increase hunger and thirst slightly with movement
        self.hunger = min(100, self.hunger + 0.5)
        self.thirst = min(100, self.thirst + 0.8)
        
    def interact(self):
        """Record that player has interacted with something"""
        self.stats["interactions"] += 1
        
    def learn(self, key, value):
        """Add knowledge to the player's memory"""
        self.knowledge[key] = value
        
    def knows(self, key):
        """Check if player knows something"""
        return key in self.knowledge
        
    def get_knowledge(self, key):
        """Get specific knowledge value"""
        return self.knowledge.get(key)
        
    def add_scar(self, description):
        """Add a permanent injury to the player"""
        self.scars.append(description)
        
    def add_status_effect(self, effect):
        """Add a temporary status effect"""
        self.status_effects.append(effect)
        
    def remove_status_effect(self, effect_id):
        """Remove a status effect by ID"""
        self.status_effects = [e for e in self.status_effects if e["id"] != effect_id]
        
    def has_status_effect(self, effect_id):
        """Check if player has a specific status effect"""
        return any(effect["id"] == effect_id for effect in self.status_effects)
        
    def consume_food(self, nutrition_value):
        """Reduce hunger based on nutrition value"""
        self.hunger = max(0, self.hunger - nutrition_value)
        
    def consume_drink(self, hydration_value):
        """Reduce thirst based on hydration value"""
        self.thirst = max(0, self.thirst - hydration_value)
        
    def rest(self, energy_recovery):
        """Recover energy based on rest value"""
        self.energy = min(100, self.energy + energy_recovery)
        
    def take_damage(self, amount):
        """Reduce health by damage amount"""
        self.health = max(0, self.health - amount)
        return self.health <= 0  # Return true if player died
        
    def heal(self, amount):
        """Increase health by healing amount"""
        self.health = min(100, self.health + amount)
        
    def get_status(self):
        """Get player status summary"""
        status = {
            "health": self.get_health_status(),
            "hunger": self.get_hunger_status(),
            "thirst": self.get_thirst_status(),
            "energy": self.get_energy_status()
        }
        
        if self.status_effects:
            status["effects"] = [e["name"] for e in self.status_effects]
            
        return status
        
    def get_health_status(self):
        """Get descriptive health status in Ido"""
        if self.health > 90:
            return "Sanoza"
        elif self.health > 70:
            return "Kelke vundita"
        elif self.health > 50:
            return "Vundita"
        elif self.health > 30:
            return "Serioze vundita"
        elif self.health > 10:
            return "Kritike vundita"
        else:
            return "Proxim morto"
            
    def get_hunger_status(self):
        """Get descriptive hunger status in Ido"""
        if self.hunger < 20:
            return "Satita"
        elif self.hunger < 40:
            return "Iomete hungrega"
        elif self.hunger < 60:
            return "Hungrega"
        elif self.hunger < 80:
            return "Tre hungrega"
        else:
            return "Afamanta"
            
    def get_thirst_status(self):
        """Get descriptive thirst status in Ido"""
        if self.thirst < 20:
            return "Hidratizita"
        elif self.thirst < 40:
            return "Kelke soifanta"
        elif self.thirst < 60:
            return "Soifanta"
        elif self.thirst < 80:
            return "Tre soifanta"
        else:
            return "Dehidratizita"
            
    def get_energy_status(self):
        """Get descriptive energy status in Ido"""
        if self.energy > 80:
            return "Energioza"
        elif self.energy > 60:
            return "Vigla"
        elif self.energy > 40:
            return "Fatigita"
        elif self.energy > 20:
            return "Tre fatigita"
        else:
            return "Exhaustita" 