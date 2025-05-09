from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from ..db import db
class Moon(db.Model):
    __tablename__ = "moons"

    id:              Mapped[int]    = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:            Mapped[str]    = mapped_column(String, nullable=False)
    size:            Mapped[float]  = mapped_column(Float, nullable=False)
    description:     Mapped[str]    = mapped_column(String, nullable=True)
    orbital_period:  Mapped[float]  = mapped_column(Float, nullable=True)   # your extra attribute

    planet_id:       Mapped[int]    = mapped_column(
                                            Integer, 
                                            ForeignKey("planets.id"), 
                                            nullable=False
                                         )

    planet:          Mapped["Planet"] = relationship(
                                            "Planet", 
                                            back_populates="moons"
                                         )

    def to_dict(self):
        return {
            "id":             self.id,
            "name":           self.name,
            "size":           self.size,
            "description":    self.description,
            "orbital_period": self.orbital_period,
            "planet_id":      self.planet_id
        }

    @classmethod
    def from_dict(cls, data: dict, planet_id: int):
        return cls(
            name            = data["name"],
            size            = data["size"],
            description     = data.get("description"),
            orbital_period  = data.get("orbital_period"),
            planet_id       = planet_id
        )