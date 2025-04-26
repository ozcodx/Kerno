# Kerno

## Game Overview
**Kerno: Kaliel - La Lasta Devo** is a narrative exploration game set in the final days of the Thalosian civilization, right before the collapse caused by the failed Crucis Engine project. Players embody an ordinary worker—initially a technician—performing routine tasks within an underground complex. Unknowingly, their actions will place them at the center of a catastrophic event that will seal the fate of the world.

**Genre:** Narrative adventure + exploration + light survival
**Aesthetic:** Retro-functional science fiction, low magic (advanced technology that appears magical)
**Game Language:** Everything occurs exclusively in Ido

## Game Stages

### Stage 1 - Daily Routine
- Player performs routine tasks in their work area
- Learn basic Ido language structures through simple actions: move, look, use, wait
- Encounter characters, like Kaliel, who provide humor, clues, and depth
- This stage works as an immersive tutorial without breaking the fiction

### Stage 2 - First Anomaly
- A minor event (technical failure, creature, human error) initiates a chain of failures
- Player begins to notice alterations in the environment
- Can continue exploring and completing tasks, but everything becomes more unstable

### Stage 3 - Expansion
- The map opens to hidden or closed areas
- The narrative branches according to decisions, discoveries, or unintentional actions
- Introduction of more complex puzzles, traps, creatures, and mysteries
- Player begins to understand that something serious and large-scale is happening

### Stage 4 - Confrontation / Choice
- A point of no return is reached
- Clues reveal that the player might have caused or could prevent part of the disaster
- Multiple routes to the ending are presented: sabotage, escape, collaboration with Kaliel, confrontation, or inaction

### Stage 5 - Multiple Endings
- Tragic, confrontational, complicit, hidden, or redemption endings
- All narratively connect with the Ashwake universe

## Game Engine and Technical Considerations

### Language and Environment
- Python + pygame as the base for the graphics engine
- Completely offline with no server
- Local LAN support planned for future versions (without requiring a dedicated server)

### Player Input
- Version 0: List of predefined actions in Ido (clicks or keys)
- Future: Free text input with lexical/syntactic parser in Ido, with autocomplete system and suggestions ("maybe you meant to say")

### Map and GUI
- Simple 2D representation of explored map (visual tiles)
- Each cell has a visual type (bridge, ladder, passage...)
- Interface divided into:
  - Map
  - Environment text
  - Inventory
  - List of available actions
  - Notebook/dictionary
  - Representative illustration of the environment
  - Text input or buttons (depending on version)

## Support for Multiple Professions

### Design
- Player can choose their role at the beginning
- Each profession will have:
  - Its own initial routine
  - Unique access within the map
  - Small thematic advantages (e.g., technician can repair, botanist can analyze plants, etc.)
  - Different dialogues and encounters
- The story converges but from different perspectives, offering replayability

### Initial Profession in MVP: Technician
- Checks terminals, corrects electrical failures, inspects energy nodes
- Can unwittingly activate an experimental subsystem that contributes to the collapse

## Incremental Project Growth
The game is designed to be developed in additive modules:

| Module | Description | Priority |
|--------|-------------|----------|
| Basic map + movement | 2D navigation with clear structure | High (MVP base) |
| Action system in Ido | Selection by contextual menu | High |
| Events and puzzles engine | Traps, mechanisms, doors | High |
| Kaliel (character and dialogues) | Scripted events and variable reactions | Medium |
| Free language parser | Requires future integration with another project | Medium |
| New professions | Botanist, archivist, etc. | Medium |
| Survival elements | Hunger, thirst, rest | Optional (advanced mode) |
| Combat system | By text or commands (simple enemies) | Medium |
| Cooperative LAN support | Share map and collaborate on puzzles | Low (future) |

## Additional Considerations

### Hunger and Thirst Management
- Planned as an optional game mode to add complexity
- Player must find food/water in the dungeon
- Affects performance (less precision, hallucinations, technical failures)
- Represents the fragility of humans even in a technological environment

## Narrative Philosophy

- You are not a hero, nor the protagonist of an epic
- You are a person who was just trying to do their job
- Learning the Ido language is emergent: it happens because you need to communicate with the world
- Kaliel is your reflection, your accomplice, or your enemy
- A tragic and comic character, as human as you
- Everything may seem routine... until it isn't 