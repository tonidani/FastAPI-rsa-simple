from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from schemas import Message

import secrets
from rsa import Rsa


app = FastAPI()
security = HTTPBasic()


def get_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "toni")
    correct_password = secrets.compare_digest(credentials.password, "123")
    if not (correct_password and correct_username):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-authenticate": "Basic"},
        )

    return credentials.username


@app.get("/")
def read_root(username: str = Depends(get_authenticated)) -> str:
    if username.status_code == 401:
        content = 'You are unauthorized to use this endpoint!'
        return HTMLResponse(content=content, status_code=401)
    content = '<form method="post"><p> Podaj text aby zaszyfrować </p> <input type="textarea" name="message"/><input type="submit"/></form>'
    return HTMLResponse(content=content, status_code=200)

@app.post("/")
def read_form(message: str = Form(...), username: str = Depends(get_authenticated)):

    if username.status_code == 401:
        content = 'You are unauthorized to use this endpoint!'
        return HTMLResponse(content=content, status_code=401)

    rsa = Rsa()
    encrypted = rsa.encrypt_RSA(message, rsa.private_key)
    decrypted = rsa.decrypt_RSA(encrypted, rsa.public_key)
    username = username

    info = "message: {} | {} | {} | {}".format(message, encrypted, username, decrypted)

    content = '<form method="post"><p> Podaj text aby zaszyfrować </p> <input type="textarea" name="message" required/><input type="submit"/></form> <br> {}'.format(info)

    return HTMLResponse(content=content, status_code=200)

@app.post("/api/encode/")
def endcode(message: Message, username: str = Depends(get_authenticated)):

    if username.status_code == 401:
        content = 'You are unauthorized to use this endpoint!'
        return {content : username.status_code}

    encrypted = Rsa().encrypt_RSA(message.message, Rsa().private_key)

    message.username = username
    message.message = encrypted
    message.public_key = Rsa().public_key
    message.private_key = Rsa().private_key

    return message


@app.post("/api/decode/")
def decode(message: Message, username: str = Depends(get_authenticated)):
    if username.status_code == 401:
        content = 'You are unauthorized to use this endpoint!'

    if not message.public_key:
        return 'No public_key given, impossible to decode'

    decrypted = Rsa().decrypt_RSA(message.message, message.public_key)
    return decrypted

