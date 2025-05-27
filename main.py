from customtkinter import CTk, CTkLabel, CTkFrame, CTkOptionMenu
import os
import sys
from pathlib import Path
from frontend.login import Login
from backend.init_db import init_database
import time # Keep time import as it's used in on_window_resize

class Main:
    """Main application class responsible for setting up the main window and managing the application flow."""
    def __init__(self):
        self.main_window = CTk()
        
        # Configure main window for responsiveness
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)
        
        # Adjust window size based on screen size
        self.set_window_size()
        
        # Scale UI elements based on screen resolution
        self.scale_ui_elements()
        
        self.setup_main_window()
        
    def set_window_size(self):
        """Adjust window size based on screen size, with a minimum size."""
        # Get screen dimensions
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        
        # Calculate initial window size as 50% of screen size
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        
        # Define minimum window size
        min_width = 800
        min_height = 540
        
        # Ensure window size is not less than the minimum
        window_width = max(window_width, min_width)
        window_height = max(window_height, min_height)
        
        # Set minimum window size to prevent excessive shrinking
        self.main_window.minsize(min_width, min_height)
        
        # Set maximum window size (can be maximized to full screen)
        self.main_window.maxsize(screen_width, screen_height)
        
        # Enable window resizing
        self.main_window.resizable(True, True)
        
        # Calculate window position to center it on the screen
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)
        
        # Apply the calculated size and position
        self.main_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
    def scale_ui_elements(self):
        """Adjust UI element scaling based on screen resolution for better user experience."""
        # Get screen dimensions
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        
        # Calculate aspect ratio
        aspect_ratio = screen_width / screen_height
        
        # Calculate scaling factor based on screen resolution and aspect ratio
        if screen_width >= 2560 and screen_height >= 1440:  # Ultra HD (2K and above)
            scaling_factor = 1.4
        elif screen_width >= 1920 and screen_height >= 1080:  # Full HD
            scaling_factor = 1.2
        elif screen_width >= 1366 and screen_height >= 768:  # Medium resolution screens
            scaling_factor = 1.0
        else:  # Low resolution screens
            scaling_factor = 0.8
        
        # Adjust scaling factor for very wide screens
        if aspect_ratio > 2.0:  # Very wide screens
            scaling_factor *= 0.9
        
        # Apply the scaling factor to the UI
        self.main_window.tk.call("tk", "scaling", scaling_factor)
        
        # Optional: Print scaling information for development (can be removed in final version)
        # print(f"Screen size: {screen_width}x{screen_height}, Aspect Ratio: {aspect_ratio:.2f}, Scaling Factor: {scaling_factor:.2f}")

    
    def setup_main_window(self):
        """Configures the main application window."""
        # Set window title
        self.main_window.title("EL-NADA Nursery")
        
        # Load application icon
        icon_path = os.path.join(Path(__file__).resolve().parent, "images", "ELNADA-icon.ico")
        try:
            self.main_window.iconbitmap(icon_path)
        except:
            # Ignore error if icon file is not found
            # print("Warning: Icon file not found.") # Removed print statement
            pass
        
        # Enable window resizing (re-confirming)
        self.main_window.resizable(True, True)
        
        # Bind window resize event
        self.main_window.bind("<Configure>", self.on_window_resize)
            
        # Add a menu for testing different resolutions if the --test-resolution argument is provided
        if len(sys.argv) > 1 and sys.argv[1] == "--test-resolution":
            self.add_resolution_tester()
          
    def add_resolution_tester(self):
        """Adds resolution testing tools for development/debugging."""
        test_frame = CTkFrame(self.main_window)
        test_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)
        
        resolutions = [
            "800x600", "1024x768", "1280x720", "1366x768", 
            "1600x900", "1920x1080", "2560x1440"
        ]
        
        CTkLabel(test_frame, text="Test Resolution:").grid(row=0, column=0, padx=5, pady=5)
        
        resolution_menu = CTkOptionMenu(
            test_frame, 
            values=resolutions,
            command=self.change_resolution
        )
        resolution_menu.grid(row=1, column=0, padx=5, pady=5)
        resolution_menu.set("1000x700") # Set a default starting resolution
    
    def change_resolution(self, resolution):
        """Changes the window size for testing purposes."""
        self.main_window.geometry(resolution)
    
    def on_window_resize(self, event):
        """Handles window resize events."""
        # Get the new window dimensions
        new_width = event.width
        new_height = event.height
        
        # If you need to update other UI elements based on the new size,
        # add that logic here.
        # Example: self.update_some_element(new_width, new_height)

    
    def run(self):
        """Starts the main application loop."""
        # Use the main window directly without an extra scrollable frame
        # This will make the interface use the full window space
        
        # Pass the main window directly to the pages
        Login(self.main_window)
        
        # Start the main event loop
        self.main_window.mainloop()

if __name__ == "__main__":
    # Initialize the database before starting the application
    init_database()
    
    # Create and run the main application instance
    app = Main()
    app.run()    

