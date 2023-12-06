from fastapi import FastAPI, Request, Depends, Form, HTTPException, Response
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connection import Base, engine, sess_db
from sqlalchemy.orm import Session
from security import get_password_hash, verify_password, create_access_token, verify_token, COOKIE_NAME
from starlette.responses import RedirectResponse
from models import NoteModel
from starlette.responses import HTMLResponse  




from repositoryuser import UserRepository

from models import UserModel

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.post("/store_notes", response_class=HTMLResponse)
def store_notes(request: Request, db: Session = Depends(sess_db), note: str = Form(...)):
    new_note = NoteModel(content=note)

    db.add(new_note)
    db.commit()

    return templates.TemplateResponse("about.html", {"request": request, "success": True})


@app.get("/user/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signupuser")
def signup_user(db: Session = Depends(sess_db), username: str = Form(), email: str = Form(), password: str = Form()):
    print(username)
    print(email)
    print(password)
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"

    signup = UserModel(email=email, username=username, password=get_password_hash(password))
    success = userRepository.create_user(signup)

    if success:
        return "create user successfully"
    else:
        raise HTTPException(
            status_code=401, detail="Credentials not correct"
        )

@app.get("/user/signin")
def login(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

from fastapi.responses import HTMLResponse

@app.post("/signinuser", response_class=HTMLResponse)
def signin_user(response: Response, db: Session = Depends(sess_db), username: str = Form(), password: str = Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"

    if verify_password(password, db_user.password):
        token = create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return RedirectResponse(url="/about", status_code=303)



@app.get('/user/verify/{token}')
def verify_user(token, db: Session = Depends(sess_db)):
    userRepository = UserRepository(db)
    payload = verify_token(token)
    username = payload.get("username")
    db_user = userRepository.get_user_by_username(username)

    if not username:
        raise HTTPException(
            status_code=401, detail="Credentials not correct"
        )
    if db_user.is_active == True:
        return "your account has been already activated"

    db_user.is_active = True
    db_user.commit()
    response = RedirectResponse(url="/user/signin")
    return response
