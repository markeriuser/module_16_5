from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

users.append(User(id=1, username="UrbanUser ", age=24))
users.append(User(id=2, username="UrbanTest", age=22))
users.append(User(id=3, username="Capybara", age=60))

@app.get("/", response_class=HTMLResponse)
async def Get_Main_Page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User  was not found")

@app.post("/user/{username}/{age}", response_model=User )
async def create_user(username: str = Path(min_length=5, max_length=20, description="Enter username", example= "UrbanUser"),
age: int = Path(ge=18, le=120, description="Enter age", example= "21")):
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User )
async def update_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example= "22"),
username: str = Path(min_length=5, max_length=20, description="Enter username", example= "UrbanUser"),
age: int = Path(ge=18, le=120, description="Enter age", example= "21")):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  was not found")

@app.delete("/user/{user_id}", response_model=User )
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  was not found")

