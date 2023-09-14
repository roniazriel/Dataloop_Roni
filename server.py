from fastapi import FastAPI, Response, Body
import time

app = FastAPI()

pong_time_ms = None
game_state = "stopped"

@app.get("/ping")
def ping():
    if game_state == "running":
        time.sleep(pong_time_ms / 1000)  # Sleep for pong_time_ms milliseconds
        return {"message": "pong"}
    else:
        return Response(content="Game is not running.", status_code=400)

@app.post("/set_pong_time")
def set_pong_time(ms: int):
    global pong_time_ms
    pong_time_ms = ms
    return {"message": f"Pong time set to {ms} milliseconds."}

@app.post("/start_game")
def start_game(ms: int = Body(..., embed=True)):
    global game_state
    if game_state == "stopped":
        game_state = "running"
        set_pong_time(ms)
        return {"message": f"Game started with {ms} milliseconds between pongs."}
    else:
        return Response(content="Game is already running.", status_code=400)

@app.post("/pause_game")
def pause_game():
    global game_state
    if game_state == "running":
        game_state = "paused"
        return {"message": "Game paused."}
    else:
        return Response(content="Game is not running.", status_code=400)

@app.post("/resume_game")
def resume_game():
    global game_state
    if game_state == "paused":
        game_state = "running"
        return {"message": "Game resumed."}
    else:
        return Response(content="Game is not paused.", status_code=400)

@app.post("/stop_game")
def stop_game():
    global game_state
    if game_state != "stopped":
        game_state = "stopped"
        return {"message": "Game stopped."}
    else:
        return Response(content="Game is already stopped.", status_code=400)

