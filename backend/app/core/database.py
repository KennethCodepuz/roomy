
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import  UniqueConstraint, text, Column, Integer, String, DateTime, ForeignKey, func, Enum, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal
import os
import uuid
import enum

load_dotenv()
url = os.getenv("DATABASE_URL")
if not url:
   raise RuntimeError("DATABASE_URL is not set")

engine = create_async_engine(url)

class Base(DeclarativeBase):
   pass

class Users(Base):
   __tablename__ = "users"
   __table_args__ = (
      UniqueConstraint("oauth_provider", "oauth_subject_id", name="uq_users_oauth_identity"),
   )

   id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
   name: Mapped[str] = mapped_column(String, nullable=False)
   sex: Mapped[str] = mapped_column(String, nullable=False)
   age: Mapped[int] = mapped_column(Integer, nullable=False)
   avatar_url: Mapped[str] = mapped_column(String, nullable=False)
   oauth_provider: Mapped[str] = mapped_column(String, nullable=False)
   oauth_subject_id: Mapped[str] = mapped_column(String, nullable=False)
   created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
   updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

   listings: Mapped[list["Listings"]] = relationship(back_populates="user")

class ListingType(str, enum.Enum):
   offer_room = "offer_room"
   find_roommate = "find_roommate"
   seek_room = "seek_room"

class Locations(str, enum.Enum):
   city_of_manila = "city_of_manila"

class RoommateGenderPreference(str, enum.Enum):
   male = "MALE"
   female = "FEMALE"
   both = "BOTH"

class Listings(Base):
   __tablename__ = "listings"

   id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
   # Use enum for set in stone choices values, so that no other values are accepted 
   listing_type: Mapped[ListingType] = mapped_column(Enum(ListingType), nullable=False)
   title: Mapped[str] = mapped_column(String)
   description: Mapped[str] = mapped_column(String)
   price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
   # Use enums here to make it strictly Manile Area
   # Future: make a table with seeded areas/locations and use it in the future
   area: Mapped[Locations] = mapped_column(Enum(Locations), nullable=False)
   roommate_gender_preference: Mapped[RoommateGenderPreference] = mapped_column(Enum(RoommateGenderPreference))
   status: Mapped[str] = mapped_column(String, nullable=False)
   open_for_roommates: Mapped[bool] = mapped_column(Boolean, nullable=False)
   created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
   updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

   user: Mapped["Users"] = relationship(back_populates="listings")



async def ping_db():
   async with engine.connect() as conn:
      result = await conn.execute(text("SELECT 1"))
      return {"result": result.all()[0][0]}



