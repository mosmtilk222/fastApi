#Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

#Uvicorn
import uvicorn

app = FastAPI()

#Models
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):

    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)
    
#Paths

##Users

@app.post(
  path="/signup",
  response_model=User,
  status_code=status.HTTP_201_CREATED,
  summary="Register a User",
  tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
  """"
  Signup

  This Path operation register a user in the app
    
  Parameters:
    -Request body parameter:
      - user: UserRegister

  Returns a json with the basic tweet information:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime

  """
  with open("users.json", "r+", encoding="utf-8") as f:
    results = json.loads(f.read())
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    results.append(user_dict)
    f.seek(0)
    f.write(json.dumps(results))

    return user

@app.post(
  path="/login",
  response_model=User,
  status_code=status.HTTP_200_OK,
  summary="Login a User",
  tags=["Users"]
)
def login():
  pass

@app.get(
  path="/users",
  response_model=List[User],
  status_code=status.HTTP_200_OK,
  summary="Show all users",
  tags=["Users"]
)
def show_all_users():
  """
  This path operation shows all users in the app

  Parameters:
    -
  
  Returns a JSON list with all users in the app, with the following keys:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
  """

  with open("users.json", "r", encoding="utf-8") as f:
    results = json.loads(f.read())
    return results

@app.get(
  path="/users/{user_id}",
  response_model=User,
  status_code=status.HTTP_200_OK,
  summary="Show a User",
  tags=["Users"]
)
def show_a_user():
  pass

@app.delete(
  path="/users/{user_id}/delete",
  response_model=User,
  status_code=status.HTTP_200_OK,
  summary="Delete a User",
  tags=["Users"]
)
def delete_a_user():
  pass

@app.put(
  path="/users/{user_id}/update",
  response_model=User,
  status_code=status.HTTP_200_OK,
  summary="Update a User",
  tags=["Users"]
)
def update_a_user():
  pass

##Tweets

@app.get(
  path="/",
  response_model=List[Tweet],
  status_code=status.HTTP_200_OK,
  summary="Get all tweets",
  tags=["Tweets"]
)
def home():
  """
  This path operation shows all tweets in the app

  Parameters:
    -
  
  Returns a JSON list with all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
  """

  with open("tweets.json", "r", encoding="utf-8") as f:
    results = json.loads(f.read())
    return results

@app.post(
  path="/post",
  response_model=Tweet,
  status_code=status.HTTP_201_CREATED,
  summary="Post a tweet",
  tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
  """"
  Post a Tweet

  This Path operation publish a tweet in the app
    
  Parameters:
    -Request body parameter:
      - tweet: Tweet

  Returns a json with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
  """
  with open("tweets.json", "r+", encoding="utf-8") as f:
    results = json.loads(f.read())
    tweet_dict = tweet.dict()
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
    tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

    results.append(tweet_dict)
    f.seek(0)
    f.write(json.dumps(results))

    return tweet

@app.get(
  path="/tweets/{tweet_id}",
  response_model=Tweet,
  status_code=status.HTTP_200_OK,
  summary="Show a tweet",
  tags=["Tweets"]
)
def show_a_tweet():
  pass

@app.delete(
  path="/tweets/{tweet_id}/delete",
  response_model=Tweet,
  status_code=status.HTTP_200_OK,
  summary="Delete a tweet",
  tags=["Tweets"]
)
def delete_a_tweet():
  pass

@app.delete(
  path="/tweets/{tweet_id}/update",
  response_model=Tweet,
  status_code=status.HTTP_200_OK,
  summary="Update a tweet",
  tags=["Tweets"]
)
def update_a_tweet():
  pass

if __name__ == '__main__':
  uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)