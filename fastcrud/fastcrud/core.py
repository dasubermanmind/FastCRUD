

import os
from typing import List
import typer

from api import Generator


app = typer.Typer()


@app.command()
def model(name: str):
    genny = Generator()
    name = name.capitalize()
    model_created = genny.generate_model_content()
    model_path = os.path.join("models", f"{name.lower()}.py")
    
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

    crud_path = os.path.join("crud", f"{name.lower()}.py")
    crud_actions = genny.generate_crud_content()

    with open(crud_path, "w") as f:
        f.write(crud_actions)
    print(f'Crud Created: {name.lower()} at {crud_path}')
    print("\nEnjoy!\n")


@app.command()
def scaffold(name: str, properties: List[str]=typer.Option([], "--property", "-p")):
    genny = Generator()
    name = name.capitalize()
    model_created = genny.generate_model_content(name, properties)
    model_path = os.path.join("models", f"{name.lower()}.py")
    
    # Model
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

    # Crud
    crud_path = os.path.join("crud", f"{name.lower()}.py")
    crud_actions = genny.generate_crud_content(name, properties)

    with open(crud_path, "w") as f:
        f.write(crud_actions)
    print(f'Crud Created: {name.lower()} at {crud_path}')

    # Router
    router_path = os.path.join("routers", f"{name.lower()}.py")
    router_actions = genny.generat_router_content(name, properties)

    with open(router_path, "w") as f:
        f.write(router_actions)
    print(f'Router Created: {name.lower()} at {router_path}')
    print("Don't forget to include this to your Main.py")


@app.command()
def router(name: str, properties: List[str]=typer.Option([], "--property", "-p")):
    genny = Generator()
    name = name.capitalize()

    router_path = os.path.join("routers")
    # only create non-model routes
    #router_actions = genny.only_routers(name, properties)
    # with open(router_path, "w") as f:
    #     f.write(router_actions)
    # print(f'Router Created: {name.lower()} at {router_path}')


@app.command()
def py_model(name: str, properties: List[str]=typer.Option([], "--property", "-p")):
    genny = Generator()
    name = name.capitalize()
    # Only create pydantic models
    py_model_path = os.path.join("models")
    py_actions = genny.generate_pydantic_model(name, properties)
    with open(py_model_path, "w") as f:
        f.write(py_actions)
    print(f"Model Created: {name} at {py_model_path}")


@app.command()
def start():
    pass
    # Gives you boilerplate FastAPI
