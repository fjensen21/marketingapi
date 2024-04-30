from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return "Hello to the world, time for an Action"
