import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Area(Base):
    __tablename__ = 'area'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)


class CatalogItem(Base):
    __tablename__ = 'catalogitem'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(700))
    city = Column(String(250))
    price = Column(String(8))
    area_id = Column(Integer, ForeignKey('area.id'))
    area = relationship(Area)


engine = create_engine('sqlite:///properteez_list.db')


Base.metadata.create_all(engine)