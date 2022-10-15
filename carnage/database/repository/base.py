from datetime import datetime
from typing import Any

from sqlalchemy import insert, select, update

from carnage.database.models.base import BaseModel
from carnage.database.session import session


class BaseRepository:
    def __init__(self, model: BaseModel = BaseModel) -> None:
        self.session = session
        self.model = model

    def insert(self, values: list[dict[str, Any]] | dict[str, Any]) -> None:
        statement = insert(self.model).values(values)

        with self.session() as session:
            session.execute(statement=statement)
            session.commit()

    def select(self) -> list[BaseModel]:
        statement = select(self.model)

        with self.session() as session:
            return session.execute(statement=statement).scalars().all()

    def select_first(self) -> BaseModel:
        statement = select(self.model)

        with self.session() as session:
            return session.execute(statement=statement).first()

    def select_by_id(self, identifier: str) -> BaseModel:
        statement = select(self.model).where(self.model.id == identifier)
        with self.session() as session:
            return session.execute(statement=statement).first()

    def select_by_name(self, name: str) -> BaseModel:
        statement = select(self.model).where(self.model.name == name)

        with self.session() as session:
            return session.execute(statement=statement).first()

    def update(self, values: dict[str, Any], identifier: str) -> None:
        statement = (
            update(self.model)
            .values(values)
            .where(
                self.model.id == identifier,
            )
        )

        with self.session() as session:
            session.execute(statement=statement)
            session.commit()

    def delete(self, identifier: str) -> None:
        statement = (
            update(self.model)
            .values({"deleted_at": datetime.now()})
            .where(self.model.id == identifier)
        )

        with self.session() as session:
            session.execute(statement=statement)
            session.commit()