from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
import shutil
import os
from fastapi.responses import HTMLResponse
import subprocess
from fastapi import BackgroundTasks
from typing import List
from fastapi.responses import FileResponse
import requests
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, BackgroundTasks

# rajouter une authentification serveur

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR_CONTROLLER =  Path(__file__).resolve().parent

def process_video(image_path, video_path, output_path):
    os.chdir(BASE_DIR)  # Change le répertoire de travail
    command = [
        "python", "run.py", "--headless",
        "--source",  image_path,
        "--target",  video_path,
        "--output", output_path
    ]

    try:
        subprocess.run(command, check=True)
        print("Video processed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to process video:", e)
        raise HTTPException(status_code=500, detail="Video processing failed.")


def cleanup_files(*paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)



def send_callback(output_path, video_path, image_path, callback_url):
    with open(output_path, "rb") as f:
        files = {"video": f.read()}
        response = requests.post(callback_url, files=files)
        cleanup_files(output_path)  # Cleanup after callback
        cleanup_files(video_path)
        cleanup_files(image_path)
        if response.status_code != 200:
            print("Failed to send processed video")

@app.post("/upload/")
async def receive_and_process(background_tasks: BackgroundTasks, image: UploadFile = File(...), video: UploadFile = File(...), callback_url: str = Form(...), key: str = Form(...)):
    keytrue = "labarquedesrapteux-jsuisdansmaparanioa"
    if key != "labarquedesrapteux-jsuisdansmaparanioa" :
        raise HTTPException(status_code=404, detail="Invalid key")
    image_path = os.path.join("uploads", BASE_DIR_CONTROLLER / "uploads" / f"{image.filename}.png")
    video_path = os.path.join("uploads", BASE_DIR_CONTROLLER / "uploads" / f"{video.filename}.mp4") 
    output_path = os.path.join("results", BASE_DIR_CONTROLLER / "results" / f"{video.filename}-processed.mp4")

    with open(image_path, "wb") as image_file:
        shutil.copyfileobj(image.file, image_file)
    with open(video_path, "wb") as video_file:
        shutil.copyfileobj(video.file, video_file)

    background_tasks.add_task(process_video, image_path, video_path, output_path)
    background_tasks.add_task(send_callback, output_path, video_path, image_path, callback_url)

    return {"message": "Files received, processing will begin shortly."}


