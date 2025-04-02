from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.post("/login")
def read_root():
    return {"Hello": "World"}


@app.get("/calendar")
def read_calendar():
    pass
@app.get("/employees")
def read_employees():
    pass
@app.get("/adminboard")
def read_adminboard():
    pass