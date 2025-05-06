from dataclasses import dataclass

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
        self.directions = ["north", "south", "east", "west", "up", "down"]
        self.basic_actions = ["look", "examine", "take", "drop", "use", "interact", "inventory", "status", "help", "quit"]
        
    def get_available_actions(self):
        """Get list of available actions in current context"""
        actions = self.basic_actions.copy()
        
        # Get available movement directions
        current_room = self.world.get_room(self.player.current_location)
        if current_room:
            available_directions = [d for d in self.directions if d in current_room.exits]
            actions.extend(available_directions)
            
            # Add examine options for items in room
            for item in current_room.items:
                actions.append(f"examine {item['name']}")
                actions.append(f"take {item['name']}")
                
            # Add interaction options for furniture
            for furniture in current_room.furniture:
                actions.append(f"interact {furniture['name']}")
                actions.append(f"examine {furniture['name']}")
        
        # Add inventory item actions
        for item in self.player.inventory:
            actions.append(f"examine {item['name']}")
            actions.append(f"drop {item['name']}")
            actions.append(f"use {item['name']}")
            
        return actions
        
    def process_action(self, action_input):
        """Process player action from input text"""
        action_input = action_input.lower().strip()
        
        # Handle empty input
        if not action_input:
            return ActionResult(
                success=False,
                message="What would you like to do?",
                action_type="none"
            )
        
        # Parse the input into action and target
        parts = action_input.split(maxsplit=1)
        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        
        # Movement commands
        if action in self.directions:
            return self._handle_movement(action)
            
        # Basic commands
        elif action == "look":
            return self._handle_look()
        elif action == "examine":
            return self._handle_examine(target)
        elif action == "take":
            return self._handle_take(target)
        elif action == "drop":
            return self._handle_drop(target)
        elif action == "use":
            return self._handle_use(target)
        elif action == "interact":
            return self._handle_interact(target)
        elif action == "inventory":
            return self._handle_inventory()
        elif action == "status":
            return self._handle_status()
        elif action == "help":
            return self._handle_help()
        elif action == "quit":
            return ActionResult(
                success=True,
                message="Are you sure you want to quit? (yes/no)",
                action_type="quit"
            )
            
        # Unknown command
        return ActionResult(
            success=False,
            message=f"I don't understand '{action_input}'.",
            action_type="unknown"
        )
        
    def _handle_movement(self, direction):
        """Handle player movement in a direction"""
        if not self.world.can_move(self.player.current_location, direction):
            return ActionResult(
                success=False,
                message=f"You can't go {direction} from here.",
                action_type="move"
            )
            
        destination = self.world.get_destination(self.player.current_location, direction)
        self.player.current_location = destination
        self.player.move(direction)
        
        current_room = self.world.get_room(destination)
        return ActionResult(
            success=True,
            message=f"You move {direction}.",
            action_type="move",
            data={"destination": destination}
        )
        
    def _handle_look(self):
        """Handle looking around"""
        current_room = self.world.get_room(self.player.current_location)
        if not current_room:
            return ActionResult(
                success=False,
                message="You can't make out your surroundings.",
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
                message="What would you like to examine?",
                action_type="examine"
            )
            
        # Check if the target is in the player's inventory
        for item in self.player.inventory:
            if target.lower() in item["name"].lower():
                return ActionResult(
                    success=True,
                    message=item.get("description", f"A {item['name']}."),
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
                        message=item.get("description", f"A {item['name']}."),
                        action_type="examine",
                        data={"item": item}
                    )
                    
            # Check room furniture
            for furniture in current_room.furniture:
                if target.lower() in furniture["name"].lower():
                    return ActionResult(
                        success=True,
                        message=furniture.get("description", f"A {furniture['name']}."),
                        action_type="examine",
                        data={"furniture": furniture}
                    )
                    
        return ActionResult(
            success=False,
            message=f"You don't see any {target} here.",
            action_type="examine"
        )
        
    def _handle_take(self, target):
        """Handle taking an item"""
        if not target:
            return ActionResult(
                success=False,
                message="What would you like to take?",
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
                            message=f"You take the {item['name']}.",
                            action_type="take",
                            data={"item": item}
                        )
                    else:
                        return ActionResult(
                            success=False,
                            message=f"You can't take the {item['name']}.",
                            action_type="take"
                        )
                        
        return ActionResult(
            success=False,
            message=f"You don't see any {target} here that you can take.",
            action_type="take"
        )
        
    def _handle_drop(self, target):
        """Handle dropping an item"""
        if not target:
            return ActionResult(
                success=False,
                message="What would you like to drop?",
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
                    message=f"You drop the {item['name']}.",
                    action_type="drop",
                    data={"item": item}
                )
                
        return ActionResult(
            success=False,
            message=f"You don't have any {target} to drop.",
            action_type="drop"
        )
        
    def _handle_use(self, target):
        """Handle using an item"""
        if not target:
            return ActionResult(
                success=False,
                message="What would you like to use?",
                action_type="use"
            )
            
        # Check if the target is in the player's inventory
        for item in self.player.inventory:
            if target.lower() in item["name"].lower():
                if not item.get("usable", False):
                    return ActionResult(
                        success=False,
                        message=f"You can't use the {item['name']} like that.",
                        action_type="use"
                    )
                    
                # Process item use
                result = self._process_item_use(item)
                if result.success:
                    self.player.use_item(item["id"])
                return result
                
        return ActionResult(
            success=False,
            message=f"You don't have any {target} to use.",
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
                message=f"You eat the {item['name']}. It satisfies your hunger.",
                action_type="use",
                data={"effect": "nutrition", "value": nutrition}
            )
            
        elif item_type == "drink":
            hydration = item.get("hydration", 10)
            self.player.consume_drink(hydration)
            return ActionResult(
                success=True,
                message=f"You drink the {item['name']}. It quenches your thirst.",
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
                            message=effect.get("message", f"You use the {item['name']}."),
                            action_type="use",
                            data={"effect": effect}
                        )
                        
            return ActionResult(
                success=False,
                message=f"You can't find a way to use the {item['name']} here.",
                action_type="use"
            )
            
        else:
            # Generic item use
            return ActionResult(
                success=True,
                message=item.get("use_message", f"You use the {item['name']}."),
                action_type="use"
            )
            
    def _handle_interact(self, target):
        """Handle interacting with an object"""
        if not target:
            return ActionResult(
                success=False,
                message="What would you like to interact with?",
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
                        message = interaction.get("message", f"You interact with the {furniture['name']}.")
                        
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
                        message=f"You interact with the {furniture['name']} but nothing happens.",
                        action_type="interact"
                    )
                    
        return ActionResult(
            success=False,
            message=f"You don't see any {target} here that you can interact with.",
            action_type="interact"
        )
        
    def _handle_inventory(self):
        """Handle checking inventory"""
        if not self.player.inventory:
            return ActionResult(
                success=True,
                message="Your inventory is empty.",
                action_type="inventory"
            )
            
        inventory_text = "Inventory:\n"
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
        
        status_text = f"Health: {status['health']}\n"
        status_text += f"Hunger: {status['hunger']}\n"
        status_text += f"Thirst: {status['thirst']}\n"
        status_text += f"Energy: {status['energy']}\n"
        
        if "effects" in status:
            status_text += "Status effects: " + ", ".join(status["effects"])
            
        return ActionResult(
            success=True,
            message=status_text,
            action_type="status",
            data={"status": status}
        )
        
    def _handle_help(self):
        """Handle help command"""
        help_text = "Available commands:\n"
        help_text += "- look: Look around your current location\n"
        help_text += "- examine [object]: Examine an object more closely\n"
        help_text += "- take [item]: Take an item and add it to your inventory\n"
        help_text += "- drop [item]: Drop an item from your inventory\n"
        help_text += "- use [item]: Use an item from your inventory\n"
        help_text += "- interact [object]: Interact with an object in the environment\n"
        help_text += "- inventory: Check your inventory\n"
        help_text += "- status: Check your current status\n"
        help_text += "- [direction]: Move in a direction (north, south, east, west, up, down)\n"
        help_text += "- quit: Exit the game\n"
        
        return ActionResult(
            success=True,
            message=help_text,
            action_type="help"
        ) 