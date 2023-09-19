from fastapi import FastAPI, Response, Body  # Response - custom HTTP responses that the API endpoint return, Body -
# declare the structure of the request body for the API endpoint
import time

# create FastAPI instance named app
app = FastAPI()

pong_time_ms = None
game_state = "stopped"


# Define routes and request handlers

# GET - can call the URL from your browser (localhost/ping)
@app.get("/ping")
def ping():
    """
    if the server is running, after pong_time_ms respond with a JSON message pong. Otherwise, return HTTP responds.
    """
    if game_state == "running":
        time.sleep(pong_time_ms / 1000)  # Sleep for pong_time_ms milliseconds
        return {"message": "pong"}
    else:
        return Response(content="Game is not running.", status_code=400)  # 200 - ok, 400- not ok


@app.post("/set_pong_time")
def set_pong_time(ms: int):
    """
    Set pong time
    """
    global pong_time_ms
    pong_time_ms = ms
    return {"message": f"Pong time set to {ms} milliseconds."}


@app.post("/start_game")
def start_game(ms: int = Body(..., embed=True)):
    """
    Change the game_state and set pong time
    """
    global game_state
    if game_state == "stopped":
        game_state = "running"
        set_pong_time(ms)
        return {"message": f"Game started with {ms} milliseconds between pongs."}
    else:
        return Response(content="Game is already running.", status_code=400)


@app.post("/pause_game")
def pause_game():
    """
    Pause game - change game_state to paused
    """
    global game_state
    if game_state == "running":
        game_state = "paused"
        return {"message": "Game paused."}
    else:
        return Response(content="Game is not running.", status_code=400)


@app.post("/resume_game")
def resume_game():
    """
    Resume game - change game_state to running
    """
    global game_state
    if game_state == "paused":
        game_state = "running"
        return {"message": "Game resumed."}
    else:
        return Response(content="Game is not paused.", status_code=400)


@app.post("/stop_game")
def stop_game():
    """
    Stop game - change game_state to stopped
    """
    global game_state
    if game_state != "stopped":
        game_state = "stopped"
        return {"message": "Game stopped."}
    else:
        return Response(content="Game is already stopped.", status_code=400)
