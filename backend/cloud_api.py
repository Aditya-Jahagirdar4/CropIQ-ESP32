from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response

app = FastAPI()
latest_image = None
command = {"spray": 0, "amount": 0}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    global latest_image
    latest_image = await file.read()
    return {"status": "received"}

@app.get("/get_image")
async def get_image():
    return Response(content=latest_image, media_type="image/jpeg")

@app.post("/command")
async def set_command(cmd: dict):
    global command
    command = cmd
    return {"status": "command_set"}

@app.get("/get_command")
async def get_command():
    return command

