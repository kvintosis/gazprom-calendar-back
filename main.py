from typing import Union

from starlette.middleware.cors import CORSMiddleware

from controllers.sqlcontroller import SQLController
from fastapi import FastAPI
import env

from model.User import User
sql_controller = SQLController(address='sqlite:///' + env.sql_address)
app = FastAPI()
origins = [
    env.url
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/login")
def read_root():
    return {"Hello": "World"}


@app.get("/events")
def read_calendar():
    pass
@app.get("/employees")
def read_employees():
    pass
@app.post("/adminboard/createuser")
def read_adminboard(user: User):
    pass