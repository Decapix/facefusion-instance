local :

cd /home/solenopsis/Documents/work-business/barque-postauto/dev/ia-v0.0.1
source .env/bin/activate
cd facefusion-instance
uvicorn api.main:app --reload --port 8010
