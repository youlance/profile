from datetime import date
from enum import Enum
from os import stat, environ
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, EmailStr, FilePath, Field
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Gender(str, Enum):
    male = 'Male'
    female = 'Female'
    other = 'Other'
    not_given = 'not_given'


class Profile(BaseModel):
    username: str
    name: str
    gender: Gender = Field("not_given", alias='gender')
    email: EmailStr
    profile_picture: Optional[str] = None
    birthdate: date


pwd = environ.get("YOULANCE")

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='profiles', user='postgres', password=pwd,
                                      cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connection successful!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)


@app.get("/profiles")
async def get_profiles():
    cursor.execute(""" SELECT * FROM profiles """)
    profiles = cursor.fetchall()
    return {"Profiles": profiles}


@app.post("/profiles", status_code=status.HTTP_201_CREATED)
async def pos(profile: Profile):
    cursor.execute(
        """INSERT INTO profiles (username,name,email,gender,birthdate,picture) VALUES (%s,%s,%s,%s,%s,%s) RETURNING * 
        """,
        (profile.username, profile.name, profile.email, profile.gender, profile.birthdate, profile.profile_picture))
    new_profile = cursor.fetchone()
    connection.commit()
    return {"data": new_profile}


@app.get("/profiles/{user}")
async def get_profile(user: str):
    cursor.execute("""SELECT * FROM profiles WHERE username = %s""", (user,))
    profile = cursor.fetchone()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{user} was not found!")

    return {"profile": profile}


@app.delete("/profiles/{user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(user: str):
    cursor.execute("""DELETE FROM profiles WHERE username = %s RETURNING *  """, (user,))
    deleted_profile = cursor.fetchone()
    connection.commit()
    if not deleted_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{user} was not found!")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/profiles/{user}")
async def update_profile(user: str, profile: Profile):
    cursor.execute(
        """UPDATE profiles SET username = %s, name = %s, email = %s, gender = %s, birthdate = %s, picture = %s WHERE 
        username= %s RETURNING * """,
        (profile.username, profile.name, profile.email, profile.gender, profile.birthdate, profile.profile_picture,
         user))
    updated_profile = cursor.fetchone()
    connection.commit()
    if not updated_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{user} was not found!")
    return {'profile': updated_profile}