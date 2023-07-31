from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel



#creating an instance of fastapi
app = FastAPI()

#post validation
class Post(BaseModel):
    title:str
    content:str
    published:bool = True
   

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/post")
def get_post():
    return {"social media posts"}

@app.post("/createpost")
def post(new_post:Post):
    print(new_post)
    return {"data : new post"}