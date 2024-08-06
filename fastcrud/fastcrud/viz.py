from sqlalchemy import inspect, create_engin
from functools import wraps
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os


class Viz:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def generate_erd(self, output_path: str):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        data = []

        for table in tables:
            columns = inspector.get_columns(table)
            for column in columns:
                data.append({"table": table, "column": column["name"]})

        df = pd.DataFrame(data)
        plt.figure(figsize=(12,10))
        sns.set_theme(style='whitegrid')
        g = sns.scatterplot(x="Table", y="Column", hue="type", data=df)
        g.set_title("Custom ERD")
        plt.savefig(output_path)

    def viz(self, endpoint):
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            output_path = "erd.png"
            self.generate_erd(output_path)
            return endpoint(*args, **kwargs)
        return wrapper


