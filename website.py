from base import Base
from sqlalchemy import Column, Integer, String, Boolean


class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    html = Column(Boolean)
