class TextFormatter:
    def __init__(self):
        """Initialize text formatter with Ido as the only language"""
        self.language = "ido"
        
        # Commands in Ido
        self.basic_commands = [
            "regardar", "examinar", "prenar", "pozar", "uzar", 
            "interagar", "inventario", "statuso", "helpo", "finar",
            "nordo", "sudo", "esto", "westo", "supre", "infre"
        ]
        
    def format_room_description(self, room, player):
        """Format room description with dynamic elements in Ido"""
        # Start with the room name as a header
        formatted_text = f"{room.name}\n"
        formatted_text += "=" * len(room.name) + "\n\n"
        
        # Get the base description
        formatted_text += room.get_description()
        
        # Add player status if it's relevant
        if player.hunger > 80:
            formatted_text += "\n\nVua stomako dolorante grondas. Vu bezonas trovar nutrivo balde."
        elif player.thirst > 80:
            formatted_text += "\n\nVua boko esas sika. Vu desperate bezonas aquo."
        elif player.energy < 20:
            formatted_text += "\n\nVu sentas exhaustita. Vu devus reposar balde."
            
        return formatted_text
        
    def format_status_block(self, player):
        """Format player status as a visual block in Ido"""
        health_bar = self.create_progress_bar(player.health, 100, 20)
        hunger_bar = self.create_progress_bar(100 - player.hunger, 100, 20)  # Invert so empty is bad
        thirst_bar = self.create_progress_bar(100 - player.thirst, 100, 20)  # Invert so empty is bad
        energy_bar = self.create_progress_bar(player.energy, 100, 20)
        
        status_text = f"Saneso: {health_bar} {player.health}%\n"
        status_text += f"Hungro: {hunger_bar} {100-player.hunger}%\n"
        status_text += f"Soifo: {thirst_bar} {100-player.thirst}%\n"
        status_text += f"Energio: {energy_bar} {player.energy}%\n"
        
        if player.status_effects:
            status_text += "\nStatuso-efekti:\n"
            for effect in player.status_effects:
                status_text += f"- {effect['name']}: {effect['description']}\n"
                
        return status_text
        
    def create_progress_bar(self, value, max_value, width=20):
        """Create a visual progress bar"""
        filled_width = int(width * (value / max_value))
        empty_width = width - filled_width
        
        # Different characters based on value percentage
        if value / max_value > 0.7:
            bar_char = "█"  # Good
        elif value / max_value > 0.3:
            bar_char = "▓"  # Medium
        else:
            bar_char = "▒"  # Low
            
        return f"[{bar_char * filled_width}{' ' * empty_width}]"
        
    def format_inventory_list(self, inventory):
        """Format inventory items as a list in Ido"""
        if not inventory:
            return "Vua inventario esas vakua."
            
        inventory_text = "Inventario:\n"
        for item in inventory:
            inventory_text += f"- {item['name']}"
            if "weight" in item:
                inventory_text += f" ({item['weight']} kg)"
            inventory_text += "\n"
            
        return inventory_text
        
    def word_wrap(self, text, width=80):
        """Wrap text to fit within specified width"""
        lines = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            if not words:
                lines.append('')
                continue
                
            current_line = words[0]
            for word in words[1:]:
                if len(current_line) + len(word) + 1 <= width:
                    current_line += ' ' + word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            
        return '\n'.join(lines)