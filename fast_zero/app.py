from fastapi import FastAPI

app = FastAPI()


@app.get('/')  # expões nossa função para ser servida pelo FastAPI
def read_root():
    return {'message': 'Hello world!'}
