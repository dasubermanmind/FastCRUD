

import os
import typer

app = typer.Typer()


@app.command()
def model(name: str):
    name = name.capitalize()
    # TODO: Update both
    model_path = os.path.join("models", f"{name.lower()}.py")
    with open(model_path, "w") as f:
        f.write(model_created)
    print(f"Model Created: {name} at {model_path}")

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



