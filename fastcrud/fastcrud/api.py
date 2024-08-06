
import os
from typing import List, Optional, Tuple


class Generator:
    def generate_model_content(name: str, properties: List[str], relationship: Optional[List[str]]):
        props = "\n".join([f"{prop} = Column({ptype}, index=True)" for prop, ptype in properties])
        added_relationship = "\n".join([f"{rel}_id = Columns(Integer, ForeignKey('{rel.lower()}.id'))
                                  \n{rel} = relationship('{rel}')" for rel in relationship])
        init_args = ", ".join([prop for prop, _ in properties] + [f"{rel}_id" for rel in relationship])
        init_section = "\n".join([f"self.{prop} = {prop}" for prop, _ in properties] + f"self.{rel}_id = {rel}_id" for rel in relationship)
        model = f"""
from sqlalchemy import Column, Integer, String
from db.base import Base

class {name}(Base):
    __tablename__ = '{name.lower()}s'
    id = Column(Integer, primary_key=True, index=True)
    {props}
    {added_relationship}

    def __init__(self, {init_args}):
    {init_section}
        """
        return model
    # Update
    def generate_crud_content(name: str,properties: List[str]):
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
    # update
    def generat_router_content(name: str, properties: List[str]):
        router = f"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.{name.lower()} import {name}
from crud.{name.lower()} import create_{name.lower()}, get_{name.lower()}, 
update_{name.lower()}, delete_{name.lower()}
from db.session import SessionLocal
from viz impot Viz

router = APIRouter()
viz = Viz("db_connection_string_here")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@viz.viz
@router.post("/{name.lower()}s/", response_model={name})
def create_item({', '.join([f"{prop}: str" for prop in properties])}, db: Session = Depends(get_db)):
    item = {name}({', '.join([prop for prop in properties])})
    return create_{name.lower()}(db=db, item=item)


@viz.viz
@router.get("/{name.lower()}s/{{item_id}}", response_model={name})
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_{name.lower()}(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item


@viz.viz
@router.put("/{name.lower()}s/{{item_id}}", response_model={name})
def update_item(item_id: int, {', '.join([f"{prop}: str" for prop in properties])}, db: Session = Depends(get_db)):
    item = {name}({', '.join([prop for prop in properties])})
    db_item = update_{name.lower()}(db, item=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item

@viz.viz
@router.delete("/{name.lower()}s/{{item_id}}", response_model={name})
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_{name.lower()}(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, details="Not Found")
    
    return db_item
        """
        return router

    def update_or_create_model(name: str, properties: List[Tuple[str, str]], relationship: List[str]):
        # Search for the model dir for pre-existing models to create a relationship with
        model_path = os.path.join("models", f"{name.lower().py}")

