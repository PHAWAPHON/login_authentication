from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from . import db


class Register(db.Model):
    __tablename__ = "register"

    id = Column(Integer, primary_key=True)
   # userName = Column(String, unique=True, nullable=False)
    gmail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    
  
