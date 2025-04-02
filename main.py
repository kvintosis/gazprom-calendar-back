from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from controllers.sqlcontroller import SQLController
import env
from model.LoginCred import LoginCred
from model.jwtBearer import create_access_token
from model.User import User
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
sql_controller = SQLController(address=f'sqlite:///{env.sql_address}')
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
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = LoginCred(login=form_data.username, password=form_data.password)
        sql_controller.login(user)
        access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid credentials"})




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
        return JSONResponse(status_code=200, content={"message": "User created"})
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
