import jwt
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from jwt import InvalidTokenError
from fastapi.responses import RedirectResponse, JSONResponse
from controllers.sqlcontroller import AsyncSQLController
import env
from model.jwtBearer import create_access_token
from model.User import User
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
sql_controller = AsyncSQLController(address=f'sqlite+aiosqlite:///{env.sql_address}')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.post("/login")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        await sql_controller.login(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=access_token_expires
        )

        # Установка cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,  # Для HTTPS. В разработке можно `secure=False`
            samesite="lax",
            max_age=1800
        )
        return {"message": "Login successful"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return login


@app.get("/events")
async def read_calendar(current_user: str = Depends(get_current_user)):
    pass


@app.get("/employees")
async def read_employees(current_user: str = Depends(get_current_user)):
    try:
        await sql_controller.get_all_events(current_user)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/adminboard/createuser")
async def create_user(user: User):
    try:
        await sql_controller.create_user(user)
        return JSONResponse(status_code=200, content={"message": "User created"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=404, content={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
