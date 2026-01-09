
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Un usuario puede guardar muchos favoritos de cada tipo
    favorite_characters = db.relationship(
        "FavoriteCharacter", back_populates="user", cascade="all, delete-orphan"
    )
    favorite_planets = db.relationship(
        "FavoritePlanet", back_populates="user", cascade="all, delete-orphan"
    )
    favorite_starships = db.relationship(
        "FavoriteStarship", back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, it's a security breach
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    weather: Mapped[str] = mapped_column(String(100))  # clima (ej. "arid", "temperate")

    # Relación: un planeta tiene muchos residentes (characters)
    residents = db.relationship("Character", back_populates="residence_planet")
    favorites = db.relationship(
        "FavoritePlanet", back_populates="planet", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "weather": self.weather,
            "residents_count": len(self.residents) if self.residents else 0,
        }


class Starship(db.Model):
    __tablename__ = "starships"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(120))
    manufacturer: Mapped[str] = mapped_column(String(120))

    # Relación 1:1 con Character (piloto principal)
    pilot = db.relationship("Character", back_populates="starship", uselist=False)

    favorites = db.relationship(
        "FavoriteStarship", back_populates="starship", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "pilot_id": self.pilot.id if self.pilot else None,
        }


class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[str] = mapped_column(String(10))  

    # Residente de un planeta (N:1)
    residence_planet_id: Mapped[int] = mapped_column(
        db.ForeignKey("planets.id")
    )
    residence_planet = db.relationship("Planet", back_populates="residents")

    # Pilotea una nave (1:1). UNIQUE asegura que cada starship tenga a lo sumo un piloto
    starship_id: Mapped[int] = mapped_column(
        db.ForeignKey("starships.id"), unique=True
    )
    starship = db.relationship("Starship", back_populates="pilot", uselist=False)

    favorites = db.relationship(
        "FavoriteCharacter", back_populates="character", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "residence_planet_id": self.residence_planet_id,
            "starship_id": self.starship_id,
        }

class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_characters"
    __table_args__ = (
        db.UniqueConstraint("user_id", "character_id", name="uq_user_character"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("characters.id"), nullable=False)

    user = db.relationship("User", back_populates="favorite_characters")
    character = db.relationship("Character", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    __table_args__ = (
        db.UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey("planets.id"), nullable=False)

    user = db.relationship("User", back_populates="favorite_planets")
    planet = db.relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }


class FavoriteStarship(db.Model):
    __tablename__ = "favorite_starships"
    __table_args__ = (
        db.UniqueConstraint("user_id", "starship_id", name="uq_user_starship"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    starship_id: Mapped[int] = mapped_column(db.ForeignKey("starships.id"), nullable=False)

    user = db.relationship("User", back_populates="favorite_starships")
    starship = db.relationship("Starship", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
        }
