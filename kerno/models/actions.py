from dataclasses import dataclass
from kerno.utils.text_utils import TextFormatter

@dataclass
class ActionResult:
    success: bool
    message: str
    action_type: str = ""
    data: dict = None

class ActionHandler:
    def __init__(self, world, player):
        self.world = world
        self.player = player
        self.text_formatter = TextFormatter()
        
        # Use Ido for directions
        self.directions = ["nordo", "sudo", "esto", "westo", "supre", "infre"]
        self.direction_mapping = {
            "nordo": "north",
            "sudo": "south",
            "esto": "east",
            "westo": "west",
            "supre": "up",
            "infre": "down"
        }
        
        # Use Ido for basic actions
        self.basic_actions = ["regardar", "examinar", "prenar", "pozar", "uzar", "interagar", "inventario", "statuso", "helpo", "finar"]
        self.action_mapping = {
            "regardar": "look",
            "examinar": "examine",
            "prenar": "take",
            "pozar": "drop",
            "uzar": "use",
            "interagar": "interact",
            "inventario": "inventory",
            "statuso": "status",
            "helpo": "help",
            "finar": "quit"
        }
        
    def get_available_actions(self):
        """Get list of available actions in current context in Ido"""
        actions = self.basic_actions.copy()
        
        # Get available movement directions
        current_room = self.world.get_room(self.player.current_location)
        if current_room:
            # Map English exit directions to Ido directions
            available_directions = []
            for d_ido, d_en in self.direction_mapping.items():
                if d_en in current_room.exits:
                    available_directions.append(d_ido)
                    
            actions.extend(available_directions)
            
            # Add examine options for items in room
            for item in current_room.items:
                actions.append(f"examinar {item['name']}")
                actions.append(f"prenar {item['name']}")
                
            # Add interaction options for furniture
            for furniture in current_room.furniture:
                actions.append(f"interagar {furniture['name']}")
                actions.append(f"examinar {furniture['name']}")
        
        # Add inventory item actions
        for item in self.player.inventory:
            actions.append(f"examinar {item['name']}")
            actions.append(f"pozar {item['name']}")
            actions.append(f"uzar {item['name']}")
            
        return actions
        
    def process_action(self, action_input):
        """Process player action from input text in Ido"""
        action_input = action_input.lower().strip()
        
        # Handle empty input
        if not action_input:
            return ActionResult(
                success=False,
                message="Quo vu volas facar?",  # What would you like to do?
                action_type="none"
            )
        
        # Parse the input into action and target
        parts = action_input.split(maxsplit=1)
        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        
        # Movement commands
        if action in self.directions:
            english_direction = self.direction_mapping.get(action)
            return self._handle_movement(action, english_direction)
            
        # Basic commands
        elif action in self.action_mapping:
            english_action = self.action_mapping.get(action)
            
            if english_action == "look":
                return self._handle_look()
            elif english_action == "examine":
                return self._handle_examine(target)
            elif english_action == "take":
                return self._handle_take(target)
            elif english_action == "drop":
                return self._handle_drop(target)
            elif english_action == "use":
                return self._handle_use(target)
            elif english_action == "interact":
                return self._handle_interact(target)
            elif english_action == "inventory":
                return self._handle_inventory()
            elif english_action == "status":
                return self._handle_status()
            elif english_action == "help":
                return self._handle_help()
            elif english_action == "quit":
                return ActionResult(
                    success=True,
                    message="Ka vu certas ke vu volas finar? (yes/no)",  # Are you sure you want to quit?
                    action_type="quit"
                )
            
        # Unknown command
        return ActionResult(
            success=False,
            message=f"Me ne komprenas '{action_input}'.",  # I don't understand
            action_type="unknown"
        )
        
    def _handle_movement(self, ido_direction, english_direction):
        """Handle player movement in a direction"""
        if not self.world.can_move(self.player.current_location, english_direction):
            return ActionResult(
                success=False,
                message=f"Vu ne povas irar {ido_direction} de ca-loke.",  # You can't go X from here
                action_type="move"
            )
            
        destination = self.world.get_destination(self.player.current_location, english_direction)
        self.player.current_location = destination
        self.player.move(english_direction)
        
        current_room = self.world.get_room(destination)
        return ActionResult(
            success=True,
            message=f"Vu movas {ido_direction}.",  # You move X
            action_type="move",
            data={"destination": destination}
        )
        
    def _handle_look(self):
        """Handle looking around"""
        current_room = self.world.get_room(self.player.current_location)
        if not current_room:
            return ActionResult(
                success=False,
                message="Vu ne povas komprenar vua cirkumajo.",  # You can't make out your surroundings
                action_type="look"
            )
            
        return ActionResult(
            success=True,
            message=current_room.get_description(detailed=True),
            action_type="look"
        )
        
    def _handle_examine(self, target):
        """Handle examining an object"""
        if not target:
            return ActionResult(
                success=False,
                message="Quo vu volas examinar?",  # What would you like to examine?
                action_type="examine"
            )
            
        # Check if the target is in the player's inventory
        for item in self.player.inventory:
            if target.lower() in item["name"].lower():
                return ActionResult(
                    success=True,
                    message=item.get("description", f"Un {item['name']}."),  # A [item name]
                    action_type="examine",
                    data={"item": item}
                )
                
        # Check if the target is in the current room
        current_room = self.world.get_room(self.player.current_location)
        if current_room:
            # Check room items
            for item in current_room.items:
                if target.lower() in item["name"].lower():
                    return ActionResult(
                        success=True,
                        message=item.get("description", f"Un {item['name']}."),  # A [item name]
                        action_type="examine",
                        data={"item": item}
                    )
                    
            # Check room furniture
            for furniture in current_room.furniture:
                if target.lower() in furniture["name"].lower():
                    return ActionResult(
                        success=True,
                        message=furniture.get("description", f"Un {furniture['name']}."),  # A [furniture name]
                        action_type="examine",
                        data={"furniture": furniture}
                    )
                    
        return ActionResult(
            success=False,
            message=f"Vu ne vidas {target} ca-hike.",  # You don't see any X here
            action_type="examine"
        )
        
    def _handle_take(self, target):
        """Handle taking an item"""
        if not target:
            return ActionResult(
                success=False,
                message="Quo vu volas prenar?",  # What would you like to take?
                action_type="take"
            )
            
        # Check if the target is in the current room
        current_room = self.world.get_room(self.player.current_location)
        if current_room:
            for item in current_room.items:
                if target.lower() in item["name"].lower():
                    if item.get("takeable", True):
                        # Add to inventory and remove from room
                        self.player.add_item(item)
                        self.world.remove_item_from_room(current_room.id, item["id"])
                        return ActionResult(
                            success=True,
                            message=f"Vu prenas la {item['name']}.",  # You take the X
                            action_type="take",
                            data={"item": item}
                        )
                    else:
                        return ActionResult(
                            success=False,
                            message=f"Vu ne povas prenar la {item['name']}.",  # You can't take the X
                            action_type="take"
                        )
                        
        return ActionResult(
            success=False,
            message=f"Vu ne vidas {target} ca-hike por prenar.",  # You don't see any X here that you can take
            action_type="take"
        )
        
    def _handle_drop(self, target):
        """Handle dropping an item"""
        if not target:
            return ActionResult(
                success=False,
                message="Quo vu volas pozar?",  # What would you like to drop?
                action_type="drop"
            )
            
        # Check if the target is in the player's inventory
        for item in self.player.inventory:
            if target.lower() in item["name"].lower():
                # Remove from inventory and add to room
                self.player.remove_item(item["id"])
                self.world.add_item_to_room(self.player.current_location, item)
                return ActionResult(
                    success=True,
                    message=f"Vu pozas la {item['name']}.",  # You drop the X
                    action_type="drop",
                    data={"item": item}
                )
                
        return ActionResult(
            success=False,
            message=f"Vu ne havas {target} por pozar.",  # You don't have any X to drop
            action_type="drop"
        )
        
    def _handle_use(self, target):
        """Handle using an item"""
        if not target:
            return ActionResult(
                success=False,
                message="Quo vu volas uzar?",  # What would you like to use?
                action_type="use"
            )
            
        # Check if the target is in the player's inventory
        for item in self.player.inventory:
            if target.lower() in item["name"].lower():
                if not item.get("usable", False):
                    return ActionResult(
                        success=False,
                        message=f"Vu ne povas uzar la {item['name']} talamaniere.",  # You can't use the X like that
                        action_type="use"
                    )
                    
                # Process item use
                result = self._process_item_use(item)
                if result.success:
                    self.player.use_item(item["id"])
                return result
                
        return ActionResult(
            success=False,
            message=f"Vu ne havas {target} por uzar.",  # You don't have any X to use
            action_type="use"
        )
        
    def _process_item_use(self, item):
        """Process the effects of using an item"""
        item_type = item.get("type", "generic")
        
        if item_type == "food":
            nutrition = item.get("nutrition", 10)
            self.player.consume_food(nutrition)
            return ActionResult(
                success=True,
                message=f"Vu manjas la {item['name']}. Ol satigas vua hungro.",  # You eat the X. It satisfies your hunger
                action_type="use",
                data={"effect": "nutrition", "value": nutrition}
            )
            
        elif item_type == "drink":
            hydration = item.get("hydration", 10)
            self.player.consume_drink(hydration)
            return ActionResult(
                success=True,
                message=f"Vu drinkas la {item['name']}. Ol satenigas vua soifo.",  # You drink the X. It quenches your thirst
                action_type="use",
                data={"effect": "hydration", "value": hydration}
            )
            
        elif item_type == "tool":
            # Tool use might depend on room context
            current_room = self.world.get_room(self.player.current_location)
            if "use_effects" in item and current_room:
                for effect in item["use_effects"]:
                    if effect.get("room_type") == current_room.type:
                        return ActionResult(
                            success=True,
                            message=effect.get("message", f"Vu uzas la {item['name']}."),  # You use the X
                            action_type="use",
                            data={"effect": effect}
                        )
                        
            return ActionResult(
                success=False,
                message=f"Vu ne povas trovar maniero uzar la {item['name']} ca-hike.",  # You can't find a way to use the X here
                action_type="use"
            )
            
        else:
            # Generic item use
            return ActionResult(
                success=True,
                message=item.get("use_message", f"Vu uzas la {item['name']}."),  # You use the X
                action_type="use"
            )
            
    def _handle_interact(self, target):
        """Handle interacting with an object"""
        if not target:
            return ActionResult(
                success=False,
                message="Kun quo vu volas interagar?",  # What would you like to interact with?
                action_type="interact"
            )
            
        # Check if the target is in the current room's furniture
        current_room = self.world.get_room(self.player.current_location)
        if current_room:
            for furniture in current_room.furniture:
                if target.lower() in furniture["name"].lower():
                    self.player.interact()
                    
                    # Check if the furniture has interaction effects
                    if "interaction" in furniture:
                        interaction = furniture["interaction"]
                        message = interaction.get("message", f"Vu interagas kun la {furniture['name']}.")  # You interact with the X
                        
                        # Process any effects
                        if "effects" in interaction:
                            self.world._process_event_effects(interaction["effects"], self.player)
                            
                        return ActionResult(
                            success=True,
                            message=message,
                            action_type="interact",
                            data={"furniture": furniture}
                        )
                        
                    return ActionResult(
                        success=True,
                        message=f"Vu interagas kun la {furniture['name']} ma nulo eventas.",  # You interact with the X but nothing happens
                        action_type="interact"
                    )
                    
        return ActionResult(
            success=False,
            message=f"Vu ne vidas {target} ca-hike por interagar.",  # You don't see any X here that you can interact with
            action_type="interact"
        )
        
    def _handle_inventory(self):
        """Handle checking inventory"""
        if not self.player.inventory:
            return ActionResult(
                success=True,
                message="Vua inventario esas vakua.",  # Your inventory is empty
                action_type="inventory"
            )
            
        inventory_text = "Inventario:\n"
        for item in self.player.inventory:
            inventory_text += f"- {item['name']}\n"
            
        return ActionResult(
            success=True,
            message=inventory_text,
            action_type="inventory",
            data={"items": self.player.inventory}
        )
        
    def _handle_status(self):
        """Handle checking player status"""
        status = self.player.get_status()
        
        # Status terms are already in Ido from the player class
        status_text = f"Saneso: {status['health']}\n"
        status_text += f"Hungro: {status['hunger']}\n"
        status_text += f"Soifo: {status['thirst']}\n"
        status_text += f"Energio: {status['energy']}\n"
        
        if "effects" in status:
            status_text += "Statuso-efekti: " + ", ".join(status["effects"])
            
        return ActionResult(
            success=True,
            message=status_text,
            action_type="status",
            data={"status": status}
        )
        
    def _handle_help(self):
        """Handle help command"""
        help_text = "Disponebla komandi:\n"
        help_text += "- regardar: Regardar vua nuna loko\n"
        help_text += "- examinar [objekto]: Examinar objekto plu detale\n"
        help_text += "- prenar [objekto]: Prenar objekto e pozar ol en vua inventario\n"
        help_text += "- pozar [objekto]: Pozar objekto de vua inventario\n"
        help_text += "- uzar [objekto]: Uzar objekto de vua inventario\n"
        help_text += "- interagar [objekto]: Interagar kun objekto en la medio\n"
        help_text += "- inventario: Kontrolar vua inventario\n"
        help_text += "- statuso: Kontrolar vua nuna statuso\n"
        help_text += "- [direciono]: Movar en direciono (nordo, sudo, esto, westo, supre, infre)\n"
        help_text += "- finar: Finar la ludo\n"
        
        return ActionResult(
            success=True,
            message=help_text,
            action_type="help"
        ) 