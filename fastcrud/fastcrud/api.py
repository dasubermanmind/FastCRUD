
import os
from typing import List, Tuple


class Generator:

    # This is the Data access object for interacting with the db
    def generate_model_content(name: str, properties: List[str]):
        props = "\n".join([f"{prop} = Column(String, index=True)" for prop in properties])
        init_section = "\n".join([f"self.{prop} = {prop}" for prop in properties])
        model = f"""
from sqlalchemy import Column, Integer, String
from db.base import Base # DB Base

class {name}(Base):
    __tablename__ = '{name.lower()}s'
    id = Column(Integer, primary_key=True, index=True)
    {props}

    def __init__(self, {','.join(properties)}):
        {init_section}
        """
        return model
    

    # Model from Pydantic to be used for Validation
    def generate_pydantic_model(name: str, properties: List[str]):
        props = "\n".join([prop for prop in properties])
        prop_types = "\n".join([type(prop) for prop in properties])
        model = f"""
from pydantic import BaseModel

class {name}(BaseModel):
    {props}: {prop_types}
        """
        return model
    

    # The actual CRUD Operations
    def generate_crud_content(name: str, properties: List[str]):
        item_args = ", ".join([f"{props}: str" for props in properties])
        item_assign = "\n".join([f"db_item.{prop} = item.{prop}" for prop in properties])
        crud = f"""
from sqlalchemy.orm import Session
from models.{name.lower()} import {name}

# Added Default CRUD Options. Please revise as you see fit. 

def create_{name.lower()}(db: Session, arg: {name}):
    db.add(arg)
    db.commit()
    db.refresh()
    return arg

def get_{name.lower()}(db: Session, arg_id: int):
    return db.query({name}).filter({name}.id == arg_id).first()

def update_{name.lower()}(db: Session, arg_id: int, arg_update: {name}):
    db_arg = db.query({name}).filter({name}.id == arg_id).first()
    if db_arg:
        {item_assign}
        db.commit()
        db.refresh(db_arg)
    return db_arg


def delete_{name.lower()}(db: Session, arg_id: int):
    db_arg = db.query({name}).filter({name}.id == arg_id).first()
    if db_arg:
        db.delete(db_arg)
        db.commit()
    return db_arg
        """
        return crud
    


    def generat_router_content(name: str, properties: List[str]):
        router = f"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.{name.lower()} import {name}
from crud.{name.lower()} import create_{name.lower()}, get_{name.lower()}, 
update_{name.lower()}, delete_{name.lower()}
from db.session import SessionLocal
#from viz impot Viz

router = APIRouter()
#viz = Viz("db_connection_string_here")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@viz.viz
@router.post("/{name.lower()}s/", response_model={name})
def create_item({', '.join([f"{prop}: str" for prop in properties])}, db: Session = Depends(get_db)):
    item = {name}({', '.join([prop for prop in properties])})
    return create_{name.lower()}(db=db, item=item)


#@viz.viz
@router.get("/{name.lower()}s/{{item_id}}", response_model={name})
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_{name.lower()}(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item


#@viz.viz
@router.put("/{name.lower()}s/{{item_id}}", response_model={name})
def update_item(item_id: int, {', '.join([f"{prop}: str" for prop in properties])}, db: Session = Depends(get_db)):
    item = {name}({', '.join([prop for prop in properties])})
    db_item = update_{name.lower()}(db, item=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item

#@viz.viz
@router.delete("/{name.lower()}s/{{item_id}}", response_model={name})
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_{name.lower()}(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item
        """
        return router

    def update_or_create_model(name: str, properties: List[Tuple[str, str]], relationship: List[str]):
        # Search for the model dir for pre-existing models to create
        model_path = os.path.join("models", f"{name.lower().py}")

