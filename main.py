from typing import Union

from starlette.middleware.cors import CORSMiddleware

from controllers.sqlcontroller import SQLController
from fastapi import FastAPI
import env

from model.User import User
sql_controller = SQLController(address=f'sqlite:///{env.sql_address}')
print(sql_controller._base.metadata.tables.keys())
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
def createuser(user: User):
    try:
        sql_controller.create_user(user)
        return {"message": "User created successfully"}
    except Exception as e:
        return {"message": str(e)}
