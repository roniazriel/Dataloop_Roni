import argparse
import requests
import json

"""This is a python script for a command-line interface (CLI) that interacts with a Pong game server using HTTP 
requests. It allows to control the Pong game by sending commands from the command line. """

# Define the base URL for the Pong game server
BASE_URL = "http://localhost:8000"


# Function to send HTTP POST requests to the Pong game server
def send_request(endpoint, method="POST", data=None):
    """
    :param endpoint: The endpoint or URL path to which the request will be sent
    :param method: The HTTP method
    :param data: The data to include in the request body

    """
    try:
        headers = {'Content-type': 'application/json'}
        if method == "POST":
            response = requests.post(BASE_URL + endpoint, headers=headers, data=json.dumps(data)) # Set the content type to JSON
        else:
            # Send a GET request to the specified endpoint
            response = requests.get(BASE_URL + endpoint)

        if response.status_code == 200:
            # If the response status code is 200, print the "message" field from the JSON response
            print(response.json()["message"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")


# CLI command-line parser
def main():
    parser = argparse.ArgumentParser(description="Pong Game CLI")  # define and parse command-line arguments

    # Add available commands
    parser.add_argument("command", choices=["start", "pause", "resume", "stop"],
                        help="Command to control the Pong game")

    # Add optional argument for 'start' command
    parser.add_argument("--pong_time_ms", type=int,
                        help="Interval between pongs in milliseconds (used with 'start' command)")

    # Construct the server endpoint based on the selected command
    args = parser.parse_args()

    # Map commands to corresponding server endpoints
    # An endpoint is a URL which allows you to access a (web) service running on a server.
    command_to_endpoint = {
        "start": "/start_game",
        "pause": "/pause_game",
        "resume": "/resume_game",
        "stop": "/stop_game"
    }

    # Construct the server endpoint based on the selected command
    endpoint = command_to_endpoint.get(args.command)

    if endpoint:
        # If 'start' command is selected, include the '--pong_time_ms' parameter as JSON in the request body
        if args.command == "start" and args.pong_time_ms is not None:
            send_request(endpoint, method="POST", data={"ms": args.pong_time_ms})
        else:
            # Send the command without any JSON data
            send_request(endpoint, method="POST", data=None)
    else:
        print("Invalid command. Use 'start', 'pause', 'resume', or 'stop'.")


if __name__ == "__main__":
    main()
