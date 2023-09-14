import requests
import time

# Define the base URL for the Pong game server
BASE_URL = "http://localhost:8000"


# Function to continuously make GET requests to the /ping endpoint
def watch_game():
    while True:
        try:
            response = requests.get(BASE_URL + "/ping")
            if response.status_code == 200:
                message = response.json()["message"]
                print(message)
            else:
                print(f"Error: {response.status_code} - {response.text}")

            # Adjust the sleep time as needed to control the polling frequency
            time.sleep(1)  # Sleep for 1 second between requests
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Watching the Pong game. Press Ctrl+C to exit.")
    watch_game()