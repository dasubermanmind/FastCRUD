
from typing import List


class Generator:
    def generate_model_content(name: str, properties: List[str]):
        props = "\n".join([f"{prop} = Column(String, index=True)" for prop in properties])
        init_section = "\n".join([f"self.{prop} = {prop}" for prop in properties])
        model = f"""
from sqlalchemy import Column, Integer, String
from db.base import Base

class {name}(Base):
    __tablename__ = '{name.lower()}s'
    id = Column(Integer, primary_key=True, index=True)
    {props}

    def __init__(self, {','.join(properties)}):
        {init_section}
        """
        return model

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

    def generat_router_content(name: str, properties: List[str]):
        pass

    
