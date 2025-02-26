import sys
import importlib

# Force reload core modules to clear any cached imports
if 'core.config_manager' in sys.modules:
    importlib.reload(sys.modules['core.config_manager'])
if 'core.database_manager' in sys.modules:
    importlib.reload(sys.modules['core.database_manager'])
if 'core.director' in sys.modules:
    importlib.reload(sys.modules['core.director'])
if 'core.app' in sys.modules:
    importlib.reload(sys.modules['core.app'])

from multiprocessing import Process

from core.app import App
from core import common
from core import splash


def main():
    """Entry point for the application.
    
    This function is the entry point for the application. It creates the app
    and starts the main loop.
    """
    # Create the app
    common.app = App()
    common.app.mainloop()

if __name__ == "__main__":
    # Start the main process in a separate process to avoid blocking the splash
    main_process = Process(target=main)
    main_process.start()

    # Create the splash screen
    splash.SplashScreen("assets/splash.png", 3000)

    # Wait for the main process to finish
    main_process.join()

    

    
    