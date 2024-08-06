

import os
import typer

app = typer.Typer()


@app.command()
def model(name: str):
    name = name.capitalize()
    model_created = f"""
from sqlalchemy import Column, Integer, Stringg
from db.base import Base

class {name}(Base):
    __tablename__ = '{name.lower()}s'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    """
    model_path = os.path.join("models", f"{name.lower()}.py")
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

    crud_actions = f"""
from sqlalchemy.orm import Session
from models.{name.lower()} import {name}

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
        db_arg.name = arg_udpate
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
    crud_path = os.path.join("crud", f"{name.lower()}.py")
    with open(crud_path, "w") as f:
        f.write(crud_actions)
    print(f'Crud Created: {name.lower()} at {crud_path}')

    # Update the main>?
    # if db_arg:
    #     db_arg.name = arg_udpate
    #     db.commit()
    #     db.refresh(db_arg)
    # return db_arg



