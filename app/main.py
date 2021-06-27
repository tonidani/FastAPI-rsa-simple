from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse

import secrets

from utils.rsa import Rsa
from schemas import Message
import config

app = FastAPI()
security = HTTPBasic()


def get_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username,  config.USER)
    correct_password = secrets.compare_digest(credentials.password, config.USER_PASSW)
    if not (correct_password and correct_username):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-authenticate": "Basic"},
        )

    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="You are authenticated",
        headers={"WWW-authenticate": "Basic",
                 "username": credentials.username},

    )


@app.get("/")
async def read_root(state: str = Depends(get_authenticated)) -> str:
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        return HTMLResponse(content=content, status_code=401)

    content = '<form method="post"><p> Enter text to encrypt </p> <input type="textarea" name="message"/><input ' \
              'type="submit"/></form> '
    return HTMLResponse(content=content, status_code=200)


@app.post("/")
async def read_form(message: str = Form(...), state: str = Depends(get_authenticated)):
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        return HTMLResponse(content=content, status_code=401)

    rsa = Rsa()
    encrypted = rsa.encrypt_RSA(message, rsa.private_key)
    decrypted = rsa.decrypt_RSA(encrypted, rsa.public_key)
    username = state.headers['username']

    info = "message: {} | encrypted: {} | username: {} | pub_key {}".format(message, encrypted, username, rsa.public_key)

    content = '<form method="post"><p>Enter text to encrypt  </p> <input type="textarea" name="message" ' \
              'required/><input type="submit"/></form> <br> {}'.format(info)

    return HTMLResponse(status_code=200, content=content)


@app.post("/api/encode/")
async def encode(message: Message, state: str = Depends(get_authenticated)):
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        raise HTTPException(status_code=401, detail=content)

    if message.message == "":
        content = 'No message given, impossible to encode'
        raise HTTPException(status_code=422, detail=content)

    rsa = Rsa()
    encrypted = rsa.encrypt_RSA(message.message, rsa.private_key)

    message.username = state.headers["username"]
    message.message = encrypted
    message.public_key = rsa.public_key
    message.private_key = rsa.private_key

    return message


@app.get("/api/encode/")
async def read_root(state: str = Depends(get_authenticated)) -> str:
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        raise HTTPException(status_code=401, detail=content)

    return 'Send your text in this format {"message" : "textoencrypt"} '


@app.post("/api/decode/")
async def decode(message: Message, state: str = Depends(get_authenticated)):
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        raise HTTPException(status_code=401, detail=content)

    if message.message == "":
        content = 'No message given, impossible to decode'
        raise HTTPException(status_code=422, detail=content)

    if not message.public_key:
        content = 'No public_key given, impossible to decode'
        raise HTTPException(status_code=422, detail=content)

    decrypted = Rsa().decrypt_RSA(message.message, message.public_key)

    message.username = state.headers["username"]
    message.message = decrypted

    return message


@app.get("/api/decode/")
async def read_root(state: str = Depends(get_authenticated)) -> str:
    if state.status_code == 401:
        content = 'You are not authorized to use this endpoint!'
        raise HTTPException(status_code=401, detail=content)

    return 'Send your text and public_key in this format {"message" : "textoencrypt", "private_key" : { "key": int, ' \
           '"n": int} } '
