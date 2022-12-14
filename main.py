from fastapi import FastAPI, Depends
from sqlalchemy.orm import session
from typing import List
import uvicorn
import database
import schemas
import models


app = FastAPI()

def get_database():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def migrate_table():
    return models.Base.metadata.create_all(bind=database.engine)

@app.get('/')
def get_dummy():
    pass

@app.post('/')
def create_usr(request: schemas.User, db: session = Depends(get_database)):
    new_user = models.user(username = request.username, password = request.password, email= request.email)
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user

@app.get('/user', response_model=List[schemas.UserView])
def get_user(db: session = Depends(get_database)):
    return db.query(models.user).all()

if __name__ == '__main__':
	uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)