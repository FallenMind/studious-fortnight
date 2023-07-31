from typing import ForwardRef

from pydantic import BaseModel, Field
from pydantic.types import Decimal
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

SubMenuRef = ForwardRef('SubmenuSchema')
DishRef = ForwardRef('DishSchema')


async def create_tables(engine):
    global Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)
    menu = relationship('Menu', back_populates='submenus')

    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False, default=Decimal('0.0'))  # Use Numeric with 10, 2 precision

    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship('Submenu', back_populates='dishes')


class SubmenuSchema(BaseModel):
    title: str = Field(..., title="Title of the submenu")
    description: str = Field(..., title="Description of the submenu")

    class Config:
        orm_mode = True
        validate_assignment = True


class DishSchema(BaseModel):
    title: str = Field(..., title="Title of the dish")
    description: str = Field(..., title="Description of the dish")
    price: str = Field(..., title="Price of the dish")

    class Config:
        orm_mode = True
        validate_assignment = True


class MenuSchema(BaseModel):
    title: str = Field(..., title="Title of the menu")
    description: str = Field(..., title="Description of the menu")

    class Config:
        orm_mode = True
        validate_assignment = True


class MenuAll(MenuSchema):
    id: str
    submenus_count: int
    dishes_count: int


class SubmenuAll(SubmenuSchema):
    id: str
    dishes_count: int


class DishAll(DishSchema):
    id: str
