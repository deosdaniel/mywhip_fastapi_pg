import pandas as pd
from sqlalchemy import select, delete
from sqlmodel import Session, create_engine
from src.directories.models import MakesDirectory, ModelsDirectory

engine = create_engine("postgresql://postgres:rootroot@localhost:5432/my_whip")


def insert_makes():
    df = pd.read_csv("make_model_dataset.csv")
    df_makes = df.drop("model", axis=1)
    df_makes = df_makes.drop_duplicates(subset="make")
    df_makes = df_makes.reset_index(drop=True)
    with Session(engine) as session:
        try:
            for _, row in df_makes.iterrows():
                make = MakesDirectory(make=row["make"])
                session.add(make)
            session.commit()
        except Exception as e:
            print(e)


def insert_models():
    with Session(engine) as session:
        makes = session.exec(select(MakesDirectory.uid, MakesDirectory.make)).all()
        make_to_uid = {make: uid for uid, make in makes}
        df = pd.read_csv("make_model_dataset.csv")
        try:
            df["make_uid"] = df["make"].map(make_to_uid)
        except Exception as e:
            print(e)
        try:
            for _, row in df.iterrows():
                model = ModelsDirectory(
                    model=row["model"],
                    make_uid=row["make_uid"],
                )
                session.add(model)
            session.commit()
        except Exception as e:
            print(e)


def clear_directories():
    with Session(engine) as session:
        session.exec(delete(ModelsDirectory))
        session.exec(delete(MakesDirectory))
        session.commit()


if __name__ == "__main__":
    clear_directories()
    insert_makes()
    insert_models()
