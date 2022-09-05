from multiprocessing import context
from uuid import UUID
import uvicorn
from fastapi import FastAPI, Form, status, Request
from typing import Union
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import generate_key
import client

app = FastAPI()
origins = ["https://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory = "templates")

@app.get('/', response_class = "HTMLResponse")
def homepage(request: Request):
    # return templates.TemplateResponse("index.html", context = {'request': request})
    return RedirectResponse("/register-user/", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/register-user/', response_class = "HTMLResponse")
def register(request: Request): 
    return templates.TemplateResponse("register.html", {"request": request})

@app.post('/register-user/', response_class = "HTMLResponse")
def register(request: Request, user_name : str = Form(), user_id: int = Form()):
    print(user_name)
    print(user_id)
    user_exists = generate_key.check_user_exists(user_name, user_id)
    if user_exists == False: 
        generate_key.generate_key(user_name, user_id)
        # redirect to the login user page
        return RedirectResponse("/login-user/", status_code=status.HTTP_303_SEE_OTHER)
    else: 
        # redirect to the login user page
        print("You have already been registered")
        return RedirectResponse("/login-user/", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/login-user/', response_class = "HTMLResponse")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login-user/', response_class = "HTMLResponse")
def login(request: Request, user_name : str = Form(), user_id: int = Form(), signing_key: str = Form(), message: str = Form()):
    print(user_name)
    print(user_id)
    print(message)
    print(signing_key)

    valid = client.user_login(user_name, user_id, message, signing_key)
    if valid == True: 
        # redirect to the organization's website
        return templates.TemplateResponse("organization.html", {"request": request})
    else: 
        print("You cannot login")
        return RedirectResponse("/login-user/", status_code=status.HTTP_303_SEE_OTHER)