"""
Main module for the backend of the supermarket implementation
"""
from argparse import ArgumentParser

from supermarket_implementation.app import App
from supermarket_implementation.server import run_server

if __name__ == "__main__":
    # Parse the command line arguments
    parser = ArgumentParser(description="Run the supermarket backend server.")
    parser.add_argument(
        "--host", "-H",
        type=str, default="localhost",
        help="The host to run the server on.",
    )
    parser.add_argument(
        "--port", "-P",
        type=int, default=3000,
        help="The port to run the server on.",
    )
    # Parse the arguments
    args = parser.parse_args()

    app = App()
    # Run the server!
    run_server(app.client, args.host, args.port)
