from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from . import db


class Login(db.Model):
    __tablename__ = "login"

    gmail = Column(String, primary_key=True)
    password = Column(String)
    


   



