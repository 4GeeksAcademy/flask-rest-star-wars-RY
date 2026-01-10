from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# 1. Tabla Usuario
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    
    # Relaciones
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="user")
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(back_populates="user")
    favorite_starships: Mapped[list["FavoriteStarship"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

# 2. Tabla Planetas
class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    weather: Mapped[str] = mapped_column(String(50), nullable=True)

    residents: Mapped[list["Character"]] = relationship(back_populates="residence")
    favorited_by: Mapped[list["FavoritePlanet"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "weather": self.weather
        }

# 3. Tabla Starships
class Starship(db.Model):
    __tablename__ = 'starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cc: Mapped[str] = mapped_column(String(50), nullable=True)

    pilot: Mapped["Character"] = relationship(back_populates="piloted_ship")
    favorited_by: Mapped[list["FavoriteStarship"]] = relationship(back_populates="starship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cc": self.cc
        }

# 4. Tabla Personajes
class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    
    residence_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    pilot_id: Mapped[int] = mapped_column(ForeignKey('starship.id'), unique=True, nullable=True) 

    residence: Mapped["Planet"] = relationship(back_populates="residents")
    piloted_ship: Mapped["Starship"] = relationship(back_populates="pilot")
    favorited_by: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "residence_id": self.residence_id,
            "pilot_id": self.pilot_id
        }

# 5. Favoritos Personajes
class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

# 6. Favoritos Planetas
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

# 7. Favoritos Starships
class FavoriteStarship(db.Model):
    __tablename__ = 'favorite_starship'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    starship_id: Mapped[int] = mapped_column(ForeignKey('starship.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_starships")
    starship: Mapped["Starship"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }