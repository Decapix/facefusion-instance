from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from celery_worker import process_video

app = FastAPI()

# Setup pour Jinja2
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_files(request: Request, image: UploadFile = File(...), videos: List[UploadFile] = File(...)):
    image_path = os.path.join("uploads", image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    for video in videos:
        video_path = os.path.join("uploads", video.filename)
        output_path = os.path.join("exec", "result", f"{video.filename}-res.mp4")
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        process_video.delay(image_path, video_path, output_path)

    return templates.TemplateResponse("index.html", {"request": request, "message": "Files uploaded and processing started"})
