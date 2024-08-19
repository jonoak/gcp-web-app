import time

from fastapi import FastAPI
from google.cloud import storage
from google.cloud import aiplatform
import docker
from circleci.api import Api as Circleci

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/gcs-buckets")
def list_gcs_buckets():
    client = storage.Client()
    buckets = list(client.list_buckets())
    bucket_names = [bucket.name for bucket in buckets]
    return {"buckets": bucket_names}

@app.get("/vertex-ai-models")
def list_vertex_ai_models():
    aiplatform.init()
    models = aiplatform.Model.list()
    model_names = [model.display_name for model in models]
    return {"models": model_names}

@app.get("/docker-images")
def list_docker_images():
    client = docker.from_env()
    images = client.images.list()
    image_tags = [image.tags for image in images]
    return {"docker_images": image_tags}

@app.post("/trigger-circleci-build")
def trigger_circleci_build(project_slug: str):
    token = "YOUR_CIRCLECI_TOKEN"
    circleci = Circleci(token=token)
    response = circleci.trigger_pipeline(project_slug=project_slug)
    return {"response": response}