from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import time



#creating an instance of fastapi
app = FastAPI()

#post validation
class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:Optional[int] = None
   
   
my_post = [{"title" : "title of post 1", "content":"content of post 1", "id":1},
           {"title":"types of food", "content": "i love pizza","id":2}]

#connecting to a database
while True:
    try:
        
        cursor =conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("connection failed")
        print(f"error was {error}")
        time.sleep(3)

def find_post(id):
    for p in my_post:
        if p["id"]==id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] ==id:
            return i

@app.get("/")
def root():
    return {"data":"my page"}

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts =cursor.fetchall()
    return {"data": posts}
#fetching one post
@app.get("/posts/{id}")
def get_postid(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()   
    return {"data ": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post {id} already deleted")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title =%s, content = %s, published = %s WHERE id =%s RETURNING *""",
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return{'data' : updated_post}





