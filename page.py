from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    website_id = Column(String, ForeignKey("websites.id"))
    website = relationship("Website", backref="pages")
