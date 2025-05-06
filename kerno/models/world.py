import json
import random
from pathlib import Path

class Room:
    def __init__(self, room_data):
        self.id = room_data.get("id")
        self.name = room_data.get("name", "Unknown Room")
        self.description = room_data.get("description", "An empty room.")
        self.type = room_data.get("type", "generic")
        self.visited = False
        self.items = room_data.get("items", [])
        self.furniture = room_data.get("furniture", [])
        self.exits = room_data.get("exits", {})
        self.events = room_data.get("events", [])
        self.properties = room_data.get("properties", {})
        self.sub_locations = room_data.get("sub_locations", [])
        
    def get_description(self, detailed=False):
        """Return room description, with additional details if requested"""
        desc = self.description
        
        # First visit provides more detail
        if not self.visited:
            detailed = True
            self.visited = True
        
        # Add information about items
        if self.items and detailed:
            item_desc = "\nVu povas vidar: " + ", ".join([item["name"] for item in self.items])
            desc += item_desc
        
        # Add information about furniture
        if self.furniture and detailed:
            furniture_desc = "\nLa chambro kontenas: " + ", ".join([f["name"] for f in self.furniture])
            desc += furniture_desc
            
        # Add information about exits
        exit_desc = "\nExiti: " + ", ".join(self._translate_exits()) if self.exits else "\nNe existas evidenta exiti."
        desc += exit_desc
        
        return desc
        
    def _translate_exits(self):
        """Translate exit directions to Ido"""
        direction_map = {
            "north": "nordo",
            "south": "sudo",
            "east": "esto",
            "west": "westo",
            "up": "supre",
            "down": "infre"
        }
        return [direction_map.get(direction, direction) for direction in self.exits.keys()]

class Passage:
    def __init__(self, passage_data):
        self.id = passage_data.get("id")
        self.name = passage_data.get("name", "Unknown Passage")
        self.description = passage_data.get("description", "A nondescript passage.")
        self.type = passage_data.get("type", "generic")
        self.visited = False
        self.connections = passage_data.get("connections", {})
        self.items = passage_data.get("items", [])
        self.properties = passage_data.get("properties", {})
        
    def get_description(self, detailed=False):
        """Return passage description"""
        desc = self.description
        
        # First visit provides more detail
        if not self.visited:
            detailed = True
            self.visited = True
            
        # Add information about items
        if self.items and detailed:
            item_desc = "\nVu povas vidar: " + ", ".join([item["name"] for item in self.items])
            desc += item_desc
            
        # Add information about connections
        conn_desc = "\nVu povas irar al: " + ", ".join(self._translate_connections()) if self.connections else "\nIca pasejo semblas duktar nulaloke."
        desc += conn_desc
        
        return desc
        
    def _translate_connections(self):
        """Translate connection directions to Ido"""
        direction_map = {
            "north": "nordo",
            "south": "sudo",
            "east": "esto", 
            "west": "westo",
            "up": "supre",
            "down": "infre"
        }
        return [direction_map.get(conn, conn) for conn in self.connections.keys()]

class World:
    def __init__(self, world_file):
        self.world_file = world_file
        self.rooms = {}
        self.passages = {}
        self.items = {}
        self.starting_room_id = None
        self.global_state = {}
        self.turn_count = 0
        self.events = []
        
    def load(self):
        """Load world data from file"""
        try:
            path = Path(self.world_file)
            with open(path, 'r', encoding='utf-8') as f:
                world_data = json.load(f)
                
            # Load global state
            self.global_state = world_data.get("global_state", {})
            self.starting_room_id = world_data.get("starting_room")
            
            # Load rooms
            for room_data in world_data.get("rooms", []):
                room = Room(room_data)
                self.rooms[room.id] = room
                
            # Load passages
            for passage_data in world_data.get("passages", []):
                passage = Passage(passage_data)
                self.passages[passage.id] = passage
                
            # Load global items
            for item_data in world_data.get("items", []):
                self.items[item_data["id"]] = item_data
                
            return True
        except Exception as e:
            print(f"Error loading world data: {e}")
            return False
            
    def get_starting_room(self):
        """Return the starting room"""
        return self.rooms.get(self.starting_room_id)
        
    def get_room(self, room_id):
        """Get a room by ID"""
        return self.rooms.get(room_id)
        
    def get_passage(self, passage_id):
        """Get a passage by ID"""
        return self.passages.get(passage_id)
        
    def can_move(self, room_id, direction):
        """Check if a move in given direction is possible"""
        room = self.get_room(room_id)
        if not room:
            return False
            
        return direction in room.exits
        
    def get_destination(self, room_id, direction):
        """Get destination room/passage ID when moving in a direction"""
        room = self.get_room(room_id)
        if not room or direction not in room.exits:
            return None
            
        return room.exits[direction]
        
    def add_item_to_room(self, room_id, item_data):
        """Add an item to a room"""
        room = self.get_room(room_id)
        if room:
            room.items.append(item_data)
            
    def remove_item_from_room(self, room_id, item_id):
        """Remove an item from a room"""
        room = self.get_room(room_id)
        if room:
            room.items = [item for item in room.items if item["id"] != item_id]
            
    def process_events(self, player):
        """Process world events for the current turn"""
        self.turn_count += 1
        events_messages = []
        
        # Process random events based on location
        current_room = self.get_room(player.current_location)
        if current_room and current_room.events:
            for event in current_room.events:
                if "probability" in event and random.random() < event["probability"]:
                    events_messages.append(event["message"])
                    # Handle any state changes from the event
                    if "effects" in event:
                        self._process_event_effects(event["effects"], player)
        
        # Process global events
        for event_id, event in enumerate(self.events):
            if "turns_remaining" in event:
                event["turns_remaining"] -= 1
                if event["turns_remaining"] <= 0:
                    events_messages.append(event["message"])
                    # Handle any state changes from the event
                    if "effects" in event:
                        self._process_event_effects(event["effects"], player)
                    # Remove the expired event
                    self.events.pop(event_id)
        
        return events_messages
        
    def _process_event_effects(self, effects, player):
        """Process effects from an event"""
        for effect in effects:
            effect_type = effect.get("type")
            if effect_type == "add_item":
                target = effect.get("target")
                item_data = effect.get("item")
                if target == "player":
                    player.add_item(item_data)
                elif target == "room":
                    room_id = effect.get("room_id", player.current_location)
                    self.add_item_to_room(room_id, item_data)
            elif effect_type == "remove_item":
                target = effect.get("target")
                item_id = effect.get("item_id")
                if target == "player":
                    player.remove_item(item_id)
                elif target == "room":
                    room_id = effect.get("room_id", player.current_location)
                    self.remove_item_from_room(room_id, item_id)
            elif effect_type == "set_global":
                key = effect.get("key")
                value = effect.get("value")
                if key:
                    self.global_state[key] = value
            elif effect_type == "schedule_event":
                turns = effect.get("turns", 1)
                message = effect.get("message", "Something happens.")
                new_effects = effect.get("effects", [])
                self.events.append({
                    "turns_remaining": turns,
                    "message": message,
                    "effects": new_effects
                })
            elif effect_type == "player_effect":
                effect_name = effect.get("effect")
                value = effect.get("value", 0)
                if effect_name == "rest":
                    player.rest(value)
                elif effect_name == "heal":
                    player.heal(value)
                elif effect_name == "damage":
                    player.take_damage(value) 