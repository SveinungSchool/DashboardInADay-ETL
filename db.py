from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Relationship
from sqlalchemy import ForeignKey
import datetime


# declarative base class
class Base(DeclarativeBase):
    pass


class Manufacturer(Base):
    __tablename__ = "Manufacturer"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))


class Product(Base):
    __tablename__ = "Products"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    manufacturer_id : Mapped[int] = mapped_column(ForeignKey("Manufacturer.id"))

class Sales(Base):
    __tablename__ = "Sales"
    id : Mapped[int] = mapped_column(primary_key=True)
    revenue : Mapped[float] = mapped_column()
    quantity : Mapped[int] = mapped_column()
    product_id : Mapped[int] = mapped_column(ForeignKey("Products.id"))
    product : Mapped[Product] = Relationship(Product)
    country : Mapped[str] = mapped_column(String(100))
    zip : Mapped[str] = mapped_column(String(100))
    date : Mapped[datetime.date] = mapped_column()

class Geography(Base):
    __tablename__ = "Geography"        
    zip : Mapped[str] = mapped_column(String(10), primary_key=True)
    country : Mapped[str] = mapped_column(String(20),primary_key=True,nullable=True)
    state : Mapped[str] = mapped_column(String(10),nullable=True)
    district : Mapped[str] = mapped_column(String(50),nullable=True)
    region : Mapped[str] = mapped_column(String(50),nullable=True)
    city : Mapped[str] = mapped_column(String(50),nullable=True)
    


def create_database(engine):
    Base.metadata.create_all(engine)