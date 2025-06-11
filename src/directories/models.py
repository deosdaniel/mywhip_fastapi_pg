from sqlmodel import Field, Column, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
from sqlalchemy import text


class MakesDirectory(SQLModel, table=True):
    __tablename__ = "makesdir"
    uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        )
    )
    make: str = Field(nullable=False)

    models: list["ModelsDirectory"] = Relationship(
        back_populates="make",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True,
    )

    def __repr__(self):
        return f"<Make {self.make}>"


class ModelsDirectory(SQLModel, table=True):
    __tablename__ = "modelsdir"
    uid: UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        )
    )
    model: str = Field(nullable=False)

    make_uid: UUID = Field(foreign_key="makesdir.uid")
    make: "MakesDirectory" = Relationship(back_populates="models")

    def __repr__(self):
        return f"<Model {self.model}>"
