from enum import Enum
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return "HEllo"

@app.get("/items/{item_id}")
async def read_item(item_id : int):
    return {"item_id": item_id}



fake_db = {
    1 : "Kaustubh",
    2 : "Hema",
    3 : "Sara",
    4 : "John",
    5 : "Dom"

}

@app.get("/users")
async def current_user():
    return {"You are the current user"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id : int):
    name = fake_db.get(user_id)
    if name is None:
        raise HTTPException(status_code= 404, detail = "UserID not found")
    return {user_id: name}



class Models(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models")
def get_all_models():
    models = []
    for model in Models:
        models.append(model)
    return models

@app.get("/models/{model_name}")
def which_model(model_name : Models):
    return {"model":model_name}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/item")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


from pydantic import BaseModel


class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

items = []
@app.post("/items")
def create_item(item : Item):
    items.append(item)
    return item

@app.get("/items")
def get_items():
    return items


@app.post("/items/fss")
async def create_items(item : Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
def update_item(item_id : int, item : Item, q : str | None = None):
    result = {"item_id":item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


"""
Q1. A recruiter asks: "What's the difference between a path parameter, query parameter, and request body? When would you use each?"
-> a path parameter goes directly into the url, a query parameter is defined inside of a function, it could be set to default as well, and a request body is a complex info that could not be sent via url so its defined inside an object such as pydantic base model.

Q2. "If I send a POST request with {"age": "25"} to an endpoint expecting age: int, what does FastAPI do with it? What if I send {"age": "hello"}?"
if you send a integer in a string format, fastapi will convert the string into integer but if you send a string where int is required then fastapi will raise a error


Q3. "What is the difference between async def and def in a FastAPI route? Which one would you use if your database library doesn't support await?"
async def tells python to complete other tasks as this will take time to complete, keep coming in between to check upon the task. def is sequential, it finishes a operation and moves forward. If await is not supported then you can simply use def or else write your own function


Q4. "Why should API keys never be hardcoded in your Python files?"
Data leakage is the main reason/


Q5. "A user hits your /resumes/ endpoint and gets a 422 error. What does that mean and what are the possible causes?"
422 means Unprocessable content. The user might have uploaded a wrong format


Q6. Build a POST /users/ endpoint that accepts:

username (required, string)
email (required, string)
age (optional, int)
is_active (bool, defaults to True)

Return the user data plus a field "account_status": "active" if is_active is True, else "inactive".
"""

class User(BaseModel):
    username: str
    email : str
    age : int
    is_active : bool = True


@app.post("/users2/")
def get_user2(user: User):

    return {
    **user.model_dump(),
    "account_status":"active" if user.is_active else "inactive"
    }


"""
Q7. You have this fake DB:
Build a GET /users/ endpoint that:

Returns all users by default
Accepts an optional query parameter role to filter by role
Returns a 404 message if no users match

"""
users_db = {
    1: {"name": "Kaustubh", "role": "admin"},
    2: {"name": "John", "role": "user"},
    3: {"name": "Sara", "role": "user"}
}


@app.get("/fakeusers")
def return_users(q : str | None = None):
    if q:
        matched = []
        for u in users_db.values():
            if u["role"] == q:
                matched.append(u)
        if not matched:
            raise HTTPException(status_code= 404, detail= "User not found")
        return matched
            
    return list(users_db.values())


"""
Q8. What is wrong with this code? Fix it:
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return users_db[user_id]
    
"""
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for u in users_db:
        if u == user_id:
            return u
    raise HTTPException(status_code =404, detail = "User not found")



"""
Q9. Build a PUT /resumes/{resume_id} endpoint that:

Accepts a resume ID from the URL
Accepts updated resume data (name, skills as list of strings, location, ready_to_relocate as bool) from the request body
Accepts an optional query parameter notify: bool -- if True, add "notification": "User has been notified" to the response
"""

class Resumes(BaseModel):
    name : str
    skills : list[str]
    location :str
    ready_to_relocate : bool

resumes_db = {
    1:{
        "name": "Alice Johnson",
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "location": "Berlin",
        "ready_to_relocate": False
    },
    2:{
        "name": "Bob Smith",
        "skills": ["JavaScript", "React", "Node.js", "MongoDB"],
        "location": "Munich",
        "ready_to_relocate": True
    },
    3:{
        "name": "Carol White",
        "skills": ["Machine Learning", "PyTorch", "Scikit-learn", "Python"],
        "location": "Hamburg",
        "ready_to_relocate": True
    },
    4:{
        "name": "David Lee",
        "skills": ["Java", "Spring Boot", "Kubernetes", "AWS"],
        "location": "Frankfurt",
        "ready_to_relocate": False
    },
    5:{
        "name": "Eva Müller",
        "skills": ["Data Engineering", "Spark", "Airflow", "SQL"],
        "location": "Berlin",
        "ready_to_relocate": False
    }
}


@app.put("/resumes/{resume_id}")
def update_resume_by_id(resume_id : int, resume : Resumes, notify : bool | None = None):

    if resume_id in resumes_db:
        resumes_db[resume_id] = resume.model_dump()

        if notify:
            response = {**resumes_db[resume_id],"notification": "User has been notified"}
            return response

        return resumes_db[resume_id] 


    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    




@app.post("/users2/")
def user(user: User):

    return {
    **user.model_dump(),
    "account_status":"active" if user.is_active else "inactive"
    }




"""
Q10. A junior developer on your team writes this:
"""


# class UserUpdate(BaseModel):
#     username: str
#     email: str
#     age: int
#     location: str
#     skills: list

# @app.put("/users/{user_id}")
# async def update_user(user_id: int, user: UserUpdate):
#     db.update(user_id, user)
#     return {"message": "Updated"}

"""
Review:
1. Why async def?? It should not execute before moving ahead
2. how is the user going to update?? Its a Pydantic object not a dictionary, first need to convert into a dict. Use model_dump(). Biggest flag in the code
3. What if user updates something wrong or maybe a wrong field by mistake? How will he know? return whats being updated.
4. skills: list should be list[str]
"""


"""
Q1.
Build a GET /resumes/ endpoint that returns all resumes from resumes_db. 
Accept an optional query parameter location: str — if provided, return only resumes from that city.location
"""

@app.get("/resumes")
def get_resumes(location : str | None = None):
    list_of_resumes = []

    for key, value in resumes_db.items():
        response = {"id":key, **value}
        if location:
            if location == response["location"]:
                list_of_resumes.append(response)
        elif not location:
            list_of_resumes.append(response)
    if not list_of_resumes:
        raise HTTPException(status_code=404, detail="Location not found")

    return list_of_resumes


"""
Q2.

Build a GET /resumes/{resume_id} endpoint that returns a single resume by ID.
 If not found, raise a 404. If found, also add a field "total_skills" with the count of skills in the response.
"""

@app.get("/resumes/{resume_id}")
def get_resume_by_id(resume_id : int):
    if resume_id in resumes_db:
        total_skills= 0
        for skill in resumes_db[resume_id]["skills"]:
            total_skills +=1
        return {**resumes_db[resume_id],"total_skills" : total_skills}
    
    raise HTTPException(status_code=404,detail="Not a valid user id")
        

"""
Q3.

Build a DELETE /resumes/{resume_id} endpoint that removes a resume from resumes_db. 
If not found, raise a 404. Return {"message": "Resume deleted successfully"} on success.
"""

@app.delete("/resumes/{resume_id}")
def delete_resume(resume_id : int):
    if resume_id in resumes_db:
        del resumes_db[resume_id]
        return {"message": "Resume deleted successfully"}
    else:
        raise HTTPException(status_code= 404, detail = "Resume not found")

"""
Q4.

Build a POST /resumes/ endpoint that adds a new resume to resumes_db. 
The request body should only accept (name, skills, location, ready_to_relocate) — no id. 
Auto-generate the id as max(resumes_db.keys()) + 1. Return the created resume including the generated id.
"""

@app.post("/resumes/add_resume")
def create_new_resume(resume : Resumes):
    # If user already exists, warning
    response = resume.model_dump()
    for r in resumes_db.values():
        if response["name"] == r["name"]:
            raise HTTPException(status_code= 409, detail="User already exists")

    new_id = max(resumes_db.keys())+1
    resumes_db[new_id] = response

    return {"id":new_id, **response}


"""
Q5.

Refactor Q4 and the PUT endpoint from our session to use two separate models —
ResumeCreate for the request body and ResumeResponse for the response, as discussed in the production pattern. 
Use response_model=ResumeResponse on both endpoints.
"""

class ResumeCreate(BaseModel):
    name : str
    skills : list[str]
    location : str
    ready_to_relocate : bool

class ResumeResponse(BaseModel):
    id : int
    name : str
    skills : list[str]
    location : str
    ready_to_relocate : bool


@app.post("/resumes/", response_model = ResumeResponse)
def create_resume(resume : ResumeCreate):
    response = resume.model_dump()
    for r in resumes_db.values():
        if response["name"] == r["name"]:
            raise HTTPException(status_code=409, detail="Resume already exists")
        
    new_id = max(resumes_db.keys()) + 1
    resumes_db[new_id] = response
    return {"id" : new_id, **response}


@app.put("/resumes/{resume_id}", response_model = ResumeResponse)
def update_resume(resume : ResumeCreate, resume_id : int):
    response = resume.model_dump()
    if resume_id in resumes_db:
        resumes_db[resume_id] = response
        return {"id": resume_id, **response}
    
    else:
        raise HTTPException(status_code= 404, detail="resume not found")