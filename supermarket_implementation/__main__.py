"""
Main module for the backend of the supermarket implementation
"""

from supermarket_implementation.app import App
from supermarket_implementation.server import run_server

if __name__ == "__main__":
    app = App()
    # Run the server!
    run_server(app.client)
