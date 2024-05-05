from celery import Celery
import subprocess

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_video(image_path, video_path, output_path):
    command = [
        "python", "run.py", "--headless",
        "--source", image_path,
        "--target", video_path,
        "--output", output_path
    ]
    try:
        subprocess.run(command, check=True)
        print("Video processed successfully.")
        # Vous pouvez ici ajouter le code pour uploader le fichier à Google Drive
    except subprocess.CalledProcessError as e:
        print("Failed to process video:", e)
