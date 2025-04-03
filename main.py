import jwt
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from controllers.sqlcontroller import AsyncSQLController
import env
from model.Dto_Event import Dto_Event
from model.Dto_Event import EventCreate
from model.jwtBearer import create_access_token
from model.User import User
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
origins = [
    env.url
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

sql_controller = AsyncSQLController(address=f'sqlite+aiosqlite:///{env.sql_address}')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.post("/login")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_exists = await sql_controller.login(form_data.username, form_data.password)
        if not user_exists:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
        role = await sql_controller.get_role(form_data.username)
        access_token = create_access_token(
            data={"sub": role},
            expires_delta=access_token_expires
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Для HTTPS. В разработке можно `secure=False`
            samesite="none",
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

# Проверка текущего пользователя
def get_current_user(token: Annotated[str | None, Cookie(alias="access_token")] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        role = payload.get("sub")
        if role is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    return role

# Остальные эндпоинты остаются без изменений
@app.get("/events")
async def read_event(_ = Depends(get_current_user)):
    try:
        event = await sql_controller.get_all_events()
        return event
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка при получении событий"}
        )

@app.get("/employees")
async def read_employees(_ = Depends(get_current_user)):
    try:
        employees = await sql_controller.get_all_employers()
        return employees
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка при получении сотрудников"}
        )

@app.post("/adminboard/createevent")
async def create_event(event: Dto_Event):
    try:
        await check_admin()
        await sql_controller.create_event(event)
        return JSONResponse(status_code=200, content={"message": "Event created"})
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})

@app.post("/adminboard/createevent")
async def create_event(event: EventCreate, role: str = Depends(get_current_user)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Только администратор может создавать события"
        )
    try:
        new_event = await sql_controller.create_event(event)
        return new_event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/adminboard/")
async def check_admin(role: str = Depends(get_current_user)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    pass

@app.delete("/adminboard/deleteevent/{event_id}")
async def delete_event(event_id: int, role: str = Depends(get_current_user)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Только администратор может удалять события"
        )
    try:
        await sql_controller.delete_event(event_id)
        return JSONResponse(status_code=200, content={"message": "Event deleted"})
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
