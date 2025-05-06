import os
import sys
import time
import textwrap

class GameIO:
    def __init__(self):
        self.wrapper = textwrap.TextWrapper(width=80, replace_whitespace=False)
        self.text_speed = 0.01  # Delay between characters for typing effect
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_intro(self):
        """Display game introduction"""
        intro_text = """
        ██╗  ██╗███████╗██████╗ ███╗   ██╗ ██████╗ 
        ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔═══██╗
        █████╔╝ █████╗  ██████╔╝██╔██╗ ██║██║   ██║
        ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██║   ██║
        ██║  ██╗███████╗██║  ██║██║ ╚████║╚██████╔╝
        ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        
        LA LASTA DEVO
        
        A narrative exploration in the final days of Thalos
        """
        
        # Print intro with typing effect
        self.type_text(intro_text)
        print("\nPress Enter to begin...")
        input()
        
    def display_message(self, message):
        """Display a game message with line wrapping"""
        # Split message into lines
        lines = message.strip().split('\n')
        
        for line in lines:
            # Wrap and print each line
            if line.strip():
                wrapped_lines = self.wrapper.wrap(line)
                for wrapped_line in wrapped_lines:
                    print(wrapped_line)
            else:
                # Keep empty lines for spacing
                print()
        
        print()  # Add a blank line after each message
        
    def display_prompt(self, available_actions=None):
        """Display the input prompt with optional action suggestions"""
        if available_actions:
            # We could optionally show a hint of possible actions here
            # print("Actions: " + ", ".join(available_actions[:5]) + " ...")
            pass
            
        prompt = "> "
        sys.stdout.write(prompt)
        sys.stdout.flush()
        
    def get_input(self):
        """Get user input"""
        return input()
        
    def type_text(self, text, speed=None):
        """Print text with a typing effect"""
        if speed is None:
            speed = self.text_speed
            
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
            
        print()  # Add a newline at the end 