

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
def all(name: str, properties: List[str]=typer.Option([], "--property", "-p")):
    genny = Generator()
    name = name.capitalize()
    model_created = genny.generate_model_content()
    model_path = os.path.join("models", f"{name.lower()}.py")
    
    # Model
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

    crud_path = os.path.join("crud", f"{name.lower()}.py")
    crud_actions = genny.generate_crud_content()

    with open(crud_path, "w") as f:
        f.write(crud_actions)
    print(f'Crud Created: {name.lower()} at {crud_path}')

    # Crud
    model_created = genny.generate_model_content()
    model_path = os.path.join("models", f"{name.lower()}.py")
    
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

    # Router
    router_path = os.path.join("routers", f"{name.lower()}.py")
    router_actions = genny.generat_router_content()

    with open(router_path, "w") as f:
        f.write(router_actions)
    print(f'Router Created: {name.lower()} at {router_path}')
    print("Don't forget to include this to your Main.py")



