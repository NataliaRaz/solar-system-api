
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import String, Float, Integer

class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int]              = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]            = mapped_column(String, nullable=False)
    description: Mapped[str]     = mapped_column(String, nullable=True)
    distance_from_sun: Mapped[float] = mapped_column(Float, nullable=True)

    moons: Mapped[list["Moon"]] = relationship(
        "Moon",
        back_populates="planet",
        cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        planet_as_dict = {}
        planet_as_dict["id"] = self.id
        planet_as_dict["name"] = self.name
        planet_as_dict["description"] = self.description
        planet_as_dict["distance_from_sun"] = self.distance_from_sun
        planet_as_dict["moons"] = [m.to_dict() for m in self.moons]

        return planet_as_dict

    @classmethod
    def from_dict(cls, planet_data: dict) -> "Planet":
        name               = planet_data["name"]
        description        = planet_data["description"]
        distance_from_sun  = planet_data["distance_from_sun"]
        return cls(
            name=name,
            description=description,
            distance_from_sun=distance_from_sun
        )